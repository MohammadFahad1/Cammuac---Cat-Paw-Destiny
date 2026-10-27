from rest_framework import serializers
from .models import CatTarotDraw

WEEKDAY_ZH_MAP = {
    0: "星期一",
    1: "星期二",
    2: "星期三",
    3: "星期四",
    4: "星期五",
    5: "星期六",
    6: "星期日",
}


class CatTarotDrawInputSerializer(serializers.Serializer):
    card_number = serializers.IntegerField(
        min_value=1,
        max_value=3,
        required=True,
        help_text="Selected card number (1, 2, or 3)"
    )


class CatTarotDrawSerializer(serializers.ModelSerializer):
    day = serializers.SerializerMethodField()
    month_year = serializers.SerializerMethodField()
    weekday_en = serializers.SerializerMethodField()
    weekday_zh = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    tag = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()

    class Meta:
        model = CatTarotDraw
        fields = [
            'id',
            'card_number',
            'date',
            'day',
            'month_year',
            'weekday_en',
            'weekday_zh',
            'category',
            'tag',
            'title',
            'content',
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

    def get_category(self, obj) -> dict:
        return {
            "en": obj.category_en,
            "zh": obj.category_zh,
        }

    def get_tag(self, obj) -> dict:
        return {
            "en": obj.category_en,
            "zh": obj.category_zh,
        }

    def get_title(self, obj) -> dict:
        return {
            "en": obj.title_en,
            "zh": obj.title_zh,
        }

    def get_content(self, obj) -> dict:
        return {
            "en": obj.content_en,
            "zh": obj.content_zh,
        }

