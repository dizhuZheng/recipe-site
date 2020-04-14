from django.views.generic import TemplateView
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Ingredient, Step
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory, FormSetView
from .fields import GroupedModelChoiceField
from .models import Category


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
    template_name = 'recipes/post_list.html'
    paginate_by = 15


class PostDetailView(DetailView):
    model = Post
    template_name = 'recipes/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['ingredients'] = self.object.post_ingredients.all()
        context['steps'] = self.object.post_steps.all()
        context['comments'] = self.object.post_comments.all()
        return context


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
    prefix = 'Ingredients'
    factory_kwargs = {'extra': 2, 'max_num': 250, 'min_num':1, 'can_order': False, 'can_delete': True}
    formset_kwargs = {'auto_id': 'my_id_%s'}


class StepInline(InlineFormSetFactory):
    model = Step
    fields = ['text', 'pic']
    prefix = 'Steps'
    factory_kwargs = {'extra': 2, 'max_num': 250, 'min_num':1, 'can_order': True, 'can_delete': True}
    formset_kwargs = {'auto_id': 'my_id_%s'}


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'recipes/confirm_delete_comment.html'

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', args=[self.kwargs.get('slug')])


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'recipes/confirm_delete_post.html'

    def get_success_url(self):
        return reverse_lazy('posts:posts_list')


class PostEditView(UpdateWithInlinesView):
    model = Post
    inlines = [IngredientInline, StepInline]
    fields = ['title', 'categories', 'cook_time']
    template_name = 'recipes/update_recipe.html'

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', args=[self.kwargs.get('slug')])



class CreateRecipeView(LoginRequiredMixin, CreateWithInlinesView):
    login_url = reverse_lazy('account_login')
    model = Post
    inlines = [IngredientInline, StepInline]
    fields = ['title', 'cook_time', 'unit', 'categories']
    template_name = 'recipes/create_recipe.html'
    success_url = 'posts_list'

    def form_valid(self, form):
        p = form.save(commit=False)
        form.instance.author = self.request.user
        p.save()
        return redirect('posts:posts_list')
