from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cake, Category, Tag, Chief, Order, Person
from .forms import CakeForm, OrderForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import PersonRegistrationForm, ChiefRegistrationForm
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group
from .decorators import check_user_permission, get_real_user, check_if_chief, get_real_chief
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.


def about(request):
    return render(request, 'main/about.html')


def home(request):
    all_cakes = Cake.objects.all()
    popular_cakes = Cake.objects.order_by('-order_count')[:4]  # Отбираем 4 самых популярных торта
    return render(request, 'main/home.html', {
        'all_cakes': all_cakes,
        'popular_cakes': popular_cakes
    })


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
            return redirect('login')
        return render(request, 'registration/register_chief.html', {'form': form})


@login_required
@get_real_user
@get_real_chief
@check_if_chief
def my_profile(request):
    if request.is_chief:
        orders = Order.objects.filter(chief=request.real_user)
        cakes = Cake.objects.filter(chief=request.real_user)
        context = {
            'is_chief': True,
            'cakes': cakes,
            'chief': request.real_user,
            'orders': orders,
        }
    else:
        orders = Order.objects.filter(client=request.real_user)
        context = {
            'is_chief': False,
            'orders': orders,
            'chief': request.real_chief
        }
    return render(request, 'main/my_profile.html', context)
#def profile(request):
   # return render(request, 'main/my_profile.html', {'is_chief': request.is_chief})


@method_decorator([login_required, get_real_user, check_if_chief], name='dispatch')
class UserProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        if isinstance(user, Chief):
            cakes = Cake.objects.filter(chief=user)
            context = {
                'is_chief': True,
                'user': user,
                'cakes': cakes
            }
        else:
            orders = Order.objects.filter(client=user)
            context = {
                'is_chief': False,
                'user': user,
                'orders': orders
            }
        return render(request, 'main/user_profile.html', context)


@method_decorator([login_required, check_if_chief, get_real_chief], name='dispatch')
class AddCakeView(View):
    def get(self, request):
        form = CakeForm()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(request, 'main/add_cake.html', {'form': form, 'categories': categories, 'tags': tags})

    def post(self, request):
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.chief = request.real_chief
            cake.save()
            form.save_m2m()
            return redirect('profile')
        categories = Category.objects.all()
        tags = Tag.objects.all()
        return render(request, 'main/add_cake.html', {'form': form, 'categories': categories, 'tags': tags})


@method_decorator([login_required, get_real_user], name='dispatch')
class AddOrderView(View):
    def get(self, request):
        form = OrderForm()
        return render(request, 'main/add_order.html', {'form': form})

    def post(self, request):
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.real_user
            order.save()
            form.save_m2m()
            return redirect('profile')
        return render(request, 'main/add_order.html', {'form': form})


@method_decorator([login_required, get_real_user], name='dispatch')
class OrderCakeView(View):
    def get(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk)
        form = OrderForm()
        return render(request, 'main/order_cake.html', {'cake': cake, 'form': form})

    def post(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk)
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.client = request.real_user
            order.chief = cake.chief
            order.product = cake
            order.save()
            form.save_m2m()
            cake.order_count += 1
            cake.save()
            return redirect('profile')
        return render(request, 'main/order_cake.html', {'cake': cake, 'form': form})


class ViewCakeView(View):
    def get(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk)
        return render(request, 'main/view_cake.html', {'cake': cake})