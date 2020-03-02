# coding: utf-8
import datetime
from sms.models import TeamGroupWorkshop, TeamStatMember, Member, Group, Workshop, Dpt
from cfg.models import CfgWorkPeriod
from django.db.models import Max, Q
from django.db import connection


def get_recent_stat_obj(team_id):
    """
    根据小组号获取小组对应的最新十个工位信息
    :return:
    """
    for stat_obj in TeamStatMember.objects.filter(
            id__in=
            TeamStatMember.objects.values('stat_id').
                    annotate(default_id=Max('id')).
                    values('default_id')
    ).filter(team=team_id):
        yield stat_obj


def get_recent_employee_stat_obj(employee_id):
    """
    返回员工目前所在的工位
    :return:
    """
    return TeamStatMember.objects.filter(
        Q(morning_shift_id=employee_id) |
        Q(middle_shift_id=employee_id) |
        Q(night_shift_id=employee_id)
    ).order_by('-update_time')[0]


def get_recent_stat_team_id(stat_ids):
    """
    返回一组工位现在所属的小组号
    :param stat_ids:
    :return: 小组号list
    """
    sql = ("SELECT a.team_id FROM sms_team_stat_member AS a , "
           "(SELECT stat_id, MAX(update_time) AS update_time FROM sms_team_stat_member "
           "WHERE stat_id in ({}) group by stat_id) AS b "
           "WHERE a.stat_id = b.stat_id AND a.update_time=b.update_time".format(
            ','.join(map(str, stat_ids))))
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
    return [row[0] for row in rows]


def get_recent_worker_team_id(worker_ids):
    """
    返回一组员工现在所属的小组号
    :param worker_ids:
    :return: 小组号list
    """
    # 由于实际需求不会有多个worker_id的同时请求，所以这里复用单个id请求的函数 日后方便拓展
    return [get_recent_employee_stat_obj(worker_id).team_id for worker_id in worker_ids]


def get_cur_stat_group_manager(stat_id):
    """
    根据工位id查询该员工大组长的Id和姓名
    :param stat_id:
    :return:
    """
    res_dict = {
        "employee_id": None,
        "employee_name": None
    }
    try:
        team_id = TeamStatMember.objects.filter(stat_id=stat_id)[0].team_id
        group_id = TeamGroupWorkshop.objects.filter(team_id=team_id)[0].group_id
        res_dict["employee_id"] = Group.objects.get(pk=group_id).employee_id
        res_dict["employee_name"] = Member.objects.get(employee_id=res_dict["employee_id"]).name
    except IndexError:
        res_dict = None

    return res_dict


def get_superior_manager_dict(cur_subordinate_id, cur_subordinate_role_id):
    if cur_subordinate_role_id == 2:  # 获取当前管理大组长经理信息
        group_id = Group.objects.get(employee_id=cur_subordinate_id)
        workershop_id = TeamGroupWorkshop.objects.filter(group_id=group_id)[0].workshop_id
        superior_manager_id = Workshop.objects.get(pk=workershop_id).employee_id
        superior_manager_name = Member.objects.get(employee_id=superior_manager_id).name
    elif cur_subordinate_role_id == 3:  # 直接从dpt中获取总经理信息
        superior_manager_id = Dpt.objects.get(pk=1).employee_id
        superior_manager_name = Member.objects.get(employee_id=superior_manager_id).name
    else:  # 需要根据员工信息获取大组长信息
        return get_cur_stat_group_manager(cur_subordinate_id)
    return {
        "employee_id": superior_manager_id,
        "employee_name": superior_manager_name
    }


def get_cur_stat_employee(stat_id):
    """
    :param stat_id:
    :return: 当前工位所工作的员工
    """
    cur_time = datetime.datetime.now().time().strftime("%H:%M:%S")
    cur_period = CfgWorkPeriod.objects.filter(start_time__lte=cur_time,
                                              end_time__gte=cur_time)[0].name
    cur_employee_id = TeamStatMember.objects.filter(stat_id=stat_id) \
        .values(cur_period + "_shift_id").order_by('-update_time')[0][cur_period + "_shift_id"]
    return cur_employee_id


def get_employee_obj(employee_id):
    return Member.objects.filter(employee_id=employee_id)[0]


def get_worker_team_group_workshop(user_id, role_id):
    """
    :param user_id:
    :param role_id:
    :return: 当前角色管理的所有worker_team_group_workshop(如果是经理)
             或worker_team_group或（如果是大组长）
    """
    if role_id == 4:
        sql = ("SELECT b.morning_shift_id, b.middle_shift_id, b.night_shift_id, \
                   a.team_id, a.group_id, a.workshop_id \
                   FROM sms_team_group_workshop as a JOIN sms_team_stat_member as b \
                   ON a.team_id = b.team_id")
    else:
        if role_id == 3:
            user_type = "workshop"
        else:
            user_type = "group"
        managed_id = globals()[user_type.title()].objects.get(employee_id=user_id).id
        sql = ("SELECT b.morning_shift_id, b.middle_shift_id, b.night_shift_id, \
            a.team_id, a.group_id, a.workshop_id \
            FROM sms_team_group_workshop as a JOIN sms_team_stat_member as b \
            ON a.team_id = b.team_id and a.%s = %d"
               ) % (user_type + "_id", managed_id)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()

    return row


def get_all_worker_id(_type, _id):
    """
    :param _type:
    :param _id:
    :return: 当前角色管理的所有员工id
    """
    sql = ("SELECT b.morning_shift_id, b.middle_shift_id, b.night_shift_id  \
                FROM sms_team_group_workshop as a JOIN sms_team_stat_member as b \
                ON a.team_id = b.team_id and a.%s = %d"
           ) % (_type + "_id", _id)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
    all_worker_id = []
    for one_query_set in row:
        for one_id in one_query_set:
            all_worker_id.append(one_id)
    return all_worker_id


def get_worker_member_dict(all_id):
    """
    :param all_id:
    :return: 字典形式的all_id里的所有sms_member信息
    """
    str_id = ""
    for one_id in all_id:
        str_id += str(one_id) + ','
    sql = "SELECT * FROM sms_member WHERE employee_id in (%s)" % str_id[:-1]
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchall()
    worker_member_dict = {}
    for item in row:
        worker_member_dict[item[0]] = [item[1], item[4]]
    return worker_member_dict
