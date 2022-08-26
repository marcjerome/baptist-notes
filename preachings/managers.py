from django.db import models
from django.db.models import Count

class TopTagsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(num_preaching=Count('preachings')).order_by('-num_preaching')

