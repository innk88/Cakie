from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cake
from .forms import CakeForm  # Создайте форму для модели Cake
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import PersonRegistrationForm, ChiefRegistrationForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
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


class ChiefRegisterView(View):
    def get(self, request):
        form = ChiefRegistrationForm()
        return render(request, 'registration/register_chief.html', {'form': form})

    def post(self, request):
        form = ChiefRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            chief = form.save(commit=False)
            chief.save()
            form.save_m2m()
            chief_group = Group.objects.get(name='Chiefs')
            chief.groups.add(chief_group)
            return redirect('login')
        return render(request, 'registration/register_chief.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class AddCakeView(View):
    def get(self, request):
        form = CakeForm()
        return render(request, 'main/add_cake.html', {'form': form})

    def post(self, request):
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.save()
            form.save_m2m()
            return redirect('home')
        return render(request, 'main/add_cake.html', {'form': form})