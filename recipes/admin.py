from django.contrib import admin
from .models import Post, Comment, Step, Ingredient, LikeCount

# Register your models here.
admin.site.register(Comment)
admin.site.register(Ingredient)
admin.site.register(LikeCount)

class PostAdmin(admin.ModelAdmin):
    exclude = ('favorites', )
    list_display = ('title', 'slug', 'status', 'created_on', 'id')

class StepAdmin(admin.ModelAdmin):
    list_display = ('text', 'post')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Category, CategoryAdmin)
