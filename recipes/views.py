from django import forms
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Ingredient, Step, Image
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from .fields import GroupedModelChoiceField
from django.contrib import messages


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
    prefix = 'Ingredients'
    fields = ['name', 'amount', 'unit']
    factory_kwargs = { 'extra': 1, 'max_num': None, 'min_num':2, 'can_order': False, 'can_delete': False}


class UpdateIngredient(IngredientInline):
    factory_kwargs = { 'extra': 1, 'min_num':1, 'can_order': False, 'can_delete': False}


class StepForm(forms.ModelForm):
    class Meta:
        model = Step
        fields = ('text', 'pic')

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['name', 'image']


class StepInline(InlineFormSetFactory):
    model = Step
    form_class = StepForm
    prefix = 'Steps'
    factory_kwargs = {'extra':1, 'max_num': 250, 'min_num':1, 'can_order': False, 'can_delete': False}

class ImageInline(InlineFormSetFactory):
    model = Image
    forms_class=ImageForm
    factory_kwargs = {'extra':1, 'max_num': 250, 'min_num':2, 'can_order': False, 'can_delete': False}


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
    inlines = [UpdateIngredient, StepInline]
    fields = ['title', 'categories', 'unit', 'cook_time']
    template_name = 'recipes/create_recipe.html'

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


class image_view(CreateView):
    success_url = 'success'
    template_name = 'recipes/a.html'
    form_class = ImageForm

    def get(self, request, *args, **kwargs):
        ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
        formset = ImageFormSet(queryset=Image.objects.none())
        return render(request, self.template_name, {'formset': formset})

    def post(self, request, *args, **kwargs):
        ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        if formset.is_valid():
            formset.save()
            return redirect('posts:success')
        else:
            return render(request, self.template_name, {'formset' : formset})


def success(request):
    if request.method == 'GET':
        Images = Image.objects.all()
        return render(request, 'recipes/success.html', {'images' : Images})
