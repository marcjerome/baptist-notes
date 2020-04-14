from django.conf.urls import url, include
from django.urls import path
from .views import UserDetailView, RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout')
]