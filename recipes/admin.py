from django.contrib import admin
from .models import Post, Comment, Category, Step, Ingredient

# Register your models here.
admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin):
    exclude = ('slug',)
    list_display = ('title', 'slug', 'status', 'created_on')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Step)
admin.site.register(Ingredient)
