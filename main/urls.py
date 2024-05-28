from django.urls import path
from main.views import home, OrderCakeView, ViewCakeView, UserProfileView
from .views import Register, ChiefRegisterView, AddCakeView, my_profile, AddOrderView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('register_chief/', ChiefRegisterView.as_view(), name='register_chief'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'home'}, name='logout'),
    path('my_profile/', my_profile, name='my_profile'),
    path('add_cake/', AddCakeView.as_view(), name='add_cake'),
    path('add_order/', AddOrderView.as_view(), name='add_order'),
    path('order_cake/<int:pk>/', OrderCakeView.as_view(), name='order_cake'),
    path('view_cake/<int:pk>/', ViewCakeView.as_view(), name='view_cake'),
    path('user_profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
]
