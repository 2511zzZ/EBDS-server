import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EBDS.settings")  # project_name 项目名称
django.setup()

import datetime
from operator import itemgetter

from EBDS.settings import FORM_FILE_PATH
from ams.models import AmsBaseInfo, AmsConveyInfo
from core.name_map import NAME_MAP
from django.db.models import Avg, Count
from utils.static_methods import get_worker_team_group_workshop, get_worker_member_dict
from dms.models.daily_models import DmsStatDaily, DmsWorkerDaily, DmsTeamDaily, DmsGroupDaily, DmsWorkshopDaily, \
    DmsDptDaily
from sms.models import Member, TeamGroupWorkshop, Workshop, Group, TeamStatMember

import xlsxwriter as xlwt
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter


def get_alert_data(start, end):
    group_alert_query_set = AmsConveyInfo.objects.filter(role_id=2, time__gte=start, time__lte=end) \
        .values("deal_employee_id", "deal_employee_name", "is_timeout")
    list_data = []
    pre_employee_id = 0
    pre_employee_name = ""
    cur_employee_id = 0
    cur_employee_name = ""
    receive_num = 0
    time_out_num = 0
    for one_group in group_alert_query_set:
        cur_employee_id = one_group["deal_employee_id"]
        cur_employee_name = one_group["deal_employee_name"]
        if cur_employee_id != pre_employee_id:  # 切换员工
            if pre_employee_id != 0:  # 不是第一个员工
                list_data.append([
                    0,
                    pre_employee_id,
                    pre_employee_name,
                    0,
                    receive_num,
                    time_out_num
                ])
            pre_employee_id = cur_employee_id
            pre_employee_name = cur_employee_name
            receive_num = 0
            time_out_num = 0
        receive_num += 1
        if one_group["is_timeout"]:
            time_out_num += 1

    if len(group_alert_query_set) != 0:
        list_data.append([
            0,
            cur_employee_id,
            cur_employee_name,
            0,
            receive_num,
            time_out_num
        ])

    # 查询最终处理人数量
    final_deal_query_set = AmsBaseInfo.objects.filter(deal_role_id=2, status=2, start_time__gte=start, end_time__lte=end) \
        .values("final_deal_employee_id", "final_deal_employee_name") \
        .annotate(cnt=Count("final_deal_employee_id"))
    # 添加到结果集
    index = 0
    if len(final_deal_query_set) != 0:
        for item in list_data:
            if item[1] == final_deal_query_set[index]["final_deal_employee_id"]:
                item[3] = final_deal_query_set[index]["cnt"]
                index += 1
                if index >= len(final_deal_query_set):
                    break

    # 排序
    list_data.sort(key=itemgetter(4, 5))
    list_data.sort(key=itemgetter(3), reverse=True)
    # 添加排名
    for i, item in enumerate(list_data):
        item[0] = i + 1
    # 添加表头
    table_name = ["排名", "组长工号", "组长姓名", "按时处理警报总数", "收到警报总数", "超时未处理警报总数"]
    list_data.insert(0, table_name)
    return list_data


def create_xlsx(path, sheet_name, list_data, width=13):
    """
    根据传入的路径,表单名和列表形式数据（包括表头）创建excel文件
    :param width:
    :param sheet_name:
    :param path:
    :param list_data:
    :return:
    """
    # 创建xlsx文件和sheet
    work_book = xlwt.Workbook(path)
    worker_daily_data_sheet = work_book.add_worksheet(sheet_name)
    formats = {
        # 'bold': True,  # 字体加粗
        # 'num_format':'$#,##0',#货币数字显示样式
        'align': 'center',  # 水平位置设置：居中
        'valign': 'vcenter',  # 垂直位置设置，居中
        'font_size': 10,  # '字体大小设置'
        'font_name': 'Courier New',  # 字体设置
        # 'italic': True,  # 斜体设置
        # 'underline': 1,  # 下划线设置 1.单下划线 2.双下划线 33.单一会计下划线 34双重会计下划线
        # 'font_color': "red",  # 字体颜色设置
        'border': 1,  # 边框设置样式1
        # 'border_color': 'green',  # 边框颜色
        # 'bg_color': '#c7ffec',  # 背景颜色设置
    }
    str_format = work_book.add_format(formats)

    # 写入列表格式数据

    worker_daily_data_sheet.set_column(0, len(list_data[0]), width)
    for i, one_list in enumerate(list_data):
        worker_daily_data_sheet.write_row('A' + str(i + 1), one_list, str_format)

    work_book.close()


