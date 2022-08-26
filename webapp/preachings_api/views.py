from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import PreachingListSerializer, PreachingDetailSerializer

import sys
sys.path.append("..") # Adds higher directory to python modules path.

from preachings.models import Preaching


class PreachingList(APIView):
    '''
    List all preachings
    '''

    def get(self, request, format=None):
        preachings = Preaching.objects.all()
        serializer = PreachingListSerializer(preachings, many=True)
        return Response(serializer.data)


class PreachingDetail(APIView):
    '''
    List all preachings
    '''

    def get_object(self, pk):
        try:
            return Preaching.objects.get(pk=pk)
        except Preaching.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        preaching = self.get_object(pk)
        serializer = PreachingDetailSerializer(preaching)
        return Response(serializer.data)