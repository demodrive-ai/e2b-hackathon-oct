from django import forms
from .models import BlogCodeRecipe


class BlogCodeRecipeForm(forms.ModelForm):
    class Meta:
        model = BlogCodeRecipe
        fields = "__all__"
