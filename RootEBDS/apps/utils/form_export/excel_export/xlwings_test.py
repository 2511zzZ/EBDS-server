import os
import time
import django

start_time = time.time()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.settings")  # project_name 项目名称
django.setup()
set_up_djangp_time = time.time()
print("setup django花费", set_up_djangp_time - start_time)
import xlwings as xw
from dms.models.daily_models import DmsWorkerDaily

app = xw.App(visible=True, add_book=False)
wb = app.books.add()
# wb.sheets['sheet1'].range('A1').value = '233'
# s2 = wb.sheets.add('s2', after='sheet1')
# s2.range('A2').value = [1, 2, 3]
# wb.sheets['sheet1'].delete()
wb.sheets.add('worker_daily')
s1 = wb.sheets['worker_daily']  # type: wb.sheets
s1.activate()
open_excel_time = time.time()
print("打开excel花费", open_excel_time - set_up_djangp_time)

worker_daily_data = DmsWorkerDaily.objects.all().order_by('efficiency')

# print(worker_daily_data)
for i, one_worker_daily_data in enumerate(worker_daily_data):
    data = [float(one_worker_daily_data.efficiency),
            float(one_worker_daily_data.accuracy),
            float(one_worker_daily_data.workhour),
            one_worker_daily_data.time,
            one_worker_daily_data.worker_id]
    s1.range('A' + str(i + 1)).value = data
    if i % 20 == 0:
        print(i)
wb.save(r'C:\documents\share\excelTest.xlsx')
wb.activate()
write_and_save_excel_time = time.time()
print("写入并保存花费", write_and_save_excel_time - open_excel_time)

time.sleep(1.5)
app.activate()
# wb.close()
# app.quit()
