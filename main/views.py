from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cake
from .forms import CakeForm  # Создайте форму для модели Cake
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import PersonRegistrationForm, ChiefRegistrationForm, ClientProfileForm, ChiefProfileForm
from django.views import View
# Create your views here.


def about(request):
    return render(request, 'main/about.html')


def home(request):
    popular_cakes = Cake.objects.order_by('-order_count')[:4]  # Отбираем 4 самых популярных торта
    return render(request, 'main/home.html', {'popular_cakes': popular_cakes})


# views.py


class Register(View):
    def get(self, request):
        form = PersonRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = PersonRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(home)
        return render(request, 'registration/register.html', {'form': form})


def register_chief(request):
    if request.method == 'POST':
        form = ChiefRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(home)
    else:
        form = ChiefRegistrationForm()
    return render(request, 'registration/register_chief.html', {'form': form})


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