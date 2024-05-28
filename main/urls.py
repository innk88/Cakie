from django.urls import path
from main.views import OrderCakeView, ViewCakeView, UserProfileView, HomeView, please_authorised, EditCakeView, \
    DeleteCakeView, EditOrderView, DeleteOrderView, EditProfileView, DeleteProfileView, ChiefDetailView
from .views import Register, ChiefRegisterView, AddCakeView, MyProfileView, AddOrderView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('register_chief/', ChiefRegisterView.as_view(), name='register_chief'),
    path('register/', Register.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': 'home'}, name='logout'),
    path('my_profile/', MyProfileView.as_view(), name='my_profile'),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('delete_profile/', DeleteProfileView.as_view(), name='delete_profile'),
    path('add_cake/', AddCakeView.as_view(), name='add_cake'),
    path('add_order/', AddOrderView.as_view(), name='add_order'),
    path('order_cake/<int:pk>/', OrderCakeView.as_view(), name='order_cake'),
    path('view_cake/<int:pk>/', ViewCakeView.as_view(), name='view_cake'),
    path('user_profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('edit_cake/<int:pk>/', EditCakeView.as_view(), name='edit_cake'),
    path('delete_cake/<int:pk>/', DeleteCakeView.as_view(), name='delete_cake'),
    path('edit_order/<int:pk>/', EditOrderView.as_view(), name='edit_order'),
    path('delete_order/<int:pk>/', DeleteOrderView.as_view(), name='delete_order'),
    path('please_authorised/', please_authorised, name='please_authorised'),
    path('chief/<int:pk>/', ChiefDetailView.as_view(), name='chief_detail'),
]
