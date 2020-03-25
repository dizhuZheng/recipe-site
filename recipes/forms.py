from django import forms
from django.forms import inlineformset_factory
from .models import Post, Ingredient

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']


PostFormSet = inlineformset_factory(Post, Ingredient, fields=('name',), extra=2, can_delete=False)
