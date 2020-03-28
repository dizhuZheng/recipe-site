from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Ingredient
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory, SuccessMessageMixin, FormSetView



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
    template_name = 'recipes/post_detail.html'


class CommentListView(ListView):
    model = Comment
    template_name = 'recipes/post_detail.html'
    paginate_by = 2


class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = Comment
    template_name = 'recipes/add_comment_to_post.html'
    fields = ['text']

    def form_valid(self, form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        comment.post_id = Post.objects.get(slug=self.kwargs.get('slug')).id
        comment.save()
        return redirect('posts:post_detail', slug=comment.post.slug)


class IngredientInline(InlineFormSetFactory):
    model = Ingredient
    fields = ['name', 'amount', 'unit']
    factory_kwargs = {'extra': 2, 'max_num': None, 'min_num':1, 'can_order': False, 'can_delete': False}


class CreateOrderView(LoginRequiredMixin, CreateWithInlinesView):
    login_url = reverse_lazy('account_login')
    model = Post
    inlines = [IngredientInline]
    fields = ['title', 'text', 'categories', 'cook_time']
    template_name = 'recipes/create_recipe.html'
    success_url = 'posts_list'

    def form_valid(self, form):
        p = form.save(commit=False)
        form.instance.author = self.request.user
        p.save()
        return redirect('posts:posts_list')


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'recipes/confirm_delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', args=[self.kwargs.get('slug')])
