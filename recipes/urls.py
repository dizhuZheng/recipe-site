from django.urls import path, include, re_path
from django.views.generic import TemplateView
<<<<<<< HEAD
from .views import PostDetailView, PostListView, CategoryListView, show_category, CategoryDetailView, CommentCreateView, CommentDeleteView, CreateRecipeView, PostDeleteView, favorite, test_ajax, PostEditView
=======
from .views import PostDetailView, PostListView, show_category, CategoryListView, CategoryDetailView, CommentCreateView, CommentDeleteView, CreateRecipeView, PostDeleteView, favorite, test_ajax, PostEditView
>>>>>>> 6b921e2b1aaf4f5f002772eddb8642a0c583cc6d

app_name = 'posts'

urlpatterns = [
<<<<<<< HEAD
    path('all_categories/', CategoryListView.as_view(), name='categories'),
    url(r'^category/(?P<hierarchy>.+)/$', show_category, name='category'),
=======
    # path('category/', TemplateView.as_view(template_name='recipes/categories.html'), name='categories'),
    path('category/', CategoryListView.as_view(), name='categories'),
    re_path(r'^category/(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),
>>>>>>> 6b921e2b1aaf4f5f002772eddb8642a0c583cc6d
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
