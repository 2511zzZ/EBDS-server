import datetime
import decimal
import json

# import django
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RootEBDS.EBDS.settings")
# django.setup()

from ams.models import AmsBaseInfo, AmsConveyInfo
from cfg.models import CfgWorkPeriod, CfgAlertCondition
from django.db.models import Max, Count
from dms.models.online_models import DmsStatOnline
from sms.models import TeamStatMember, Member, TeamGroupWorkshop, Group, Workshop, Dpt
from standard.models import StandardTeam

from utils.static_methods import get_cur_stat_employee, get_superior_manager_dict
from utils.redis_tools import RedisClient
from extra_tasks.configs import RESEARCH_INTERVAL


def get_diff(time1, time2):
    # 返回除了日期的两个时间的差值(分钟)
    t1 = time1.hour * 60 + time1.minute
    t2 = time2.hour * 60 + time2.minute
    diff = t2 - t1
    return diff


def is_switching(cur_time, duration):
    # 查询换班时间
    morning = CfgWorkPeriod.objects.filter(name="morning")[0].start_time
    middle = CfgWorkPeriod.objects.filter(name="middle")[0].start_time
    night = CfgWorkPeriod.objects.filter(name="night")[0].start_time
    morning_diff = get_diff(morning, cur_time)
    middle_diff = get_diff(middle, cur_time)
    night_diff = get_diff(night, cur_time)
    if (0 < morning_diff < duration) or (0 < middle_diff < duration) or (0 < night_diff < duration):
        return True
    return False


def get_team_s_eff_dict():
    standard_team_query_set = StandardTeam.objects.all()
    team_s_eff_dict = {}
    for standard_team_obj in standard_team_query_set:
        team_s_eff_dict[standard_team_obj.team_id] = {
            "s_efficiency": standard_team_obj.s_efficiency,
            "s_accuracy": standard_team_obj.s_accuracy,
            "s_workhour": standard_team_obj.s_workhour
        }
    return team_s_eff_dict


def get_stat_team_dict():
    team_stat_member_query_set = TeamStatMember.objects.all()
    stat_team_dict = {}
    for team_stat_member_obj in team_stat_member_query_set:
        stat_team_dict[team_stat_member_obj.stat_id] = team_stat_member_obj.team_id
    return stat_team_dict


def analysis_reason(cur_stat_max_eff, time_diff):
    """
    根据效率/准确率/工时分析警报原因（暂时只传入效率
    :param time_diff: 时间差
    :param cur_stat_max_eff:当前工位最高效率
    :return: 字符串形式的原因描述
    """
    reason = ""
    if cur_stat_max_eff != 0:
        reason = f"持续{time_diff}分钟效率未达标"
    elif cur_stat_max_eff == 0:
        reason = f"缺人持续{time_diff}分钟"

    return reason


def convey(convey_alert_info_query_set, cur_time):
    """
    用当前时间和警报被传递到的最高等级时间进行比较。
    未超时则不做处理。
    超时则关闭或者向上层传递
    :param: 同一个警报的传递信息
    """
    transfer_conf = RedisClient.cfg_alert_transfer_conf()
    timeout = transfer_conf["timeout"]
    max_timeout = transfer_conf["max_timeout"]
    try:
        convey_info_cur_max_level = convey_alert_info_query_set.order_by("-role_id")[0]
    except IndexError:
        print("convey_alert_info角色Id排序为0")
        return
    if convey_info_cur_max_level.role_id == 4:
        # 拿到这个警报的开始时间start_time
        cur_alert_start_time = AmsBaseInfo.objects\
            .get(alert_id=convey_info_cur_max_level.alert_id)\
            .start_time
        if (cur_time - cur_alert_start_time) > datetime.timedelta(minutes=max_timeout) - datetime.timedelta(seconds=30):
            # 警报传递到了总经理，且总经理超过max_timeout时间没有处理
            convey_info_cur_max_level.is_timeout = 1
            convey_info_cur_max_level.save()
            # 关闭警报
            base_obj = AmsBaseInfo.objects.get(alert_id=convey_info_cur_max_level.alert_id)
            base_obj.end_time = cur_time
            base_obj.status = 3
            base_obj.save()
        return convey_info_cur_max_level.deal_employee_id, convey_info_cur_max_level.alert_id
    if (cur_time - convey_info_cur_max_level.time) > datetime.timedelta(minutes=timeout) - datetime.timedelta(seconds=30):
        # 警报超时，需要向上级传递
        convey_info_cur_max_level.is_timeout = 1
        convey_info_cur_max_level.save()
        # 查询上级employee_id和name
        superior_manager_dict = get_superior_manager_dict(convey_info_cur_max_level.deal_employee_id,
                                                          convey_info_cur_max_level.role_id)
        AmsConveyInfo.objects.create(deal_employee_id=superior_manager_dict["employee_id"],
                                     deal_employee_name=superior_manager_dict["employee_name"],
                                     role_id=convey_info_cur_max_level.role_id+1, is_timeout=0,
                                     is_delete=0, time=cur_time, alert_id=convey_info_cur_max_level.alert_id)
        return superior_manager_dict["employee_id"], convey_info_cur_max_level.alert_id
    return ()


