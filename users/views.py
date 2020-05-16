from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserProfile
from .forms import ProfileForm
from recipes.models import Post


@login_required
def profile(request):
    '''show my profile'''
    user = request.user
    return render(request, 'users/profile.html', {'user':user})


@csrf_protect
@login_required
def change_profile(request):
    '''更新个人资料'''
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Personal Info has been updated！')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/change_profile.html', context={'form': form})


@login_required
def my_posts(request):
    user = request.user
    my_posts = Post.objects.filter(author=user, status=1)
    return render(request, 'users/my_posts.html', {'user':user, 'my_posts': my_posts})


@login_required
def my_drafts(request):
    user = request.user
    my_drafts = Post.objects.filter(author=user, status=0)
    return render(request, 'users/my_drafts.html', {'user':user, 'my_drafts': my_drafts})


@login_required
def my_saves(request):
    user = request.user
    my_saves = user.post_favo.all()
    return render(request, 'users/my_saves.html', {'user':user, 'my_saves': my_saves})
