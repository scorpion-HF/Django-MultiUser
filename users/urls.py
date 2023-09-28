from django.urls import path

from users.views import NormalUserSignUpView, SupervisorSignUpView, ProfileView, LoginUserView

urlpatterns = [
    path('accounts/login/', LoginUserView.as_view(), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('accounts/signup/normal/', NormalUserSignUpView.as_view(), name='normal-signup'),
    path('accounts/signup/supervisor/', SupervisorSignUpView.as_view(), name='supervisor-signup'),
]