def generate_alert_base_info():
    cur_time = datetime.datetime.now()
    # 查询低于标准的持续时间
    alert_condition_conf = RedisClient.cfg_alert_condition_conf()
    duration = alert_condition_conf["duration"]
    percent = alert_condition_conf["percent"]
    # 判断是否在换班中
    if is_switching(cur_time, duration):
        print("正处于换班时间 不进行警报生成")
        return
    # 没在换班就开始查stat_online表
    stat_data_query_set = DmsStatOnline.objects.\
        filter(time__gte=cur_time - datetime.timedelta(minutes=duration) - datetime.timedelta(seconds=30),
               time__lte=cur_time).values("stat_id").annotate(cnt=Count("*"), max_eff=Max("efficiency"))
    try:
        if stat_data_query_set[0]["cnt"] < duration:
            return
    except IndexError:
        print("数据库没有stat_online数据")
    # 获取team-s_eff的字典映射
    team_s_eff_dict = get_team_s_eff_dict()
    # 获取stat_team的字典映射
    stat_team_dict = get_stat_team_dict()
    # 循环判断每一个工位
    for one_stat_data in stat_data_query_set:
        cur_stat_id = one_stat_data["stat_id"]
        cur_stat_max_eff = one_stat_data["max_eff"]
        cur_team = stat_team_dict[cur_stat_id]
        cur_stat_standard_eff = team_s_eff_dict[cur_team]["s_efficiency"]
        if decimal.Decimal(cur_stat_max_eff / cur_stat_standard_eff) < (1 - percent):
            # 该工位这段时间效率不达标
            cur_stat_employee_id = get_cur_stat_employee(cur_stat_id)
            # 获取今天总警报编号
            try:
                next_num = AmsBaseInfo.objects.filter(start_time__gte=cur_time.date()).order_by("-alert_id")[0]
                next_num = int(str(next_num)[6:]) + 1
            except IndexError:
                next_num = 1
            # 拼接alert_id
            if next_num < 1000:
                next_num = "%04d" % next_num
            else:
                next_num = str(next_num)
            alert_id = int(cur_time.date().strftime("%Y%m%d")[2:] + next_num)
            # 该工位当前员工姓名
            cur_employee_name = Member.objects.get(employee_id=cur_stat_employee_id).name
            # 警报原因
            reason = analysis_reason(cur_stat_max_eff, duration)
            # 把相关数据插入ams_base_info
            AmsBaseInfo.objects.create(alert_id=alert_id, stat_id=cur_stat_id,
                                       employee_id=cur_stat_employee_id, employee_name=cur_employee_name,
                                       reason=reason, start_time=cur_time)
    print(f"警报生成 完成{cur_time}")


def convey_alert():
    cur_time = datetime.datetime.now()
    waiting_base_query_set = AmsBaseInfo.objects.filter(status=None)
    conveying_base_query_set = AmsBaseInfo.objects.filter(status=1)
    to_be_notified_employee_id = set()
    to_be_notified_alert_id = set()

    # 处理等待传递的警报
    for waiting_alert in waiting_base_query_set:
        # 根据当前工位取到其大组长的id和name
        group_manager_dict = get_superior_manager_dict(waiting_alert.stat_id, 0)
        if (cur_time - waiting_alert.start_time) > datetime.timedelta(seconds=RESEARCH_INTERVAL):
            # 系统异常
            waiting_alert.status = -1
            waiting_alert.save()
            # 只有警报状态发生变化才需要通知socket
            to_be_notified_alert_id.add(waiting_alert.alert_id)
        else:
            # 传递警报
            waiting_alert.status = 1
            waiting_alert.save()
            # 插入警报传递信息
            AmsConveyInfo.objects.create(deal_employee_id=group_manager_dict["employee_id"],
                                         deal_employee_name=group_manager_dict["employee_name"],
                                         role_id=2, is_timeout=0, is_delete=0, time=cur_time,
                                         alert_id=waiting_alert.alert_id)
        # 存储此警报的接收人员信息和警报信息
        to_be_notified_employee_id.add(group_manager_dict["employee_id"])
    # 处理正在传递的警报
    for conveying_base_obj in conveying_base_query_set:
        # 获取该警报的ams_convey_info查询集
        convey_alert_info_query_set = AmsConveyInfo.objects.filter(alert_id=conveying_base_obj.alert_id)
        # 将警报向上级传递
        superior_id_and_alert_id = convey(convey_alert_info_query_set, cur_time)
        # 如果警报超时，则存储此接收此警报的人员信息和警报信息
        if len(superior_id_and_alert_id) != 0:
            to_be_notified_employee_id.add(superior_id_and_alert_id[0])
            to_be_notified_alert_id.add(superior_id_and_alert_id[1])

    # 合并两个集合中的employee_id
    alert_employees = AmsConveyInfo.objects.filter(alert_id__in=to_be_notified_alert_id).values_list('deal_employee_id')
    alert_employees = set([i[0] for i in alert_employees])
    to_be_notified_employee_ids = alert_employees | to_be_notified_employee_id
    # 把需要通知的employee的employee_id存到redis中
    RedisClient().redis.hset('ws', 'ws_alert_send_messages', json.dumps(list(to_be_notified_employee_ids)))
    print(f"警报传递 完成{cur_time}")


generate_alert_base_info()
convey_alert()
