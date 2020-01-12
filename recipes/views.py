from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm
from django.shortcuts import redirect
from .models import Post, Comment
from django.views.generic import ListView, DetailView

class Home(TemplateView):
    template_name = 'home.html'


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
    template_name = 'post_list.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
