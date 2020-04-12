from django.conf.urls import url, include
from django.urls import path
from .views import UserDetailView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('user/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    #path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/logout', auth_views.LogoutView.as_view(), name='logout')
]