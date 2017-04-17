import random
import string
import django.contrib.auth.models
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password, \
    password_validators_help_text_html
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.utils.translation import ugettext as _


class SignupForm(ModelForm):
    verify_password = forms.CharField(label="Type your password to verify ", widget=forms.PasswordInput(),
                                      max_length=100)

    class Meta:
        model = django.contrib.auth.models.User
        fields = ['username', 'password', 'verify_password', 'email']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        # rewriting clean method to check whether passwords match or not
        cleaned_data = super(SignupForm, self).clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        ps1 = cleaned_data.get('password')
        ps2 = cleaned_data.get('verify_password')
        if email == "":
            self.add_error('email', "Please input your email!")
        if ps1 != ps2:
            msg = _("Пароль не совпадает!")
            self.add_error('verify_password', msg)
        # Save hashed password instead of password directly
        encoded_password = make_password(ps1, make_salt())
        cleaned_data['password'] = encoded_password
        # Make sure email is unique
        if email and django.contrib.auth.models.User.objects.filter(email=email).exclude(username=username).count():
            msg = _("Такой Email уже зарегистрирован!")
            self.add_error('email', msg)
        if ps1:
            try:
                validate_password(ps1, user=self)
                cleaned_data['help_text'] = None
            except ValidationError:
                cleaned_data['help_text'] = password_validators_help_text_html()
                self.add_error('password', 'Your password it too weak. Please choose another password')
        return cleaned_data


class SigninForm(forms.Form):
    username = forms.CharField(label="User name ", required=False, max_length=100)
    email = forms.EmailField(label="Your email ", required=False, max_length=100)
    password = forms.CharField(label="Password ", widget=forms.PasswordInput(), max_length=100)

    def clean(self):
        cleaned_data = super(SigninForm, self).clean()
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        if not (username or email):
            msg = _("Пожалуйста, введите ваше имя пользователя или адрес электронной почты!")
            self.add_error('username', msg)
        if username:
            if django.contrib.auth.models.User.objects.filter(username=username).count() == 0:
                msg = _("Имя пользователя не существует!")
                self.add_error('username', msg)
            elif not authenticate(username=username, password=password):
                msg = _("Имя пользователя и пароль не совпадают!")
                self.add_error('password', msg)
        else:
            if django.contrib.auth.models.User.objects.filter(email=email).count() == 0:
                msg = _("Электронной почты не существует!")
                self.add_error('email', msg)
            elif not authenticate(username=email, password=password):
                msg = _("Электронная почта и пароль не совпадают!")
                self.add_error('password', msg)
        return cleaned_data


def make_salt():
    letters = string.ascii_letters
    result = random.sample(letters, 5)
    return ''.join(result)
