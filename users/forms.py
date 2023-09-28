from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from users.models import CustomUser, SupervisorProfile, NormalProfile


class SupervisorSignUpForm(UserCreationForm):
    supervisor_id = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supervisor = True
        user.is_normal = False
        user.save()
        profile = SupervisorProfile.objects.create(user=user)
        profile.supervisor_id = self.cleaned_data.get('supervisor_id')
        profile.save()
        return user


class NormalUserSignUpForm(UserCreationForm):
    normal_user_id = forms.CharField(max_length=30, required=True)

    class Meta:
        model = CustomUser
        fields = ('email',)

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_supervisor = False
        user.is_normal = True
        user.save()
        profile = NormalProfile.objects.create(user=user)
        profile.normal_user_id = self.cleaned_data.get('normal_user_id')
        profile.save()
        return user
