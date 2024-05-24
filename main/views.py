from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cake
from .forms import CakeForm  # Создайте форму для модели Cake
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import ClientRegistrationForm, ChiefRegistrationForm, ClientProfileForm, ChiefProfileForm
# Create your views here.


def about(request):
    return render(request, 'main/about.html')


def home(request):
    popular_cakes = Cake.objects.order_by('-order_count')[:4]  # Отбираем 4 самых популярных торта
    return render(request, 'main/home.html', {'popular_cakes': popular_cakes})


# views.py


def register_client(request):
    if request.method == 'POST':
        user_form = ClientRegistrationForm(request.POST)
        profile_form = ClientProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            new_user = authenticate(username=user.username, password=user_form.cleaned_data['password'])
            login(request, new_user)
            return redirect(home)
    else:
        user_form = ClientRegistrationForm()
        profile_form = ClientProfileForm()
    return render(request, 'main/registration/register.html', {'user_form': user_form, 'profile_form': profile_form})


def register_chief(request):
    if request.method == 'POST':
        form = ChiefRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home)
    else:
        form = ChiefRegistrationForm()
    return render(request, 'main/registration/register_chief.html', {'form': form})


@login_required
def add_cake(request):
    if not hasattr(request.user, 'chief'):
        return redirect(home)

    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.save()
            return redirect('home')
    else:
        form = CakeForm()
    return render(request, 'main/add_cake.html', {'form': form})