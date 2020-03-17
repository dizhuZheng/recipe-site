from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import CommentForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'recipes/add_comment_to_post.html'
    form_class = CommentForm
    success_url = reverse_lazy('posts')

    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        return super(CommentCreateView, self).form_valid(form)


class CommentUpdate(UpdateView):
    model = Comment
    fields = ['text']


class CommentDelete(DeleteView):
    model = Comment
    success_url = reverse_lazy('posts:post_detail')
