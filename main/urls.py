from django.urls import path
from main.views import home
from .views import Register, ChiefRegisterView, AddCakeView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('register_chief/', ChiefRegisterView.as_view(), name='register_chief'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_cake/', AddCakeView.as_view(), name='add_cake'),
]
