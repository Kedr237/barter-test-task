from django.urls import path

from .views import AdListView, AdDetail

urlpatterns = [
    path('', AdListView.as_view(), name='ad_list'),
    path('ads/<int:id>/', AdDetail.as_view(), name='ad_detail'),
]
