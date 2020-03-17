from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]
        widgets = {"post": forms.HiddenInput()}


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']
