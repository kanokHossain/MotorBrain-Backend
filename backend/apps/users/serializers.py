from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserSubscription


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "password_confirm"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = User.objects.create_user(**validated_data)
        UserSubscription.objects.create(user=user)
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    subscription_plan = serializers.CharField(source="subscription.plan", read_only=True)
    is_premium = serializers.BooleanField(source="subscription.is_premium", read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "first_name", "last_name", "phone_number",
            "avatar", "is_verified", "date_joined", "subscription_plan", "is_premium",
        ]
        read_only_fields = ["id", "email", "is_verified", "date_joined"]


class FCMTokenSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(max_length=500)

    def update(self, instance, validated_data):
        instance.fcm_token = validated_data["fcm_token"]
        instance.save(update_fields=["fcm_token"])
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect current password.")
        return value
