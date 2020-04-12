from django.conf.urls import url, include
from django.urls import path
from .views import PreachingDetailView, PreachingCreateView, PreachingList, PreachingUpdate, PreachingDelete, TaggedPreachingList

urlpatterns = [
    path('note/add/', PreachingCreateView.as_view(), name='preaching_create'),
    path('note/update/<slug:slug>/', PreachingUpdate.as_view(), name='preaching_update'),
    path('note/delete/<slug:slug>/', PreachingDelete.as_view(), name='preaching_delete'),
    path('note/<slug:slug>/', PreachingDetailView.as_view(), name='preaching_detail'),
    path('', PreachingList.as_view(), name='index_preaching_list'),
    path('<str:tag>/', TaggedPreachingList.as_view(), name='tagged_preaching_list')

]

#2020-4-3-test