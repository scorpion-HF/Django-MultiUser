from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from users.permissions import SupervisorRequiredMixin, SuperUserRequiredMixin
from users.forms import SupervisorSignUpForm, NormalUserSignUpForm
from users.models import CustomUser, SupervisorProfile, NormalProfile


class LoginUserView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse('profile')


class ProfileView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'demonstrate/profile.html'

    def get_login_url(self):
        return reverse('login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_supervisor:
            context['profile'] = SupervisorProfile.objects.get(user=self.request.user)
            return context
        if self.request.user.is_normal:
            context['profile'] = NormalProfile.objects.get(user=self.request.user)
            return context


class SupervisorSignUpView(SuperUserRequiredMixin, CreateView):
    model = CustomUser
    form_class = SupervisorSignUpForm
    template_name = 'registration/supervisor_signup_form.html'
    permission_required = 'users.create_normal_profile'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'supervisor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect(reverse('supervisor-signup'))


class NormalUserSignUpView(SupervisorRequiredMixin, CreateView):
    model = CustomUser
    form_class = NormalUserSignUpForm
    template_name = 'registration/normal_user_signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'normal'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect(reverse('normal-signup'))
