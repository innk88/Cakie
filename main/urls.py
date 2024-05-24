from django.urls import path
from main.views import home
from .views import Register
from main.views import register_chief
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name='home'),
    path('register/chief/', register_chief, name='register_chief'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
