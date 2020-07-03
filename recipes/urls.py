from django.urls import path, include, re_path
from django.conf.urls import url
from django.views.generic import TemplateView
from .views import PostDetailView, PostListView, CategoryListView, show_category, CategoryDetailView, CommentCreateView, CommentDeleteView, CreateRecipeView, PostDeleteView, favorite, test_ajax, PostEditView

app_name = 'posts'

urlpatterns = [
    path('all_categories/', CategoryListView.as_view(), name='categories'),
    url(r'^category/(?P<hierarchy>.+)/$', show_category, name='category'),
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
