from django.urls import path
from .views import PreachingList, PreachingDetail

urlpatterns = [
    path('preachings/', PreachingList.as_view(), name='preachings_list_api'),
    path('preaching-detail/<int:pk>/', PreachingDetail.as_view(), name='preachings_detail_api'),
]
