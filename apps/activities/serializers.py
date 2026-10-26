from rest_framework import serializers
from .models import DailyCheckIn

WEEKDAY_ZH_MAP = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日",
}


class DailyCheckInSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    month_year = serializers.SerializerMethodField()
    weekday_en = serializers.SerializerMethodField()
    weekday_zh = serializers.SerializerMethodField()

    class Meta:
        model = DailyCheckIn
        fields = [
            'id',
            'date',
            'day',
            'month_year',
            'weekday_en',
            'weekday_zh',
            'good_for',
            'avoid',
            'quote',
            'lucky_color',
            'lucky_number',
            'lucky_direction',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_day(self, obj) -> int:
        return obj.date.day

    def get_month_year(self, obj) -> str:
        return obj.date.strftime("%b %Y")

    def get_weekday_en(self, obj) -> str:
        return obj.date.strftime("%a")

    def get_weekday_zh(self, obj) -> str:
        return WEEKDAY_ZH_MAP.get(obj.date.weekday(), "")


# Backwards compatibility alias
DailyActivitySerializer = DailyCheckInSerializer
