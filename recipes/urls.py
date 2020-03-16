from django.urls import path
from .views import PostDetailView, PostListView, Recipes, CommentCreateView

app_name = 'posts'

urlpatterns = [
    path('', Recipes.as_view(), name='recipes_home'),
    path('posts/<slug:slug>', PostDetailView.as_view(), name='post_detail'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('posts/comments/', CommentCreateView.as_view(), name='comments'),
]
