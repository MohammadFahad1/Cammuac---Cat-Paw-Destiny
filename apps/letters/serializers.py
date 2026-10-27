from rest_framework import serializers
from .models import Letter, LetterStatus


STATUS_BILINGUAL_MAP = {
    LetterStatus.PENDING: {"en": "Pending", "zh": "待開啟"},
    LetterStatus.OPENED: {"en": "Opened", "zh": "已開啟"},
}


class LetterSerializer(serializers.ModelSerializer):
    status_display = serializers.SerializerMethodField()
    is_opened = serializers.SerializerMethodField()
    formatted_date_zh = serializers.SerializerMethodField()
    formatted_date_en = serializers.SerializerMethodField()
    content_length = serializers.SerializerMethodField()

    class Meta:
        model = Letter
        fields = [
            'id',
            'sticker',
            'title',
            'content',
            'status',
            'status_display',
            'is_opened',
            'date',
            'formatted_date_zh',
            'formatted_date_en',
            'content_length',
            'opened_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = fields

    def get_status_display(self, obj) -> dict:
        return STATUS_BILINGUAL_MAP.get(obj.status, {"en": obj.status, "zh": obj.status})

    def get_is_opened(self, obj) -> bool:
        return obj.status == LetterStatus.OPENED

    def get_formatted_date_zh(self, obj) -> str:
        return f"{obj.date.year}年{obj.date.month}月{obj.date.day}日"

    def get_formatted_date_en(self, obj) -> str:
        return obj.date.strftime("%B %d, %Y")

    def get_content_length(self, obj) -> int:
        return len(obj.content) if obj.content else 0


class LetterCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Letter
        fields = ['sticker', 'title', 'content']
        extra_kwargs = {
            'sticker': {'required': False, 'allow_blank': True, 'default': 'heart'},
            'title': {'required': False, 'allow_blank': True},
            'content': {'required': True, 'min_length': 1, 'max_length': 2000},
        }


class LetterUpdateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=LetterStatus.choices,
        required=False,
        help_text="Status of the letter: 'pending' (待開啟) or 'opened' (已開啟)"
    )

    class Meta:
        model = Letter
        fields = ['sticker', 'title', 'content', 'status']
        extra_kwargs = {
            'sticker': {'required': False, 'allow_blank': True},
            'title': {'required': False, 'allow_blank': True},
            'content': {'required': False, 'min_length': 1, 'max_length': 2000},
            'status': {'required': False},
        }


# Backward-compatibility alias
LetterCreateUpdateSerializer = LetterCreateSerializer


