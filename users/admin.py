from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.decorators import login_required
# from recipes.models import Recipe

# Register your models here.
admin.site.register(UserProfile)
# admin.site.register(Recipe)
