import string
import random

from django.db import models
from django.contrib.auth.models import User


def create_user_with_random_username(email='', password=None):
    def generate_username_and_password():
        _LOWERCASE = ''.join(string.ascii_lowercase)
        _ALPHA_DIGIT = ''.join(
            [string.ascii_lowercase, string.ascii_uppercase, string.digits])
        USERNAME_LENGTH = 8
        PASSWORD_LENGTH = 10

        return ''.join([''.join(random.sample(_LOWERCASE, 1)),
                        ''.join(random.sample(_ALPHA_DIGIT, USERNAME_LENGTH - 1))]),\
               ''.join([''.join(random.sample(_LOWERCASE, 1)),
                        ''.join(random.sample(_ALPHA_DIGIT, PASSWORD_LENGTH - 1))])

    while True:
        username, random_password = generate_username_and_password()
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            password = password or random_password
            user = User.objects.create_user(username=username, password=password, email=email)
            break
    return user


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user = models.ForeignKey(User, unique=True)
    birthday = models.DateField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    token = models.CharField(max_length=40)

    def __str__(self):
        return self.user.email.encode('utf8')

    def to_dict(self):
        birthday = self.birthday.strftime('%Y-%m-%d')
        return dict(id=self.user.id, email=self.user.email, birthday=birthday, gender=self.gender,
                    token=self.token)

    @classmethod
    def get_user(cls, token):
        try:
            return cls.objects.get(token=token).user
        except UserProfile.DoesNotExist:
            return None
