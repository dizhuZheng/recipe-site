from django.contrib import admin
from .models import Post, Comment, Category, Step, Ingredient

# Register your models here.
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Ingredient)

class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'slug', 'status', 'created_on')

class StepAdmin(admin.ModelAdmin):
    list_display = ('text', 'post')

admin.site.register(Post, PostAdmin)
admin.site.register(Step, StepAdmin)
