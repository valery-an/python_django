from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from app_users.models import CustomUser


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-input'
            field.field.widget.attrs['data-validate'] = 'require'


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label='ФИО')
    email = forms.CharField(
        required=True,
        label='E-mail',
        error_messages={'unique': 'Пользователь с таким e-mail уже существует'}
    )
    phone_number = forms.CharField(
        required=True,
        label='Телефон',
        error_messages={'max_length': '',
                        'unique': 'Пользователь с таким номером телефона уже существует'}
    )
    avatar = forms.ImageField(required=False, label='Аватар')

    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'phone_number', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-input'
            if field.field.required:
                field.field.widget.attrs['data-validate'] = 'require'
        self.fields['email'].widget.attrs['placeholder'] = 'send@test.test'
        self.fields['phone_number'].widget.attrs['placeholder'] = '+70000000000'

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.startswith('+7'):
            raise ValidationError('Номер телефона должен начинаться с +7')
        if not phone_number[1:].isdigit():
            raise ValidationError('Номер телефона должен состоять из цифр')
        if len(phone_number) != 12:
            raise ValidationError('Номер телефона должен состоять из 10 цифр')
        return phone_number


class RegisterForm(ProfileForm, UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'email', 'phone_number', 'password1', 'password2', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Введите пароль повторно'


class PasswordEditForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Пароль',
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Тут можно изменить пароль',
                                          'class': 'form-input'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        required=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password',
                                          'placeholder': 'Введите пароль повторно',
                                          'class': 'form-input'}),
    )
