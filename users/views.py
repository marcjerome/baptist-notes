from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic import DetailView, CreateView, ListView
from django.views import View
from django.contrib.auth import logout
from preachings.models import Preaching
from .forms import CustomUserCreationForm 

class UserDetailView(ListView):
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    #Why can't I logout?!
    def get_queryset(self):
        self.user = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preachings'] = Preaching.objects.filter(user=self.user, privacy=False)
        return context

class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/user_create.html'


    def get_success_url(self):
        return self.request.GET.get('next')
        