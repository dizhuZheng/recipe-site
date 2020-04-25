from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import ProfileForm


@login_required
def profile(request):
    '''展示个人资料'''
    user = request.user
    return render(request, 'users/profile.html', {'user':user})


@login_required
def change_profile(request):
    '''更新个人资料'''
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, '个人信息更新成功！')
            return redirect('users:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'users/change_profile.html', context={'form': form
        })
