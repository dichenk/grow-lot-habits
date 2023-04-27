from rest_framework import serializers
from app_custom_user.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
                'id',
                'email',
                'password',
                )
