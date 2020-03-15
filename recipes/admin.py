from django.contrib import admin
from .models import Post, Comment

# Register your models here.
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on')


admin.site.register(Post, PostAdmin)
