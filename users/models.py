from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    username = models.CharField(max_length=200, verbose_name='Username', null=False, blank=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    job = models.CharField(max_length=200, verbose_name='Job', null=True, blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email', null=True, blank=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username
