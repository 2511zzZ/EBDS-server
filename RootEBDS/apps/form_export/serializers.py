import os
import datetime
from rest_framework import serializers
from core.choices import FORM_TYPE_CHOICES, FORM_EXPORT_CHOICES
from utils.form_export.export_methods import create_efficiency_rank_xlsx, \
    create_efficiency_rank_pdf, create_alert_rank_xlsx, create_alert_rank_pdf
from EBDS.settings import FORM_FILE_PATH
from core.name_map import NAME_MAP


class FormSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=FORM_TYPE_CHOICES)
    all_id = serializers.RegexField(required=False, regex=r'^(\d+,)+\d+$|^\d+$|^all$')  # 匹配形如1,2或者正整数或者all
    start = serializers.DateField(required=False)
    end = serializers.DateField(required=False)
    file_type = serializers.ChoiceField(choices=FORM_EXPORT_CHOICES)
    password = serializers.CharField(max_length=12, min_length=3, required=False, trim_whitespace=True)

    class Meta:
        fields = ("type", "all_id", "start", "end", "file_type", "password")

    def validate(self, attrs):
        """
        对象级别的验证器
        如果_type是alert, 则不能提供all_id, start, end参数
        否则全部必须提供
        :param attrs: 经过序列化字段校验的数据
        :return: 被验证后的数据
        """
        if attrs["type"] == "alert":
            if "all_id" in attrs or "start" in attrs or "end" in attrs:
                raise serializers.ValidationError("alert类型不支持all_id, start或者end")
        else:
            if "all_id" not in attrs or "start" not in attrs or "end" not in attrs:
                raise serializers.ValidationError("非alert类型必填all_id, start和end")
        return attrs

    def create(self, validated_data):

        watermark_text = "流水线员工行为AI检测系统"

        _type = validated_data["type"]
        all_id = None
        start = None
        end = None
        if _type != "alert":
            # 适配数据格式(time->str, all_id->list)
            all_id = validated_data["all_id"].split(',')
            all_id.sort()
            start = validated_data["start"]
            end = validated_data["end"]
        user_id = self.context["request"].user.employee_id
        role_id = self.context["request"].user.groups.all()[0].id
        file_type = validated_data["file_type"]
        try:
            password = validated_data["password"]
        except KeyError:
            password = None

        file_name = self.get_file_name(_type, start, end, user_id, all_id, file_type, password)
        local_path = os.path.join(os.path.abspath("."), FORM_FILE_PATH, file_name)
        if _type == "alert":
            now_date = datetime.datetime.now().date()
            last_month = now_date - datetime.timedelta(days=31)
            start = datetime.datetime(year=last_month.year, month=last_month.month, day=1)
            end = start + datetime.timedelta(days=30)
            if file_type == "excel":
                create_alert_rank_xlsx(local_path, start, end)
            else:
                create_alert_rank_pdf(local_path, start, end, password)
        else:  # 导出效率相关文件
            # 如果文件已存在且请求的是all
            if all_id != ["all"] or not os.path.exists(local_path) or password is not None:
                if file_type == "excel":
                    create_efficiency_rank_xlsx(local_path, _type, all_id, start, end, user_id, role_id)
                else:
                    create_efficiency_rank_pdf(local_path, _type, all_id, start, end, watermark_text, user_id, role_id,
                                               password)

        url = "http://" + self.context["request"].META["HTTP_HOST"] \
              + '/' + os.path.join("media", "form_file", file_name).replace('\\', '/')

        return {"url": url}

    def get_file_name(self, _type, start, end, user_id, all_id, file_type, password):
        cur_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")[2:]
        # 例如：报表2019-8-1_2020-1-1_员工_(导出人:3)管辖所有
        file_name = "报表_"
        if _type != "alert":
            start = datetime.datetime.strftime(start, "%Y-%m-%d")[2:]
            end = datetime.datetime.strftime(end, "%Y-%m-%d")[2:]
            file_name += start + '_' + end + "_"
        file_name += NAME_MAP[_type] + "(导出人" + str(user_id) + ")" + cur_time
        # 如果要导出的是all，则先看有没有之前的文件
        if all_id is not None and all_id == ["all"]:
            file_name += "管辖所有"
        if password is not None:
            file_name += "(加密)"
        if file_type == "excel":
            file_name += ".xlsx"
        else:
            file_name += ".pdf"

        return file_name
