from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Comment, Ingredient, Step
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .fields import GroupedModelChoiceField
from django.contrib import messages

class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ('text', 'pic')
        widgets = {
            'text': Textarea(attrs={'label': 'Step', 'placeholder': 'Enter the specific step here', 'required': True}),
            'pic': ClearableFileInput(attrs={'type':"file", 'name':"filePhoto", 'value':"", 'id':"filePhoto",'class':"required borrowerImageFile",
            'data-errors':"PhotoUploadErrorMsg"})
            }


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'author']


class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        exclude = ['post']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','placeholder': 'Colby Chess','required': True}),
            'amount': TextInput(attrs={'class': 'form-control','placeholder': 'eg:2g','required': True}),
            }


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    template_name = 'recipes/post_list.html'
    paginate_by = 15
    ordering = ['-created_on']

    def get_queryset(self):
        return Post.objects.filter(status=1)


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


class CreateRecipeView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = Post
    template_name = 'recipes/create_recipe.html'
    success_url = 'posts:posts_list'
    form_class = PostForm
    IngredientFormSet = inlineformset_factory(Post, Ingredient, form=IngredientForm, extra=2, can_delete=False, can_order=False, min_num=1)
    StepFormSet = inlineformset_factory(Post, Step, form=StepForm, extra=1, can_delete=False, can_order=False, min_num=1)


    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(prefix='ingredients')
        step_formset = self.StepFormSet(prefix='steps')
        return render(request, self.template_name, {'form': form, 'ingredient_formset': ingredient_formset, 'step_formset': step_formset})

    def form_invalid(self, form, ingredient_formset, step_formset):
        return self.render_to_response(self.get_context_data(form=form,
                                  ingredient_formset=ingredient_formset, step_formset=step_formset))

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(request.POST, queryset=Ingredient.objects.none(), prefix='ingredients')
        step_formset = self.StepFormSet(request.POST, request.FILES, queryset=Ingredient.objects.none(), prefix='steps')
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            step_formset.instance = self.object
            step_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, ingredient_formset, step_formset)
