from rest_framework import serializers

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from preachings.models import Preaching

class PreachingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preaching
        fields = ['title', 'date', 'pk', 'user', 'tags']


class PreachingDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preaching
        fields = '__all__'
