from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Chief, Cake, Person, Order, Category, Tag, Review


class PersonRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True)
    number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email', 'address', 'number']


class ChiefRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True)
    number = forms.CharField(max_length=20, required=True)
    logo = forms.ImageField(required=False)

    class Meta:
        model = Chief
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'information', 'email', 'address', 'number', 'logo']


class CakeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label="Категория")

    class Meta:
        model = Cake
        fields = ['name', 'filling', 'price', 'weight', 'description', 'image', 'category']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(attrs={'id': 'tags'}),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['count', 'description', 'design', 'due_date', 'image']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CakeFilterForm(forms.Form):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Фильтр по тегам"
    )


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment','image']


class CakeEditForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['name', 'filling', 'price', 'weight', 'description', 'image', 'tags']


class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['count', 'description', 'design', 'due_date', 'image']


class PersonEditForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'number']


class ChiefEditForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = ['username', 'first_name', 'last_name', 'email', 'address', 'number', 'logo']