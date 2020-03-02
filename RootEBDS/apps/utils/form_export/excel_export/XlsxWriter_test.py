import os
import time
import django

start_time = time.time()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.settings")  # project_name 项目名称
django.setup()
set_up_djangp_time = time.time()
print("setup django花费", set_up_djangp_time - start_time)
import xlsxwriter as xlwt
from dms.models.daily_models import DmsWorkerDaily

work_book = xlwt.Workbook(r'C:\documents\share\excelTest.xlsx')
worker_daily_data_sheet = work_book.add_worksheet("worker_daily_data")
date_format = work_book.add_format({'num_format': 'yyyy/m/d'})
date_column = 4
open_excel_time = time.time()
print("打开excel花费", open_excel_time - set_up_djangp_time)

worker_daily_data = DmsWorkerDaily.objects.all().order_by('efficiency')

for i, one_worker_daily_data in enumerate(worker_daily_data):
    data = [float(one_worker_daily_data.efficiency),
            float(one_worker_daily_data.accuracy),
            float(one_worker_daily_data.workhour),
            one_worker_daily_data.worker_id]
    worker_daily_data_sheet.write_row('A' + str(i + 1), data)
    worker_daily_data_sheet.set_column(date_column, date_column, 13)
    worker_daily_data_sheet.write_datetime(row=i, col=date_column,
                                           date=one_worker_daily_data.time, cell_format=date_format)

work_book.close()
write_and_save_excel_time = time.time()
print("写入并保存花费", write_and_save_excel_time - open_excel_time)


