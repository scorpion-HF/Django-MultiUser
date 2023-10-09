from django.contrib.auth import get_user_model
from users.models import CustomUser, SupervisorProfile, NormalProfile
from rest_framework import generics
from users.serializers import NormalUserCreateSerializer, NormalUserSerializer, \
    SupervisorCreateSerializer, SupervisorSerializer
from users.permissions import IsSupervisor
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class NormalUserCreateAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = NormalUserCreateSerializer
    permission_classes = [IsSupervisor]

    def perform_create(self, serializer):
        usr = get_user_model().objects.create_user(email=serializer.validated_data['email'],
                                                   password=serializer.validated_data['password'],
                                                   is_normal=True)
        usr.save()
        profile = NormalProfile.objects.create(normal_user_id=serializer.validated_data['normal_user_id'], user=usr)
        profile.save()


class SupervisorCreateAPI(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = SupervisorCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        usr = get_user_model().objects.create_user(email=serializer.validated_date['email'],
                                                   password=serializer.validated_date['password'],
                                                   is_superuser=True)
        usr.save()
        profile = SupervisorProfile.objects.create(supervisor_id=serializer.validated_date['supervisor_id'], user=usr)
        profile.save()


class UserProfileAPI(generics.RetrieveAPIView):

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.user.is_supervisor:
            return SupervisorSerializer
        elif self.request.user.is_normal:
            return NormalUserSerializer