def create_pdf(path, title, col_wid, table_data, start: str, end: str, water_mark_text, password):
    """
    根据传入的数据创建pdf文件。
    :param col_wid:
    :param path:
    :param title:
    :param table_data:
    :param start: 被统计数据开始时间(string)
    :param end: 被统计数据结束时间(string)
    :param water_mark_text: 水印文本内容
    :param password: 密码为None表示无密码
    :return: 无返回值
    """
    # 生成一个未加水印的临时pdf
    temp_path = os.path.join(FORM_FILE_PATH, "temp.pdf")
    pdfmetrics.registerFont(TTFont('pingbold', 'PingBold.ttf'))
    pdfmetrics.registerFont(TTFont('ping', 'ping.ttf'))

    flow_data = []
    style_sheet = getSampleStyleSheet()
    normal_style = style_sheet['Normal']

    cur_date = datetime.datetime.now().date().strftime("%Y-%m-%d")
    rpt_title = "<para autoLeading='off' fontSize=17 align=center>" \
                "<font face='ping'>"f"<b>{title}</b></font>" \
                f"<br/><br/></para>"
    export_data_para = "<para autoLeading='off' fontSize=12 align=center>" \
                       "<font face='ping'>"f"<i>({start}到{end})</i></font>" \
                       "<br/><br/><br/></para>"
    cur_date_para = "<para autoLeading='off' fontSize=8 align=right>" \
                    f"<font face='ping' color=grey>导出日期: {cur_date}</font>" \
                    "<br/></para>"

    # 生成表格流对象
    component_table = Table(table_data, colWidths=[col_wid for i in range(len(table_data[0]))],
                            rowHeights=10)
    # 添加表格样式
    component_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'ping'),  # 字体
        ('FONTSIZE', (0, 0), (-1, -1), 6.5),  # 字体大小
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightskyblue),  # 设置第一行背景颜色
        ('LINEBEFORE', (0, 0), (0, -1), 0.1, colors.grey),  # 设置表格左边线颜色为灰色，线宽为0.1
        # ('TEXTCOLOR', (0, 1), (1, 1), colors.red),  # 设置表格内文字颜色
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
        # ('GRID', (0, 0), (-1, -1), 0.1, colors.black),  # 设置表格框线，线宽为0.5
    ]))
    flow_data.append(Paragraph(rpt_title, normal_style))
    flow_data.append(Paragraph(export_data_para, normal_style))
    flow_data.append(Paragraph(cur_date_para, normal_style))
    flow_data.append(component_table)

    doc = SimpleDocTemplate(temp_path)
    doc.build(flow_data)
    # 生成只有水印的pdf
    watermark_path = create_watermark_file(water_mark_text)
    # 合并两个文件，如果有密码则加密
    merge_pdf_with_watermark(watermark_path, temp_path, path, password)


def create_alert_rank_xlsx(path, start, end):
    list_data = get_alert_data(start, end)
    create_xlsx(path, "警报处理排名", list_data, 19)


def create_alert_rank_pdf(path, start, end, password):
    list_data = get_alert_data(start, end)
    create_pdf(path, "警报处理排名", 60, list_data, start.strftime("%Y-%m-%d"),
               end.strftime("%Y-%m-%d"), "流流流流水县", password)


def create_efficiency_rank_xlsx(path, _type, all_id, start, end, user_id, role_id):
    # 查表拿到数据
    """
    list格式数据：[[第0个是需插入的表头], [后面就是相对应的数据], .......]
    """
    if _type == "worker":
        list_data = get_worker_export_data(all_id, start, end, user_id, role_id)
    else:
        list_data = get_export_data(_type, all_id, start, end, user_id, role_id)
    sheet_name = "效率排名"
    # 将数据写入excel文件
    create_xlsx(path, sheet_name, list_data)


