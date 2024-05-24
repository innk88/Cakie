from django import forms
from django.contrib.auth.models import User
from .models import Chief, Cake, Person


class ClientRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Подтверждение пароля")

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