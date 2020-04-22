from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponse
from .forms import PreachingForm
import json
from .models import Preaching, Tag

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

class PreachingDelete(LoginRequiredMixin, DeleteView):
    model = Preaching
    success_url = reverse_lazy('index_preaching_list')
    template_name = 'preachings/preaching_confirm_delete.html'
    slug_field = 'slug' 

    def dispatch(self, request, *args, **kwargs):
        preaching = self.get_object()
        if preaching.user.id != request.user.id:
            return redirect('index_preaching_list')
        return super().dispatch(request, *args, **kwargs)
        
       
class PreachingUpdate(LoginRequiredMixin, UpdateView):
    model = Preaching
    slug_field = 'slug'
    template_name = 'preachings/preaching_update.html'
    fields = ['title', 'text', 'date', 'privacy']

    def dispatch(self, request, *args, **kwargs):
        preaching = self.get_object()
        if preaching.user.id != request.user.id:
            return redirect('index_preaching_list')
        return super().dispatch(request, *args, **kwargs)
        

class TaggedPreachingList(ListView):
    template_name = 'preachings/index_preaching_list.html'

    def get_queryset(self):
        self.tag = Tag.objects.get(title__iexact = self.kwargs['tag'])
        return Preaching.objects.filter(tags=self.tag)


def tag_suggestions(request):
    print('inside tag_suggestions ')
    if request.method == 'POST':
        data = json.loads(request.body) 

        try:
            tags = Tag.objects.filter(title__icontains = data['keyword'])
            response_data = [tag.title for tag in tags]
            return JsonResponse({'tag': response_data})
        except ObjectDoesNotExist:
            return JsonResponse('')
      
    else:
        print('not ajax Test')
        return HttpResponse('Test')
