# coding: utf-8

from collections import OrderedDict
from ..models import DmsTeamOnline, DmsGroupOnline, DmsWorkshopOnline, DmsDptOnline, DmsStatOnline
from sms.models import TeamStatMember, Member
from cfg.models import CfgWorkPeriod
from utils.person_serializers import OnlineSerializer, DmsListSerializer


class OnlineListSerializer(DmsListSerializer):
    """
    重写Online序列化格式
    """

    def to_representation(self, data) -> list:
        response = super().to_representation(data)
        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')
        req_id = self.context['request'].query_params.get('id')
        if sms_type == 'stat':
            # 获取worker+period信息
            worker_list = []
            stat_obj = TeamStatMember.objects.filter(
                stat_id=req_id).order_by('-update_time')[0]
            for period in CfgWorkPeriod.objects.all():
                worker_dict = OrderedDict()
                worker_dict['worker_id'] = getattr(
                    stat_obj, f"{period.name}_shift_id")
                worker_dict['name'] = Member.objects.get(
                    employee_id=worker_dict['worker_id']).name
                worker_dict['period'] = [period.start_time, period.end_time]
                worker_list.append(worker_dict)

            # 更新response
            response[0]['worker'] = worker_list
            response[0].move_to_end(metric)
        return response


class DmsTeamOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsTeamOnline
        list_serializer_class = OnlineListSerializer
        fields = ('team_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsGroupOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsGroupOnline
        list_serializer_class = OnlineListSerializer
        fields = ('group_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkshopOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsWorkshopOnline
        list_serializer_class = OnlineListSerializer
        fields = ('workshop_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsDptOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsDptOnline
        list_serializer_class = OnlineListSerializer
        fields = ('dpt_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsStatOnlineSerializer(OnlineSerializer):

    class Meta:
        model = DmsStatOnline
        list_serializer_class = OnlineListSerializer
        fields = ('stat_id', 'efficiency', 'accuracy', 'workhour', 'time')

