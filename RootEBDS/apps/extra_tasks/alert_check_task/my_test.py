# import django
# import os
# import datetime
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RootEBDS.EBDS.settings")
# django.setup()
#
#
# from ams.models import AmsBaseInfo
# cur_time = datetime.datetime.now()
# res = AmsBaseInfo.objects.filter(start_time__gte=cur_time.date()).order_by("-alert_id")[0]
#
# print(res)
# 组长工号，组长姓名，收到警报数量，超时数量，处理数量
# from django.db.models import Count
#
# group_alert_query_set = AmsConveyInfo.objects.filter(role_id=2, deal_employee_id__lte=42) \
#     .values("deal_employee_id", "deal_employee_name", "is_timeout")
# data_list = [["组长工号", "组长姓名", "按时处理警报总数", "收到警报总数", "超时未处理警报总数"]]
# pre_employee_id = 0
# pre_employee_name = ""
# cur_employee_id = 0
# cur_employee_name = ""
# receive_num = 0
# time_out_num = 0
# for one_group in group_alert_query_set:
#     cur_employee_id = one_group["deal_employee_id"]
#     cur_employee_name = one_group["deal_employee_name"]
#     if cur_employee_id != pre_employee_id:  # 切换员工
#         if pre_employee_id != 0:  # 不是第一个员工
#             data_list.append([
#                 pre_employee_id,
#                 pre_employee_name,
#                 0,
#                 receive_num,
#                 time_out_num
#             ])
#         pre_employee_id = cur_employee_id
#         pre_employee_name = cur_employee_name
#         receive_num = 0
#         time_out_num = 0
#     receive_num += 1
#     if one_group["is_timeout"]:
#         time_out_num += 1
#
# if len(group_alert_query_set) != 0:
#     data_list.append([
#         cur_employee_id,
#         cur_employee_name,
#         0,
#         receive_num,
#         time_out_num
#     ])
#
# # 查询最终处理人数量
# final_deal_query_set = AmsBaseInfo.objects.filter(deal_role_id=2, status=2) \
#     .values("final_deal_employee_id", "final_deal_employee_name") \
#     .annotate(cnt=Count("final_deal_employee_id"))
#
# index = 0
# if len(final_deal_query_set) != 0:
#     for item in data_list:
#         if item[0] == final_deal_query_set[index]["final_deal_employee_id"]:
#             item[2] = final_deal_query_set[index]["cnt"]
#             index += 1
#             if index >= len(final_deal_query_set):
#                 break
#
# print(data_list)
