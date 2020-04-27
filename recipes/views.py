from django import forms
from django.forms import formset_factory, modelformset_factory, inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from .models import Post, Comment, Ingredient, Step, Image, Tea
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

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'author', 'status']


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


class CreateRecipeView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = Post
    template_name = 'recipes/create_recipe.html'
    success_url = 'posts:posts_list'
    form_class = PostForm
    IngredientFormSet = inlineformset_factory(Post, Ingredient, exclude=('post',), extra=2, can_delete=False, can_order=False)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet()
        return render(request, self.template_name, {'form': form, 'ingredient_formset': ingredient_formset})

    def form_invalid(self, form, ingredient_formset):
        return self.render_to_response(self.get_context_data(form=form,
                                  ingredient_formset=ingredient_formset,))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(request.POST, queryset=Ingredient.objects.none())
        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, ingredient_formset)


class image_view(CreateView):
    success_url = 'success'
    template_name = 'recipes/a.html'
    ImageFormSet = modelformset_factory(Image, form=ImageForm, extra=3)
    TeaFormSet = modelformset_factory(Tea, fields='__all__', extra=3)

    def get(self, request, *args, **kwargs):
        formset = self.ImageFormSet(queryset=Image.objects.none())
        tea_formset = self.TeaFormSet(queryset=Tea.objects.none())
        return render(request, self.template_name, {'formset': formset, 'tea_formset': tea_formset})

    def post(self, request, *args, **kwargs):
        formset = self.ImageFormSet(request.POST, request.FILES, queryset=Image.objects.none())
        tea_formset = self.TeaFormSet(request.POST, queryset=Tea.objects.none())
        if formset.is_valid() and tea_formset.is_valid():
            formset.save()
            tea_formset.save()
            return redirect('posts:success')
        else:
            return render(request, self.template_name, {'formset' : formset, 'tea_formset': tea_formset})


def success(request):
    global Tea
    if request.method == 'GET':
        Images = Image.objects.all()
        tea = Tea.objects.all()
        return render(request, 'recipes/success.html', {'images' : Images, 'tea': tea})
