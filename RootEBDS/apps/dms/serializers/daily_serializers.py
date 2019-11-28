# coding: utf-8
import datetime
from datetime import timedelta
from django.db.models import Q
from collections import OrderedDict
from sms.models import TeamStatMember, Member
from core.choices import DAY_PERIOD_CHOICES
from ..models import DmsTeamDaily, DmsGroupDaily, DmsWorkshopDaily, DmsDptDaily, \
    DmsStatDaily, DmsWorkerDaily
from utils.person_serializers import DailySerializer, DmsListSerializer


class DailyListSerializer(DmsListSerializer):
    """
    重写Daily序列化格式
    """

    def to_representation(self, data) -> list:
        response = super().to_representation(data)
        metric = self.context['request'].query_params.get('metric')  # 获取路径参数
        sms_type = self.context['request'].query_params.get('type')
        if sms_type == 'stat':
            # 更新response
            response[0]['changes'] = self.stat_data()
            response[0].move_to_end(metric)
        elif sms_type == 'worker':
            # 更新response
            name, changes_list = self.worker_data()
            response[0]['name'] = name
            response[0]['changes'] = changes_list
            response[0].move_to_end(metric)
        return response

    def stat_data(self):
        """
        获取工位的变更信息
        :return: changes_list 变更信息
        """
        req_id = self.context['request'].query_params.get('id')
        start = self.context['request'].query_params.get('start')
        end = self.context['request'].query_params.get('end')

        stat_time_list = [
            stat.update_time for stat in TeamStatMember.objects.filter(
                stat_id=req_id).filter(
                update_time__gte=start,
                update_time__lte=end).order_by('update_time')]
        start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()

        if not stat_time_list:
            stat_time_list.insert(0, start_date)
        elif start_date != stat_time_list[0]:  # 对start_date的变更特殊处理
            stat_time_list.insert(0, start_date)
        stat_time_list.insert(len(stat_time_list), end_date)
        # print(stat_time_list)

        changes_list = []  # 变更信息(用list模拟时间段)
        for index in range(len(stat_time_list) - 1):
            if index == 0:
                # 取离start_date最近的一条工位信息
                try:
                    stat = TeamStatMember.objects.filter(stat_id=req_id).filter(
                        update_time__lte=stat_time_list[0]).order_by('-update_time')[0]
                except IndexError:  # 没有的话说明start_date之前没有工位信息
                    continue
            else:
                stat = TeamStatMember.objects.filter(
                    stat_id=req_id).filter(
                    update_time=stat_time_list[index])[0]
            change_dict = OrderedDict()
            for day_period in ['morning', 'middle', 'night']:
                change_dict[f'{day_period}_shift_id'] = getattr(stat, f'{day_period}_shift_id')
                change_dict[f'{day_period}_shift_name'] = Member.objects.get(
                    employee_id=change_dict[f'{day_period}_shift_id']).name
            change_dict['period'] = [stat_time_list[index], stat_time_list[index + 1] - timedelta(days=1)]
            changes_list.append(change_dict)

        changes_list[-1]['period'][-1] += timedelta(days=1)  # 最后一个值特殊处理
        return changes_list

    def worker_data(self):
        """
        获取工人的变更信息
        :return: name 工人的名字, changes_list 变更信息
        """
        req_id = self.context['request'].query_params.get('id')
        start = self.context['request'].query_params.get('start')
        end = self.context['request'].query_params.get('end')

        # 获取工人名字
        name = Member.objects.get(employee_id=req_id).name

        stat_time_list = [stat.update_time for stat in TeamStatMember.objects.filter(
            update_time__gte=start,
            update_time__lte=end).filter(
            Q(morning_shift_id=req_id) |
            Q(middle_shift_id=req_id) |
            Q(night_shift_id=req_id)).order_by('update_time')]

        start_date = datetime.datetime.strptime(start, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end, '%Y-%m-%d').date()

        if not stat_time_list:
            stat_time_list.insert(0, start_date)
        elif start_date != stat_time_list[0]:  # 对start_date的变更特殊处理
            stat_time_list.insert(0, start_date)
        stat_time_list.insert(len(stat_time_list), end_date)
        # print(stat_time_list)

        changes_list = []  # 变更信息(用list模拟时间段)
        for index in range(len(stat_time_list) - 1):
            if index == 0:
                # 取离start_date最近的一条工位信息
                try:
                    stat = TeamStatMember.objects.filter(
                            Q(morning_shift_id=req_id) |
                            Q(middle_shift_id=req_id) |
                            Q(night_shift_id=req_id)).filter(
                            update_time__lte=stat_time_list[0]).order_by('-update_time')[0]
                except IndexError:  # 没有的话说明start_date之前没有工位信息
                    continue
            else:
                stat = TeamStatMember.objects.filter(
                            Q(morning_shift_id=req_id) |
                            Q(middle_shift_id=req_id) |
                            Q(night_shift_id=req_id)).filter(
                            update_time=stat_time_list[index])[0]
            change_dict = OrderedDict()
            change_dict["stat_id"] = stat.stat_id
            change_dict["team_id"] = stat.team_id
            for day_period in DAY_PERIOD_CHOICES:  # 获取worker所工作的时间段
                if int(req_id) == getattr(stat, f'{day_period[0]}_shift_id'):
                    change_dict["shift"] = day_period[1]
                    break
            change_dict['period'] = [stat_time_list[index], stat_time_list[index + 1] - timedelta(days=1)]
            changes_list.append(change_dict)

        changes_list[-1]['period'][-1] += timedelta(days=1)  # 最后一个值特殊处理
        return name, changes_list


class DmsTeamDailySerializer(DailySerializer):

    class Meta:
        model = DmsTeamDaily
        list_serializer_class = DailyListSerializer
        fields = ('team_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsGroupDailySerializer(DailySerializer):

    class Meta:
        model = DmsGroupDaily
        list_serializer_class = DailyListSerializer
        fields = ('group_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkshopDailySerializer(DailySerializer):

    class Meta:
        model = DmsWorkshopDaily
        list_serializer_class = DailyListSerializer
        fields = ('workshop_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsDptDailySerializer(DailySerializer):

    class Meta:
        model = DmsDptDaily
        list_serializer_class = DailyListSerializer
        fields = ('dpt_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsStatDailySerializer(DailySerializer):

    class Meta:
        model = DmsStatDaily
        list_serializer_class = DailyListSerializer
        fields = ('stat_id', 'efficiency', 'accuracy', 'workhour', 'time')


class DmsWorkerDailySerializer(DailySerializer):

    class Meta:
        model = DmsWorkerDaily
        list_serializer_class = DailyListSerializer
        fields = ('worker_id', 'efficiency', 'accuracy', 'workhour', 'time')
