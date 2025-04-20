from django.urls import path

from . import views

urlpatterns = [
    path('', views.AdListView.as_view(), name='ad_list'),
    path('ads/<int:id>/', views.AdDetail.as_view(), name='ad_detail'),
    path('ads/create/', views.AdCreateView.as_view(), name='ad_create'),
    path('ads/my/', views.MyAdListView.as_view(), name='my_ad_list'),
    path('ads/delete/<int:id>/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('proposals/delete/<int:id>/', views.ProposalDeleteView.as_view(), name='proposal_delete'),
    path('proposals/my/', views.MyProposalsView.as_view(), name='my_proposals'),
    path('proposals/for-me/', views.ProposalsForMeView.as_view(), name='proposals_for_me'),
    path('proposals/edit/<int:id>/', views.EditProposalView.as_view(), name='edit_proposal'),
]
