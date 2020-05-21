from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Preaching, Tag
from django.contrib.auth import get_user_model

User = get_user_model()

@registry.register_document
class PreachingDocument(Document):
    user = fields.ObjectField()
    text = fields.TextField()
    tags = fields.NestedField(properties={
        'title': fields.TextField(),
        'slug': fields.TextField(),
    }) 
    class Index:
        name = 'preachings'
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0,    
                    }

    class Django:
        model = Preaching
        fields = ['title', 'slug',]
        related_models = [User,Tag]

    def get_instance_from_related(self, related_instance):
        if isinstance(related_instance, User):
            return related_instance.user
        elif isinstance(related_instance, Tag):
            return related_instance.tags_set.all()