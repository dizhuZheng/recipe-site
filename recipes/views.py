from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView, CreateView
from .forms import CommentForm, PostForm

class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['name'] = 'BooBooRecipe'
        return context

class Recipes(TemplateView):
    template_name = 'recipes/recipes_home.html'


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    paginate_by = 15


class PostDetailView(DetailView):
    model = Post


class CommentListView(ListView):
    model = Comment
    template_name = 'recipes/post_detail.html'
    paginate_by = 2


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'recipes/add_comment_to_post.html'
    form_class = CommentForm
