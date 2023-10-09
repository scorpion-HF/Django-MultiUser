from django.urls import path
from users.views import NormalUserCreateAPI, SupervisorCreateAPI, UserProfileAPI

urlpatterns = [
    path('accounts/signup/normal/', NormalUserCreateAPI.as_view(), name='normal-signup'),
    path('accounts/signup/supervisor/', SupervisorCreateAPI.as_view(), name='supervisor-signup'),
    path('accounts/profile/', UserProfileAPI.as_view(), name='profile'),

]
