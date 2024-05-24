from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Chief, Cake, Person


class PersonRegistrationForm(UserCreationForm):
    address = forms.CharField(max_length=100, required=True)
    number = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Person
        fields = ['username', 'password1', 'password2', 'email', 'address', 'number']


class ChiefRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")
    logo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['address', 'number']


class ChiefProfileForm(forms.ModelForm):
    class Meta:
        model = Chief
        fields = ['address', 'number', 'logo']


class CakeForm(forms.ModelForm):
    class Meta:
        model = Cake
        fields = ['name', 'filling', 'price', 'weight', 'description', 'image', 'tags']