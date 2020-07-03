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
<<<<<<< HEAD
    list_display = ('name', 'id')
=======
    prepopulated_fields = {'slug': ('name',)}
>>>>>>> 9f69666340c0860fedb468d8dc29c07334d54d84

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Step, StepAdmin)
admin.site.register(Category, CategoryAdmin)
