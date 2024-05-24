from django.urls import path
from main.views import home
from main.views import register_client
from main.views import register_chief
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', home, name="main"),
    path('register/chief/', register_chief, name='register_chief'),
    path('register/', register_client, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='main/registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=home), name='logout'),
]
