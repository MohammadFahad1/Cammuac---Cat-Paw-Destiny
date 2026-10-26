from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'status', 'created_at', 'updated_at']
        extra_kwargs = {
            'email': {'validators': []},
            'status': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def validate_email(self, value):
        email = value.lower().strip()
        user = User.objects.filter(email=email).first()
        if user and (user.status != User.INACTIVE and user.is_active):
            raise serializers.ValidationError("A user with this email already exists.")
        return email

    def validate_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        email = self.validated_data.get('email')
        existing_user = User.objects.filter(email=email).first()

        validated_data = {**self.validated_data, **kwargs}
        password = validated_data.pop('password', None)

        if existing_user and (existing_user.status == User.INACTIVE or not existing_user.is_active):
            for attr, val in validated_data.items():
                setattr(existing_user, attr, val)
            if password:
                existing_user.set_password(password)
            existing_user.save()
            self.instance = existing_user
            return existing_user
        else:
            if password:
                validated_data['password'] = password
            user = User.objects.create_user(**validated_data)
            self.instance = user
            return user


class EmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, min_length=6, required=True)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmptySerializer(serializers.Serializer):
    pass


class EmailPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reset_token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'status', 'is_active', 'is_staff', 'is_superuser', 'created_at', 'updated_at']
        read_only_fields = fields
