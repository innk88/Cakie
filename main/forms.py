from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Chief, Cake, Person, Order


class PersonRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True)
    number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Person
        fields = ['username', 'password1', 'password2', 'email', 'address', 'number']


class ChiefRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True)
    number = forms.CharField(max_length=20, required=True)
    logo = forms.ImageField(required=False)

    class Meta:
        model = Chief
        fields = ['username', 'password1', 'password2', 'email', 'address', 'number', 'logo']


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['name', 'filling', 'price', 'weight', 'description', 'image', 'tags']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['count', 'description', 'design', 'due_date', 'image', 'chief', 'product']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }