from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    '''Расширенная пользовательская модель.'''

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name', )
    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        max_length=254
    )
    first_name = models.CharField(
        'Имя',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )

    class Meta:
        ordering = [('pk')]
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.username} - {self.first_name} {self.last_name}'
