from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.http import JsonResponse, HttpResponse
from django.contrib.postgres.search import SearchVector
from .forms import PreachingForm
import json
from .models import Preaching, Tag
from django.contrib.auth import get_user_model
#from .documents import PreachingDocument



def preachingDeleteSuccess(request):
    return render(request, 'preachings/preaching_delete_success.html')

class PreachingDetailView(DetailView):
    model = Preaching
    template_name = 'preachings/preaching_detail.html'
    context_object_name = 'preachings'
    slug_url_kwarg = 'slug'


class PreachingCreateView(LoginRequiredMixin, CreateView):
    model = Preaching
    template_name = 'preachings/preaching_create.html'
    form_class = PreachingForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)
'''
    def get_form_kwargs(self):
        kwargs = super(PreachingCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
'''
    
class PreachingList(ListView):
    model = Preaching
    template_name = 'preachings/index_preaching_list.html'
    ordering = ['-date']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_tags'] = Tag.top_tags.all()[0:10]
        context['top_users'] = get_user_model().top_user.all()[0:10]
        return context

class PreachingDelete(LoginRequiredMixin, DeleteView):
    model = Preaching
    success_url = reverse_lazy('preaching_delete_success')
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
    form_class = PreachingForm

    def dispatch(self, request, *args, **kwargs):
        preaching = self.get_object()
        if preaching.user.id != request.user.id:
            return redirect('index_preaching_list')
        return super().dispatch(request, *args, **kwargs)
        

    def get_form_kwargs(self):
        """Return the keyword arguments for instantiating the form."""
        kwargs = super().get_form_kwargs()
        if hasattr(self, 'object'):
            kwargs.update({'instance': self.object})
        preaching = kwargs['instance']
        tags = [tag.title for tag in preaching.tags.all()]
        print('date')
        print(preaching.date)
        kwargs['initial'] = {'tags': ','.join(tags), 'pk':preaching.pk}
        return kwargs



class TaggedPreachingList(ListView):
    template_name = 'preachings/index_preaching_list.html'

    def get_queryset(self):
        self.tag = Tag.objects.get(title__iexact = self.kwargs['tag'])
        return Preaching.objects.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_tags'] = Tag.top_tags.all()[0:10]
        context['top_users'] = get_user_model().top_user.all()[0:10]
        return context


class SearchPreachingList(ListView):
    template_name = 'preachings/search_preachings.html'

    def get_queryset(self):
        search_text = self.request.GET['search_text']
        return Preaching.objects.annotate(search=SearchVector('title', 'text')).filter(search=search_text)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_text'] = self.request.GET['search_text']
        context['top_tags'] = Tag.top_tags.all()[0:10]
        context['top_users'] = get_user_model().top_user.all()[0:10]
        return context


def tag_suggestions(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        try:
            tags = Tag.objects.filter(title__icontains = data['keyword'])
            response_data = [tag.title for tag in tags]
            return JsonResponse({'tag': response_data})
        except ObjectDoesNotExist:
            return JsonResponse('')
      
    else:
        return HttpResponse('Test')
