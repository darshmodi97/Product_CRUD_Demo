from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from product.models import Product, Category


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class ProductCreationForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if not image:
            raise ValidationError("Image field required.")
        return image


class CategoryCreationForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
