from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Cake, Category, Tag, Chief, Order, Person
from .forms import CakeForm, OrderForm, CakeFilterForm, CakeEditForm, OrderEditForm, ChiefEditForm, PersonEditForm, \
    ReviewForm, OrderStatusForm
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


class HomeView(View):
    def get(self, request):
        form = CakeFilterForm(request.GET or None)
        cakes = Cake.objects.all()
        categories = Category.objects.all()
        tags = Tag.objects.all()
        if form.is_valid():
            tags = form.cleaned_data.get('tags')
            if tags:
                cakes = cakes.filter(tags__in=tags).distinct()
        top_cakes = Cake.objects.order_by('-order_count')[:4]
        context = {
            'form': form,
            'all_cakes': cakes,
            'popular_cakes': top_cakes,
            'tags': tags,
            'categories': categories,
        }
        return render(request, 'main/home.html', context)


# views.py


#all_cakes = Cake.objects.all()
#   popular_cakes = Cake.objects.order_by('-order_count')[:4]  # Отбираем 4 самых популярных торта
#    return render(request, 'main/home.html', {
#        'all_cakes': all_cakes,
#        'popular_cakes': popular_cakes
#    })
class Register(View):
    def get(self, request):
        form = PersonRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = PersonRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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


@method_decorator([login_required, get_real_user, get_real_chief], name='dispatch')
class MyProfileView(View):
    def get(self, request):
        if request.is_chief:
            orders_pending = Order.objects.filter(chief=request.real_chief, status='pending')
            orders_in_process = Order.objects.filter(chief=request.real_chief, status='in_process')
            orders_completed = Order.objects.filter(chief=request.real_chief, status='completed')
            my_orders_pending = Order.objects.filter(client=request.real_user, status='pending')
            my_orders_in_process = Order.objects.filter(client=request.real_user, status='in_process')
            my_orders_completed = Order.objects.filter(client=request.real_user, status='completed')
            cakes = Cake.objects.filter(chief=request.real_chief)
            context = {
                'is_chief': True,
                'cakes': cakes,
                'chief': request.real_chief,
                'orders_pending': orders_pending,
                'orders_in_process': orders_in_process,
                'orders_completed': orders_completed,
                'my_orders_pending': my_orders_pending,
                'my_orders_in_process': my_orders_in_process,
                'my_orders_completed': my_orders_completed,
            }
            return render(request, 'main/my_profile.html', context)
        else:
            orders_pending = Order.objects.filter(client=request.real_user, status='pending')
            orders_in_process = Order.objects.filter(client=request.real_user, status='in_process')
            orders_completed = Order.objects.filter(client=request.real_user, status='completed')
            context = {
                'is_chief': False,
                'orders_pending': orders_pending,
                'orders_in_process': orders_in_process,
                'orders_completed': orders_completed,
                'client': request.real_user
            }
            return render(request, 'main/my_profile.html', context)


#def profile(request):
# return render(request, 'main/my_profile.html', {'is_chief': request.is_chief})


@method_decorator([login_required, get_real_user], name='dispatch')
class UserProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(Person, pk=pk)

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
            selected_tags = request.POST.getlist('tags')
            if selected_tags:
                cake.tags.set(selected_tags)
            form.save_m2m()
            return redirect('my_profile')
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
            return redirect('my_profile')
        return render(request, 'main/order_cake.html', {'cake': cake, 'form': form})


class ViewCakeView(View):
    def get(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk)
        reviews = cake.reviews.all()
        form = ReviewForm()
        return render(request, 'main/view_cake.html', {'cake': cake, 'reviews': reviews, 'form': form})

    @method_decorator(login_required)
    def post(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.cake = cake
            review.user = request.user
            review.save()
            return redirect('view_cake', pk=cake.pk)
        reviews = cake.reviews.all()
        return render(request, 'main/view_cake.html', {'cake': cake, 'reviews': reviews, 'form': form})


def please_authorised(request):
    return render(request, 'main/please_authorised.html')


@method_decorator([login_required, get_real_chief, check_if_chief], name='dispatch')
class EditCakeView(View):
    def get(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk, chief=request.real_chief)
        form = CakeEditForm(instance=cake)
        return render(request, 'main/edit_cake.html', {'form': form, 'cake': cake})

    def post(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk, chief=request.real_chief)
        form = CakeEditForm(request.POST, request.FILES, instance=cake)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        return render(request, 'main/edit_cake.html', {'form': form, 'cake': cake})


@method_decorator([login_required,check_if_chief, get_real_chief], name='dispatch')
class DeleteCakeView(View):
    def post(self, request, pk):
        cake = get_object_or_404(Cake, pk=pk, chief=request.real_chief)
        cake.delete()
        return redirect('my_profile')


@method_decorator([login_required, get_real_user], name='dispatch')
class EditOrderView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, client=request.real_user)
        form = OrderEditForm(instance=order)
        return render(request, 'main/edit_order.html', {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, client=request.real_user)
        form = OrderEditForm(request.POST, request.FILES, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        return render(request, 'main/edit_order.html', {'form': form, 'order': order})


@method_decorator([login_required, get_real_user], name='dispatch')
class DeleteOrderView(View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, client=request.real_user)
        order.delete()
        return redirect('my_profile')


@method_decorator([login_required, get_real_user], name='dispatch')
class EditProfileView(View):
    def get(self, request):
        if request.is_chief:
            form = ChiefEditForm(instance=request.real_chief)
        else:
            form = PersonEditForm(instance=request.real_user)
        return render(request, 'main/edit_profile.html', {'form': form})

    def post(self, request):
        if request.is_chief:
            form = ChiefEditForm(request.POST, request.FILES, instance=request.real_chief)
        else:
            form = PersonEditForm(request.POST, instance=request.real_user)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        return render(request, 'main/edit_profile.html', {'form': form})


@method_decorator([login_required, get_real_user], name='dispatch')
class DeleteProfileView(View):
    def post(self, request):
        user = request.real_user
        user.delete()
        return redirect('home')


class ChiefDetailView(View):
    def get(self, request, pk):
        chief = get_object_or_404(Chief, pk=pk)
        cakes = Cake.objects.filter(chief=chief)
        return render(request, 'main/chief_detail.html', {
            'chief': chief,
            'cakes': cakes
        })


@method_decorator([login_required, get_real_user, get_real_chief,check_if_chief], name='dispatch')
class ChangeOrderStatusView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, chief=request.real_chief)
        form = OrderStatusForm(instance=order)
        return render(request, 'main/change_order_status.html', {'form': form, 'order': order})

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, chief=request.real_chief)
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
        return render(request, 'main/change_order_status.html', {'form': form, 'order': order})