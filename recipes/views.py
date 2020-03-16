from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm, PostForm
from django.shortcuts import redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView

class Home(TemplateView):
    template_name = 'home.html'
    def get_context_data(self, *args, **kwargs):
        context = super(Home, self).get_context_data(*args, **kwargs)
        context['name'] = 'BooBooRecipe'
        return context

class Recipes(TemplateView):
    template_name = 'recipes/recipes_home.html'

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.filter(active=True)
    # comment posted
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        else:
            form = CommentForm()
    return render(request, 'recipes/add_comment_to_post.html', {'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            Post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'recipes/post_detail.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)


class PostListView(ListView):
    model = Post
    context_object_name = 'post_list'
    ordering = ['-created_on']
    paginate_by = 15


class PostDetailView(DetailView):
    model = Post
    template_name = 'recipes/post_detail.html'
