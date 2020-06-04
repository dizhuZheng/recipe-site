from django.db import models
from django.contrib.auth.models import AbstractUser
import django.utils.timezone as timezone
from django.urls import reverse

class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    photo = models.ImageField(upload_to='images/', null=True, blank=True)
    username = models.CharField(max_length=200, verbose_name='Username', null=False, blank=False, unique=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Male')
    date_joined = models.DateTimeField(default=timezone.now)
    job = models.CharField(max_length=200, verbose_name='Job', null=True, blank=True)
    email = models.EmailField(max_length=150, verbose_name='Email', null=True, blank=True, unique=True)
    address = models.CharField(max_length=200, verbose_name='Address', null=True, blank=True)

    class Meta:
        verbose_name = 'User Info'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def get_absolute_url(self):
        """returns the url to access a particular user access"""
        return reverse('users:profile', kwargs={'username': self.username})

    def get_absolute_url(self):
        """returns the url to access a particular user access"""
        return reverse('users:profile', kwargs={'username': self.username})

    def __str__(self):
        return self.username
