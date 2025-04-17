from django.urls import path

from .views import AdCreateView, AdDetail, AdListView

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ads/<int:id>/', AdDetail.as_view(), name='ad_detail'),
    path('ads/create/', AdCreateView.as_view(), name='ad_create')
]
