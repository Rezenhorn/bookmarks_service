from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .managers import EmailUserManager


class User(AbstractUser):
    """Кастомная модель юзера."""
    username = models.CharField(
        'username',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
        blank=True,
        null=True,
        help_text=(
            '150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            'unique': 'A user with that username already exists.',
        },
    )
    email = models.EmailField(
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
    )

    objects = EmailUserManager()

    REQUIRED_FIELDS = ()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
