from django.urls import path
from .views import (
    AddressDeleteView,
    AddressUpdateView,
    IssueCategoryCreateView,
    IssueCategoryDeleteView,
    IssueCategoryListView,
    IssueCategoryUpdateView,
    IssueDeleteView,
    IssueUpdateView,
    IssuesListView,
    IssueDetailView,
    PropertiesListView,
    PropertyDeleteView, 
    PropertyDetailView, 
    AddressListView, 
    AddressDetailView,
    AddressCreateView,
    PropertyUpdateView
)

from . import views


urlpatterns = [
    path('', views.home, name='tnt-mgmt-home'),
    path('issues/', IssuesListView.as_view(), name='issues'),
    path('issues/new/', views.newIssue, name='newIssue'),
    path('issues/<int:pk>', IssueDetailView.as_view(), name='issueDetails'),
    path('issues/<int:pk>/edit', IssueUpdateView.as_view(), name='issueEdit'),
    path('issues/<int:pk>/delete/', IssueDeleteView.as_view(), name='issueDelete'),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='addressDetails'),
    path('addresses/<int:pk>/edit', AddressUpdateView.as_view(), name='addressEdit'),
    path('addresses/<int:pk>/delete/', AddressDeleteView.as_view(), name='addressDelete'),
    path('addresses/new/', AddressCreateView.as_view(), name='newAddress'),
    path('properties/', PropertiesListView.as_view(), name='properties'),
    path('properties/new/', views.newProperty, name='newProperty'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='propertyDetails'),
    path('properties/<int:pk>/edit/', PropertyUpdateView.as_view(), name='propertyEdit'),
    path('properties/<int:pk>/delete/', PropertyDeleteView.as_view(), name='propertyDelete'),
    path('categories/', IssueCategoryListView.as_view(), name='categories'),
    path('categories/new/', IssueCategoryCreateView.as_view(), name='newCategory'),
    path('categories/<int:pk>/edit/', IssueCategoryUpdateView.as_view(), name='categoryEdit'),
    path('categories/<int:pk>/delete/', IssueCategoryDeleteView.as_view(), name='categoryDelete'),
]
