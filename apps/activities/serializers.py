from rest_framework import serializers
from .models import DailyCheckIn, Alarm, DayStatus, get_day_status_payload, DayStatusType

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
    day_status = serializers.SerializerMethodField()

    class Meta:
        model = DailyCheckIn
        fields = [
            'id',
            'date',
            'day',
            'month_year',
            'weekday_en',
            'weekday_zh',
            'day_status',
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

    def get_day_status(self, obj) -> dict:
        day_status_obj = DayStatus.objects.filter(date=obj.date).first()
        status_key = day_status_obj.status if day_status_obj else getattr(obj, 'day_status', DayStatusType.NORMAL) or DayStatusType.NORMAL
        return get_day_status_payload(status_key)


# Backwards compatibility alias
DailyActivitySerializer = DailyCheckInSerializer


class AlarmSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    titleZh = serializers.CharField(source='title_zh')
    titleEn = serializers.CharField(source='title_en')
    iconEmoji = serializers.CharField(source='icon_emoji')
    bgColor = serializers.CharField(source='bg_color')
    borderColor = serializers.CharField(source='border_color')

    class Meta:
        model = Alarm
        fields = [
            'id',
            'time',
            'period',
            'titleZh',
            'titleEn',
            'repeat',
            'iconEmoji',
            'bgColor',
            'borderColor',
            'enabled',
        ]
        read_only_fields = ['id']

    def to_representation(self, instance):
        return {
            "id": str(instance.id),
            "time": instance.time,
            "period": instance.period,
            "titleZh": instance.title_zh,
            "titleEn": instance.title_en,
            "repeat": instance.repeat,
            "iconEmoji": instance.icon_emoji,
            "bgColor": instance.bg_color,
            "borderColor": instance.border_color,
            "enabled": instance.enabled,
        }


class AlarmCreateUpdateSerializer(serializers.ModelSerializer):
    titleZh = serializers.CharField(required=True, max_length=100, help_text="Chinese title, e.g. '起床囉！'")
    titleEn = serializers.CharField(required=True, max_length=100, help_text="English title, e.g. 'Wake Up!'")
    iconEmoji = serializers.CharField(required=False, default="🌅🐱", max_length=50, help_text="Icon and emoji, e.g. '🌅🐱'")
    bgColor = serializers.CharField(required=False, default="bg-pink-50", max_length=50, help_text="Tailwind bg class, e.g. 'bg-pink-50'")
    borderColor = serializers.CharField(required=False, default="border-pink-200", max_length=50, help_text="Tailwind border class, e.g. 'border-pink-200'")

    class Meta:
        model = Alarm
        fields = [
            'time',
            'period',
            'titleZh',
            'titleEn',
            'repeat',
            'iconEmoji',
            'bgColor',
            'borderColor',
            'enabled',
        ]
        extra_kwargs = {
            'time': {'required': True},
            'period': {'required': False, 'default': 'AM'},
            'repeat': {'required': False, 'default': '每天 Every day'},
            'enabled': {'required': False, 'default': True},
        }

    def to_internal_value(self, data):
        # Support both camelCase and snake_case in incoming request data
        normalized = data.copy() if hasattr(data, 'copy') else dict(data)
        mappings = {
            'title_zh': 'titleZh',
            'title_en': 'titleEn',
            'icon_emoji': 'iconEmoji',
            'bg_color': 'bgColor',
            'border_color': 'borderColor',
        }
        for snake, camel in mappings.items():
            if snake in normalized and camel not in normalized:
                normalized[camel] = normalized[snake]
        return super().to_internal_value(normalized)

    def create(self, validated_data):
        return Alarm.objects.create(
            user=self.context['request'].user,
            time=validated_data['time'],
            period=validated_data.get('period', 'AM'),
            title_zh=validated_data['titleZh'],
            title_en=validated_data['titleEn'],
            repeat=validated_data.get('repeat', '每天 Every day'),
            icon_emoji=validated_data.get('iconEmoji', '🌅🐱'),
            bg_color=validated_data.get('bgColor', 'bg-pink-50'),
            border_color=validated_data.get('borderColor', 'border-pink-200'),
            enabled=validated_data.get('enabled', True),
        )

    def update(self, instance, validated_data):
        if 'time' in validated_data:
            instance.time = validated_data['time']
        if 'period' in validated_data:
            instance.period = validated_data['period']
        if 'titleZh' in validated_data:
            instance.title_zh = validated_data['titleZh']
        if 'titleEn' in validated_data:
            instance.title_en = validated_data['titleEn']
        if 'repeat' in validated_data:
            instance.repeat = validated_data['repeat']
        if 'iconEmoji' in validated_data:
            instance.icon_emoji = validated_data['iconEmoji']
        if 'bgColor' in validated_data:
            instance.bg_color = validated_data['bgColor']
        if 'borderColor' in validated_data:
            instance.border_color = validated_data['borderColor']
        if 'enabled' in validated_data:
            instance.enabled = validated_data['enabled']
        instance.save()
        return instance

