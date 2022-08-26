from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy
from preachings.models import Preaching
from .forms import CustomUserCreationForm, CustomUserUpdateForm


class UserDetailView(ListView):
    template_name = 'users/user_detail.html'
    context_object_name = 'user'

    def get_queryset(self):
        self.user = get_user_model().objects.get(pk=self.kwargs['pk'])
        return self.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['preachings'] = Preaching.objects.filter(user=self.user).order_by('-date')
        return context



class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/user_create.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index_preaching_list')
        return super(RegisterView, self).get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('index_preaching_list')

class UserUpdate(LoginRequiredMixin,SuccessMessageMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/user_update.html'
    form_class = CustomUserUpdateForm
    success_message = "Profile successfully updated!"

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.middle_name == None:
            self.get_object().middle_name == ' '
        if user.id != request.user.id:
            return redirect('index_preaching_list')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user_detail',kwargs={'pk': self.get_object().pk})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'registration/password_change.html'



class CustomPasswordChangeDone(PasswordChangeDoneView, SuccessMessageMixin):
    template_name = 'registration/password_change_success.html'


def logoutConfirmView(request):
    return render(request, 'registration/logout_confirmation.html')