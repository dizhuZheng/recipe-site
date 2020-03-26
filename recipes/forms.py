from django import forms
from django.forms.models import inlineformset_factory
from .models import Post, Ingredient

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['author', 'slug']


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'


IngredientFormSet = inlineformset_factory(Post, Ingredient, fields=('name', 'amount', 'unit'), extra=3, can_delete=False, max_num=5)
