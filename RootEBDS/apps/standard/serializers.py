# coding: utf-8


from .models import StandardTeam, StandardGroup, StandardWorkshop, StandardDpt
from utils.person_serializers import StandardSerializer


class StandardTeamSerializer(StandardSerializer):

    class Meta:
        model = StandardTeam
        fields = "__all__"


class StandardGroupSerializer(StandardSerializer):

    class Meta:
        model = StandardGroup
        fields = "__all__"


class StandardWorkshopSerializer(StandardSerializer):

    class Meta:
        model = StandardWorkshop
        fields = "__all__"


class StandardDptSerializer(StandardSerializer):

    class Meta:
        model = StandardDpt
        fields = "__all__"

