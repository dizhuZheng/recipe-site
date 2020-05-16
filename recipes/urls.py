from django.urls import path, include
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import PostDetailView, PostListView, CommentCreateView, CommentDeleteView, CreateRecipeView, PostDeleteView, favorite, test_ajax, PostEditView

app_name = 'posts'

urlpatterns = [
    path('', TemplateView.as_view(template_name="recipes/templates/recipes/recipes_home.html"), name='recipes_home'),
    path('posts/', PostListView.as_view(), name='posts_list'),
    path('create/', CreateRecipeView.as_view(), name='create'),
    path('posts/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<slug:slug>/ajax/', test_ajax, name='ajax'),
    path('posts/<slug:slug>/favorite/', favorite, name='post_favorite'),
    path('posts/<slug:slug>/update_post/', PostEditView.as_view(), name='update_post'),
    path('posts/<slug:slug>/add_comment/', CommentCreateView.as_view(), name='add_comment'),
    path('posts/<slug:slug>/delete_comment/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
    path('posts/<slug:slug>/delete_post/', PostDeleteView.as_view(), name='delete_post'),
]
