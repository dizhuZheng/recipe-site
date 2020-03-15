from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text',]


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']