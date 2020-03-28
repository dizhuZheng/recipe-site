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


IngredientFormSet = inlineformset_factory(Post, Ingredient, form=IngredientForm, fields=('name', 'amount', 'unit'), extra=1, min_num=1, validate_min=True, help_texts='Ingredient:', max_num=6)
