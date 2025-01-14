from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect

from app_orders.models import Order
from app_users.forms import LoginForm, ProfileForm, RegisterForm, PasswordEditForm


class UserLoginView(LoginView):
    """
    Страница авторизации пользователя.

    **Context**

    ``form``: Форма аутентификации модели пользователя :model:`app_users.CustomUser`

    **Template:**

    :template:`users/login.html`
    """
    template_name = 'users/login.html'
    form_class = LoginForm


class UserLogoutView(LogoutView):
    """
    Страница выхода пользователя из системы.

    **Template:**

    :template:`users/logout.html`
    """
    template_name = 'users/logout.html'


def register_view(request):
    """
    Страница регистрации пользователя.

    **Context**

    ``form``: Форма регистрации модели пользователя :model:`app_users.CustomUser`

    **Template:**

    :template:`users/register.html`
    """
    if request.method == 'POST':
        register_form = RegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            register_form.save()
            email = register_form.cleaned_data.get('email')
            raw_password = register_form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            return redirect('account')
        else:
            for field in register_form.errors:
                register_form[field].field.widget.attrs['class'] += ' form-input_error'
    else:
        register_form = RegisterForm()
    return render(request, 'users/register.html', context={'form': register_form})


@login_required
def account_view(request):
    """
    Страница личного кабинета пользователя.

    **Context**

    - ``user``: Экземпляр модели пользователя :model:`app_users.CustomUser`
    - ``order``: Экземпляр модели заказа :model:`app_orders.Order`

    **Template:**

    :template:`users/account.html`
    """
    order = Order.objects.filter(user=request.user).first()
    return render(request, 'users/account.html', context={'user': request.user, 'order': order})


@login_required
def profile_view(request):
    """
    Страница редактирования профиля пользователя.

    **Context**

    - ``profile_form``: Форма профиля модели пользователя :model:`app_users.CustomUser`
    - ``password_form``: Форма изменения пароля модели пользователя :model:`app_users.CustomUser`

    **Template:**

    :template:`users/profile.html`
    """
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user)
        password_form = PasswordEditForm(request.user, request.POST)
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Профиль успешно сохранен')
            if new_password1 or new_password2:
                if password_form.is_valid():
                    password_form.save()
                    messages.success(request, 'Пароль успешно изменён')
                    email = profile_form.cleaned_data.get('email')
                    raw_password = password_form.cleaned_data.get('new_password1')
                    user = authenticate(email=email, password=raw_password)
                    login(request, user)
                    return redirect('profile')
                else:
                    for field in password_form.errors:
                        password_form[field].field.widget.attrs['class'] += ' form-input_error'
            else:
                return redirect('profile')
        else:
            for field in profile_form.errors:
                profile_form[field].field.widget.attrs['class'] += ' form-input_error'
    else:
        profile_form = ProfileForm(instance=request.user)
        password_form = PasswordEditForm(user=request.user)
    context = {'profile_form': profile_form, 'password_form': password_form}
    return render(request, 'users/profile.html', context=context)
