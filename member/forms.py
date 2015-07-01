# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class RegistrationForm(forms.Form):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    email = forms.EmailField(label=u'이메일')
    password = forms.CharField(label=u'비밀번호', widget=forms.PasswordInput(render_value=False))
    birthday = forms.DateField(input_formats=('%Y-%m-%d',))
    gender = forms.ChoiceField(label=u'성별', choices=GENDER_CHOICES)

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(u'이메일 형식이 아닙니다.')
            return email
        else:
            raise ValidationError(u'이미 가입한 이메일입니다.')


class AuthenticationForm(forms.Form):
    email = forms.CharField(label=u'이메일')
    password = forms.CharField(label=u'비밀번호', widget=forms.PasswordInput(render_value=False))

    def clean(self):
        try:
            user = authenticate(username=self.cleaned_data['email'], password=self.cleaned_data['password'])
            if user:
                self.user = user
            else:
                raise ValidationError(u'비밀번호가 틀렸습니다.')
        except User.DoesNotExist:
            raise ValidationError(u'존재하지 않는 이메일입니다.')
        return self.cleaned_data

    def get_user(self):
        return self.user




