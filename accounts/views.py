from django.contrib.auth.models import User, Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'
    template_name = 'registration/signup.html'


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля (только для авторизованных)"""
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile_edit')

    def get_object(self, queryset=None):
        return self.request.user


class UpgradeToAuthor(LoginRequiredMixin, View):
    """Добавление пользователя в группу authors"""
    def get(self, request):
        authors_group = Group.objects.get(name='authors')
        request.user.groups.add(authors_group)
        messages.success(request, 'Поздравляем! Теперь вы автор и можете публиковать новости.')
        return redirect('post_list')