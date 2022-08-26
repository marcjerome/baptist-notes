from django.conf.urls import url, include
from django.urls import path
from .views import UserDetailView, RegisterView, UserUpdate, CustomPasswordChangeView, CustomPasswordChangeDone, logoutConfirmView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('accounts/update/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/register/', RegisterView.as_view(), name='register'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change_success/', CustomPasswordChangeDone.as_view(), name='password_change_done'),
    path('accounts/logout_confirmation', logoutConfirmView, name='logout_confirmation' ),
    path('accounts/reset_password/', auth_views.PasswordResetView.as_view(template_name = 'registration/reset_password.html'), name ='reset_password'),
    path('accounts/reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'registration/reset_password_done.html'), name ='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = 'registration/reset_password_confirm.html'), name ='password_reset_confirm'),
    path('accounts/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'registration/reset_password_complete.html'), name ='password_reset_complete'),
]  