from django.urls import path
from .views import PostDetailView, PostListView, Recipes, CommentCreateView, CommentDeleteView, CreateOrderView

app_name = 'posts'

urlpatterns = [
    path('', Recipes.as_view(), name='recipes_home'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('create/', CreateOrderView.as_view(), name='create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('posts/<slug:slug>/delete_comment/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
]
