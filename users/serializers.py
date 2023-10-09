from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from users.models import CustomUser, NormalProfile, SupervisorProfile


class NormalUserCreateSerializer(ModelSerializer):
    normal_user_id = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'is_staff', 'password', 'normal_user_id']


class SupervisorCreateSerializer(ModelSerializer):
    supervisor_id = serializers.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'is_staff', 'password', 'supervisor_id']


class NormalProfileSerializer(ModelSerializer):
    class Meta:
        model = NormalProfile
        fields = ['normal_user_id']


class SupervisorProfileSerializer(ModelSerializer):
    class Meta:
        model = SupervisorProfile
        fields = ['supervisor_id']


class NormalUserSerializer(ModelSerializer):
    profile = NormalProfileSerializer(source='normal_profile')

    class Meta:
        model = CustomUser
        fields = ['email', 'date_joined', 'profile']


class SupervisorSerializer(ModelSerializer):
    profile = SupervisorProfileSerializer(source='supervisor_profile')

    class Meta:
        model = CustomUser
        fields = ['email', 'date_joined', 'profile']
