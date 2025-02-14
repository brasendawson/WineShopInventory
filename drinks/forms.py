from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User  
from .models import Drink, Category

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DrinkForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model = Drink
        fields = ['name' , 'quantity' , 'category' , 'price']