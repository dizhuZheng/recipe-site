from django.forms import ModelForm, TextInput, Textarea, ClearableFileInput
from django.forms import inlineformset_factory
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Post, Comment, Ingredient, Step, LikeCount, Foo
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .fields import GroupedModelChoiceField
from django.contrib import messages
from django.http import JsonResponse
import json
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from users.models import UserProfile


class StepForm(ModelForm):
    class Meta:
        model = Step
        fields = ('text', 'pic')
        widgets = {
            'text': Textarea(attrs={'label': 'Step', 'placeholder': 'Enter the specific step here', 'required': True}),
            'pic': ClearableFileInput(attrs={'type':"file", 'name':"filePhoto", 'class':"required borrowerImageFile", 'onchange':"loadFile(event)",
            'data-errors':"PhotoUploadErrorMsg"})
        }


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'author', 'favorites']


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
    queryset = Post.objects.filter(status=1)
    template_name = 'recipes/post_list.html'
    paginate_by = 8
    ordering = ['-created_on']


<<<<<<< HEAD
class CategoryListView(ListView):
    model = Category
    context_object_name = 'category_list'
    queryset = Category.objects.all()
    template_name = 'recipes/categories.html'


def show_category(request, hierarchy=None):
    category_slug = hierarchy.split('/')
    category_queryset = list(Category.objects.all())
    all_slugs = [ x.slug for x in category_queryset ]
    parent = None
    for slug in category_slug:
        if slug in all_slugs:
            parent = get_object_or_404(Category, slug=slug, parent=parent)
        else:
            instance = get_object_or_404(Post, slug=slug)
            breadcrumbs_link = instance.get_cat_list()
            category_name = [' '.join(i.split('/')[-1].split('-')) for i in breadcrumbs_link]
            breadcrumbs = zip(breadcrumbs_link, category_name)
            return render(request, "postDetail.html", {'instance':instance,'breadcrumbs':breadcrumbs})
    return render(request, "recieps/categories.html", {'post_set':parent.post_set.all(), 'sub_categories':parent.children.all()})


=======
>>>>>>> 8b287a3bdb3f2aaeb2932eb74bb7ed79941afaae
class PostDetailView(DetailView):
    model = Post
    template_name = 'recipes/post_detail.html'
    context_object_name = 'post'
    Foo.objects.filter(ratings__isnull=False).order_by('ratings__average')

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['ingredients'] = self.object.post_ingredients.all()
        context['steps'] = self.object.post_steps.all()
        context['comments'] = self.object.post_comments.all()
        context['save_status'] = False
        context['likes'] = len(self.object.likes.all())
        if self.object.favorites.filter(username=self.request.user).exists():
            context['save_status'] = True
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'recipes/category_detail.html'
    context_object_name = 'category'


@login_required
@csrf_exempt
def favorite(request, slug):
    p = get_object_or_404(Post, slug=slug)
    action = request.POST.get("like")
    if action:
        try:
            p.favorites.add(request.user)
            messages.success(request, 'Successfully Saved!')
            return redirect('posts:post_detail', slug=slug)
        except:
            return HttpResponse('Error just happened.')
    else:
        return HttpResponse('No action specified.')


class CommentCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('account_login')
    model = Comment
    template_name = 'recipes/add_comment_to_post.html'
    fields = ['text']

    def form_valid(self,form):
        comment = form.save(commit=False)
        form.instance.author = self.request.user
        comment.post_id = Post.objects.get(slug=self.kwargs.get('slug')).id
        comment.save()
        messages.success(self.request, 'Comment has been posted!')
        return redirect('posts:post_detail', slug=comment.post.slug)


class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'recipes/confirm_delete_comment.html'

    def get_success_url(self):
        messages.success(self.request, 'Comment has been deleted!')
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
    IngredientFormSet = inlineformset_factory(Post, Ingredient, form=IngredientForm, extra=2, can_delete=True, can_order=False, min_num=1)
    StepFormSet = inlineformset_factory(Post, Step, form=StepForm, extra=1, can_delete=True, can_order=False, min_num=1)

    def get(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(prefix='ingredients')
        step_formset = self.StepFormSet(prefix='steps')
        return render(request, self.template_name, {'form': form, 'ingredient_formset': ingredient_formset, 'step_formset': step_formset})

    def form_invalid(self, form, ingredient_formset, step_formset):
        messages.error(self.request,'Error happened !!!')
        return self.render_to_response(self.get_context_data(form=form,ingredient_formset=ingredient_formset, step_formset=step_formset))

    def post(self, request, *args, **kwargs):
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(request.POST, queryset=Ingredient.objects.none(), prefix='ingredients')
        step_formset = self.StepFormSet(request.POST, request.FILES, queryset=Step.objects.none(), prefix='steps')
        if form.is_valid() and ingredient_formset.is_valid() and step_formset.is_valid():
            messages.success(self.request, 'Recipe has been posted!')
            self.object = form.save(commit=False)
            self.object.author = UserProfile.objects.get(id=request.user.id)
            self.object.save()
            ingredient_formset.instance = self.object
            ingredient_formset.save()
            step_formset.instance = self.object
            step_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form, ingredient_formset, step_formset)


class PostEditView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('account_login')
    model = Post
    template_name = 'recipes/update_post.html'
    form_class = PostForm
    IngredientFormSet = inlineformset_factory(Post, Ingredient, form=IngredientForm, extra=0, can_delete=True, can_order=False, min_num=1)
    StepFormSet = inlineformset_factory(Post, Step, form=StepForm, extra=0, can_delete=True, can_order=False, min_num=1)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.form_class)
        ingredient_formset = self.IngredientFormSet(prefix='ingredients', instance=self.object)
        step_formset = self.StepFormSet(prefix='steps', instance=self.object)  #this is wrong
        return self.render_to_response(self.get_context_data(form=form, ingredient_formset=ingredient_formset, step_formset=step_formset))

    def get_success_url(self):
        return reverse_lazy('posts:posts_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.form_class)

        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.author = self.request.user
            self.object.save()
            ingredient_formset = self.IngredientFormSet(request.POST, prefix='ingredients', instance=self.object, queryset=Ingredient.objects.filter(post_id=self.object.id).all())
            if ingredient_formset.is_valid():
                ingredient_formset.instance = self.object
                ingredient_formset.save()
            else:
                return self.render_to_response(self.get_context_data(ingredient_formset=ingredient_formset))
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))


@csrf_exempt
def test_ajax(request, slug):
    p = get_object_or_404(Post, slug=slug)
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'You haven\'t logged in yet!!!'})
    if LikeCount.objects.filter(posts__id=p.id, author=request.user).exists():
        return JsonResponse({'message': 'You already liked it!!!'})
    else:
        like = LikeCount(content_object=p, author=request.user)
        like.save()
        like_count = len(p.likes.all())
        return JsonResponse({'likes': like_count, 'message': 'Success!!!'})
