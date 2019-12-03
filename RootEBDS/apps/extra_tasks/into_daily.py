import datetime
import decimal

from db_tools.tools.tools import get_db_connector
from extra_tasks.configs import STAT_NUMBER, WORKER_NUMBER, DAILY_UPDATE_TIME, DAILY_UPDATE_ITERVAL
from extra_tasks.save_datas import SaveData
from dms.models.online_models import DmsStatOnline


def get_daily(level: str):     # stat
    table_name = "dms_"+level+"_avg"
    con = get_db_connector()
    cursor = con.cursor(dictionary=True)
    today = datetime.datetime.today()
    datetime_now = datetime.datetime(today.year, today.month, today.day,
                                     DAILY_UPDATE_TIME["hour"], DAILY_UPDATE_TIME["minute"], DAILY_UPDATE_TIME["second"])
    # 从avg表中查找当前(00:00)之后五分钟的数据
    sql = "SELECT a_efficiency, a_accuracy ,a_workhour, time, {} FROM {} WHERE time between '{}' and '{}' "\
        .format(level+"_id", table_name, datetime_now, datetime_now+datetime.timedelta(seconds=DAILY_UPDATE_ITERVAL))
    cursor.execute(sql)
    avg_data_list = cursor.fetchall()
    if not avg_data_list:
        raise Exception
    return avg_data_list


def into_daily(level):
    avg_data_list = get_daily(level)
    SaveData(avg_data_list, "dms_"+level+"_daily").insert()


con = get_db_connector()
cursor = con.cursor()
# 获得员工排班表
cursor.execute("SELECT morning_shift_id, middle_shift_id, night_shift_id FROM sms_team_stat_member")
work_timetable = cursor.fetchall()
# 获得时刻表
cursor.execute("SELECT start_time, end_time FROM cfg_work_period")
timetable = cursor.fetchall()
if timetable:
    morning_begin = timetable[0][0]
    morning_end = timetable[0][1]
    middle_begin = timetable[1][0]
    middle_end = timetable[1][1]
    night_begin = timetable[2][0]
    night_end = timetable[2][1]
cursor.close()
con.close()


def time_to_datetime(a_time, cur_time):
    cur_time = datetime.datetime(year=cur_time.year, month=cur_time.month, day=cur_time.day,hour=0, minute=0, second=0)
    res = cur_time+a_time
    return res


# 员工每日数据
def insert_worker_daily_data(cur_time):

    # 查工位效率
    morning_data = DmsStatOnline.objects.filter(time__gte=time_to_datetime(morning_begin, cur_time),
                                                time__lte=time_to_datetime(morning_end, cur_time))
    middle_data = DmsStatOnline.objects.filter(time__gte=time_to_datetime(middle_begin, cur_time),
                                               time__lte=time_to_datetime(middle_end, cur_time))
    night_data = DmsStatOnline.objects.filter(time__gte=time_to_datetime(night_begin, cur_time),
                                              time__lte=time_to_datetime(night_end, cur_time))
    data = [morning_data, middle_data, night_data]

    i = 0
    for one_data in data:  # 循环早中晚共三次
        efficiency_sum = [0 for i in range(WORKER_NUMBER * 2)]
        accuracy_sum = [0 for i in range(WORKER_NUMBER * 2)]
        workhour_sum = [0 for i in range(WORKER_NUMBER * 2)]
        j = 0
        for one_item in one_data:  # 每分钟每个工位的效率数据 5000 * 早上分钟 次
            efficiency_sum[work_timetable[j][i]] += one_item.efficiency
            accuracy_sum[work_timetable[j][i]] += one_item.accuracy
            workhour_sum[work_timetable[j][i]] += one_item.workhour
            j += 1
            j %= STAT_NUMBER
        # 生成每一条员工效率
        length = decimal.Decimal(len(one_data) / STAT_NUMBER)
        worker_dict_list = list()
        if length == 0:
            print("工位表中没有查到相应数据%d" % i)
        else:
            for one_item in work_timetable:
                one_worker_dict = dict()
                one_worker_dict['worker_id'] = one_item[i]
                one_worker_dict['efficiency'] = round(efficiency_sum[one_item[i]]/length, 1)
                one_worker_dict['accuracy'] = round(accuracy_sum[one_item[i]]/length, 1)
                one_worker_dict['workhour'] = round(workhour_sum[one_item[i]]/length, 1)
                one_worker_dict['time'] = cur_time.date()
                worker_dict_list.append(one_worker_dict)
            SaveData(worker_dict_list, "dms_worker_daily").insert()
        i += 1
