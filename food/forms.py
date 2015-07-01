# -*- coding: utf-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from member.models import UserProfile
from food.models import Snack


class TokenCheckForm(forms.Form):
    token = forms.CharField(label='token')
    user = None

    def clean_token(self):
        token = self.cleaned_data['token']
        try:
            up = UserProfile.objects.get(token=token)
        except UserProfile.DoesNotExist:
            raise ValidationError(u'없는 유저 입니다.')
        else:
            self.user = up.user
            return token

    def get_user(self):
        return self.user


class ListIndexCheckForm(forms.Form):
    token = forms.CharField(label='token')
    index = forms.IntegerField(label='index')
    user = None

    def clean(self):
        token = self.cleaned_data['token']

        try:
            up = UserProfile.objects.get(token=token)
        except UserProfile.DoesNotExist:
            raise ValidationError(u'없는 유저 입니다.')
        else:
            self.user = up.user
            return self.cleaned_data

    def get_user(self):
        return self.user


class SnackIdCheckForm(forms.Form):
    token = forms.CharField(label='token')
    snackId = forms.IntegerField(label='snackId')
    user = None
    snack = None

    def clean(self):
        token = self.cleaned_data['token']
        snack_id = self.cleaned_data['snackId']

        try:
            up = UserProfile.objects.get(token=token)
        except UserProfile.DoesNotExist:
            raise ValidationError(u'없는 유저 입니다.')
        else:
            try:
                snack = Snack.objects.get(id=snack_id)
            except Snack.DoesNotExist:
                raise ValidationError(u'존재하지 않는 식품입니다.')
            else:
                self.user = up.user
                self.snack = snack
            return self.cleaned_data

    def get_user(self):
        return self.user

    def get_snack(self):
        return self.snack

