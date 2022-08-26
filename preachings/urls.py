from django.conf.urls import url, include
from django.urls import path
from .views import tag_suggestions, preachingDeleteSuccess, PreachingDetailView, PreachingCreateView, PreachingList, PreachingUpdate, PreachingDelete, TaggedPreachingList, SearchPreachingList

urlpatterns = [
    path('', PreachingList.as_view(), name='index_preaching_list'),
    path('note/add/', PreachingCreateView.as_view(), name='preaching_create'),
    path('note/update/<slug:slug>/', PreachingUpdate.as_view(), name='preaching_update'),
    path('note/delete/<slug:slug>/', PreachingDelete.as_view(), name='preaching_delete'),
    path('note/confirm-delete/success/', preachingDeleteSuccess, name='preaching_delete_success'),
    path('note/<slug:slug>/', PreachingDetailView.as_view(), name='preaching_detail'),
    path('search/', SearchPreachingList.as_view(), name='search'),
    path('tag/<str:tag>/', TaggedPreachingList.as_view(), name='tagged_preaching_list'),
    path('note/add/tag', tag_suggestions, name='tag_suggestions'),
    
]