def create_efficiency_rank_pdf(path, _type, all_id, start, end, water_mark_text, user_id, role_id, password=None):
    # 生成数据集
    if _type == "worker":
        table_data = get_worker_export_data(all_id, start, end, user_id, role_id)
    else:
        table_data = get_export_data(_type, all_id, start, end, user_id, role_id)
    # 得到标题
    title = NAME_MAP[_type] + "效率排名"
    # 生成pdf
    create_pdf(path, title, 35, table_data, start, end, water_mark_text, password)

# 将生成的pdf文件与水印pdf文件合并
def merge_pdf_with_watermark(watermark_file, origin_file_name, new_file_name, password):
    # 打开原始的pdf文件,获取文件指针
    origin_file_obj = open(origin_file_name, 'rb')

    # 创建reader对象
    pdf_reader = PdfFileReader(origin_file_obj, strict=False)

    # 创建一个指向新的pdf文件的指针
    pdf_writer = PdfFileWriter()

    # 通过迭代将水印添加到原始pdf的每一页
    # 打开水印pdf文件
    watermark_file_obj = open(watermark_file, 'rb')
    for page in range(pdf_reader.numPages):
        wm_page_obj = add_watermark(watermark_file_obj, pdf_reader.getPage(page))
        # 将合并后的即添加了水印的page对象添加到pdfWriter
        pdf_writer.addPage(wm_page_obj)

    # 关闭源pdf
    # origin_file_obj.close()

    # 如果提供了密码，则进行加密
    if password is not None:
        pdf_writer.encrypt(password)

    # 打开新的pdf文件
    new_file = open(new_file_name, 'wb')
    # 将已经添加完水印的pdf_writer对象写入文件
    pdf_writer.write(new_file)

    # 关闭pdf
    origin_file_obj.close()
    watermark_file_obj.close()
    new_file.close()


# 生成只有水印的pdf文件
def create_watermark_file(text):
    # 生成水印文件
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm

    out_file_path = os.path.join(FORM_FILE_PATH, "watermark")
    # text = "WWW.23333.COM"

    c = canvas.Canvas(out_file_path)
    c.setFillColorRGB(0, 0, 0)
    c.setFont("pingbold", 30)

    c.saveState()
    c.translate(18.5 * cm, 23 * cm)
    c.rotate(90)
    c.setFillColorRGB(0.9, 0.9, 0.9)
    c.drawRightString(0, 0, text)
    c.restoreState()

    c.showPage()
    c.save()
    return out_file_path


# 给每一页Pdf加水印
def add_watermark(watermark_file_obj, page_obj):
    # 创建pdfReader对象，把打开的水印pdf传入
    pdf_reader = PdfFileReader(watermark_file_obj)

    # 将水印pdf的首页与传入的原始pdf的页进行合并
    page_obj.mergePage(pdf_reader.getPage(0))
    page_obj.compressContentStreams()

    return page_obj


def get_export_data(_type, all_id, start, end, user_id, role_id):
    list_data = [["排名", NAME_MAP[_type], NAME_MAP["efficiency"], NAME_MAP["accuracy"], NAME_MAP["workhour"]]]
    # 拿到当前用户能拿到的，经过"all_id"过滤的所有数据
    middle_query_set = get_filtered_query_set(_type, all_id, start, end, user_id, role_id)
    if middle_query_set is not None:  # 对当前用户能拿到的所有数据求平均并排序
        daily_query_set = middle_query_set.values(f"{_type}_id") \
            .annotate(Avg("efficiency"), Avg("accuracy"), Avg("workhour")) \
            .order_by("-efficiency__avg")
        for i, one_model_dic in enumerate(daily_query_set):
            new_list = [
                i + 1,
                one_model_dic[f"{_type}_id"],
                one_model_dic["efficiency__avg"],
                one_model_dic["accuracy__avg"],
                one_model_dic["workhour__avg"]
            ]
            list_data.append(new_list)
    return list_data


