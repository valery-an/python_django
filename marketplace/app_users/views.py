from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from app_users.forms import LoginForm, ProfileForm, RegisterForm, PasswordEditForm


class UserLoginView(LoginView):
    """ Страница авторизации пользователя """
    template_name = 'users/login.html'
    form_class = LoginForm


class UserLogoutView(LogoutView):
    """ Выход пользователя из системы """
    template_name = 'users/logout.html'


def register_view(request):
    """ Страница регистрации пользователя """
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            email = register_form.cleaned_data.get('email')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('main')
        else:
            for field in register_form.errors:
                register_form[field].field.widget.attrs['class'] += ' form-input_error'
    else:
        register_form = RegisterForm()
    return render(request, 'users/register.html', context={'form': register_form})


@login_required
def account_view(request):
    """ Страница личного кабинета пользователя """
    return render(request, 'users/account.html', context={'user': request.user})


@login_required
def profile_view(request):
    """ Страница редактирования профиля пользователя """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordEditForm(request.user, request.POST)
        if profile_form.is_valid() and password_form.is_valid():
            profile_form.save()
            password_form.save()
            messages.success(request, 'Профиль успешно сохранен')
            return redirect('profile')
        else:
            for field in profile_form.errors:
                profile_form[field].field.widget.attrs['class'] += ' form-input_error'
            for field in password_form.errors:
                password_form[field].field.widget.attrs['class'] += ' form-input_error'
    else:
        profile_form = ProfileForm(instance=request.user)
        password_form = PasswordEditForm(user=request.user)
    context = {'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'users/profile.html', context=context)
