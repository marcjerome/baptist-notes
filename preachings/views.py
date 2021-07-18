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
#from .documents import PreachingDocument

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
        kwargs['initial'] = {'tags': ','.join(tags)}
        return kwargs

class TaggedPreachingList(ListView):
    template_name = 'preachings/index_preaching_list.html'

    def get_queryset(self):
        self.tag = Tag.objects.get(title__iexact = self.kwargs['tag'])
        return Preaching.objects.filter(tags=self.tag)


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


def search(request):
    pass
    #q = request.GET.get('q')
    #preachings = PreachingDocument.search().filter("match", title=q)
    #preachings = PreachingDocument.search().filter("match", text=q)
    #preachings = PreachingDocument.search().filter("match", tags=q)#not sure for manytomanyfield if how
    #preaching = preachings.to_queryset()
    #sreturn render(request, 'preachings/search.html', {'preachings':preaching})
