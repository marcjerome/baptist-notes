from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import PreachingForm
from .models import Preaching

class PreachingDetailView(DetailView):
    model = Preaching
    template_name = 'preachings/preaching_detail.html'
    context_object_name = 'preachings'
    slug_url_kwarg = 'slug'

    #Solve preaching object is not iterable in .html when its only one

class PreachingCreateView(LoginRequiredMixin, CreateView):
    model = Preaching
    template_name = 'preachings/preaching_create.html'
    form_class = PreachingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PreachingList(ListView):
    model = Preaching
    template_name = 'preachings/index_preaching_list.html'

class PreachingDelete(DeleteView):
    model = Preaching
    success_url = reverse_lazy('index_preaching_list')
    template_name = 'preachings/preaching_confirm_delete.html'
    slug_field = 'slug' 

    def dispatch(self, request, *args, **kwargs):
        preaching = self.get_object()
        if preaching.user.id != request.user.id:
            return redirect('index_preaching_list')
        return super().dispatch(request, *args, **kwargs)
        
       
class PreachingUpdate(UpdateView):
    model = Preaching
    slug_field = 'slug'
    template_name = 'preachings/preaching_update.html'
    fields = ['title', 'text', 'date', 'privacy']