def get_all_worker_id(worker_team_group_workshop_query_set):
    all_worker_id = []
    for one_tuple in worker_team_group_workshop_query_set:
        for one_worker_id in one_tuple:
            all_worker_id.append(one_worker_id)

    return all_worker_id


def get_filtered_query_set(_type, all_id, start, end, user_id, role_id):
    query_set = globals()[f"Dms{_type.title()}Daily"].objects.filter(time__gte=start, time__lte=end)
    # all_id的值有两种情况
    if all_id == ["all"]:  # 将["all"]转换为当前用户有权限能拿到的所有_type下的id
        if role_id == 4:  # 总经理
            return query_set
        if role_id == 3:  # 经理
            # 查询经理管理的是哪个车间
            user_managed_struct_id = Workshop.objects.filter(employee_id=user_id)[0].id
            # 查询这个车间下所有的_type，拿到所有id
            cur_user_team_group_workshop_query_set = TeamGroupWorkshop.objects \
                .filter(workshop_id=user_managed_struct_id).values(_type + "_id").distinct()
            all_id = []
            for item in cur_user_team_group_workshop_query_set:
                all_id.append(item[_type + "_id"])
        else:  # 大组长
            # 查询大组长管理的是哪个车间
            user_managed_struct_id = Group.objects.filter(employee_id=user_id)[0].id
            # 查询这个大组下所有的_type，拿到所有id
            cur_user_team_group_workshop_query_set = TeamGroupWorkshop.objects \
                .filter(group_id=user_managed_struct_id).values(_type + "_id").distinct()
            all_id = []
            for item in cur_user_team_group_workshop_query_set:
                all_id.append(item[_type + "_id"])
    # 再在all_id范围内查询所有数据
    if _type == "workshop":
        return query_set.filter(workershop_id__in=all_id)
    elif _type == "group":
        return query_set.filter(group_id__in=all_id)
    elif _type == "team":
        return query_set.filter(team_id__in=all_id)


def get_worker_export_data(all_id, start, end, user_id, role_id):
    """
    all_id: "1，2，3" 这样的序号或者"all"
    list格式数据：[[第0个是需插入的表头], [后面就是相对应的数据], .......]
    :return: 
    """""
    # 先定义好表头
    # 表头：team_id, worker_id, name, efficiency, accuracy, workhour,
    list_data = []
    list_data.append(["排名", NAME_MAP["team_id"], NAME_MAP["worker_id"], NAME_MAP["name"],
                      NAME_MAP["efficiency"], NAME_MAP["accuracy"], NAME_MAP["workhour"]])
    worker_team_group_workshop_query_set = get_worker_team_group_workshop(user_id, role_id)
    temp_all_id = []
    worker_team_dict = {}
    for one_query_set in worker_team_group_workshop_query_set:
        if all_id == ["all"]:  # 将["all"]转换成当前用户所管理的所有worker_id
            temp_all_id.append(one_query_set[0])
            temp_all_id.append(one_query_set[1])
            temp_all_id.append(one_query_set[2])
        worker_team_dict[one_query_set[0]] = one_query_set[3]
        worker_team_dict[one_query_set[1]] = one_query_set[3]
        worker_team_dict[one_query_set[2]] = one_query_set[3]
    if all_id == ["all"]:
        all_id = temp_all_id
    worker_member_dict = get_worker_member_dict(all_id)
    # 查询出所有worker的平均效率并排名
    worker_daily_query_set = DmsWorkerDaily.objects \
        .filter(worker_id__in=all_id, time__gte=start, time__lte=end) \
        .values("worker_id") \
        .annotate(Avg("efficiency"), Avg("accuracy"), Avg("workhour")) \
        .order_by("-efficiency__avg", "-worker_id")
    # 循环添加最终的数据
    i = 0
    for one_worker_daily in worker_daily_query_set:
        worker_id = one_worker_daily["worker_id"]
        list_data.append([
            i + 1,
            worker_team_dict[worker_id],
            worker_id,
            worker_member_dict[worker_id][0],
            one_worker_daily["efficiency__avg"],
            one_worker_daily["accuracy__avg"],
            one_worker_daily["workhour__avg"]
        ])
        i += 1

    return list_data
