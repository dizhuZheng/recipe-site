from django.contrib import admin
from .models import UserProfile, Image
from django.contrib.auth.decorators import login_required
# from recipes.models import Recipe

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Image)
# admin.site.register(Recipe)
