from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserLogoutView, UserProfileUpdateView, ChangePasswordView, ActivateAccountView
 
urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('activate/<uid64>/<token>/', ActivateAccountView.as_view(), name='activate'),
]