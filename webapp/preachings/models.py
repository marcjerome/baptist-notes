from django.shortcuts import reverse
from django.db import models
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.conf import settings
from .managers import TopTagsManager
import datetime

class Preaching(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    text = RichTextField()
    date = models.DateField(auto_now_add=True,)
    slug = models.SlugField(max_length=265, unique=True, blank=True, editable=False)
    privacy = models.BooleanField(default=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='preachings',)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('preaching_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        date = datetime.datetime.today()
        self.slug = '%i-%i-%i-%s' % (
            date.year, date.month, date.day, slugify(self.title)
        )   
        super(Preaching, self).save(*args, **kwargs)

   # Have unique_slug generator in utils
   # Add slug to Preaching and also make custom admin and create Tag Model

class Tag(models.Model):
    title = models.CharField(max_length=200, blank=False, unique=True)
    slug = models.SlugField(unique=True,blank=True, editable=False)
    objects = models.Manager()
    top_tags = TopTagsManager()
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Tag, self).save(*args, **kwargs)
    