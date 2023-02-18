from rest_framework import serializers
from users.models import User


class UserAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )


class UserNoAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role"
        )
        read_only_fields = ("role",)


class RegestrationTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True)
    confirmation_code = serializers.CharField(
        required=True)

    class Meta:
        model = User
        fields = ("username", "confirmation_code",)


class SignUpUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email", "username",)
