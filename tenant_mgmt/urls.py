from django.urls import path
from .views import (
    IssuesListView, 
    PropertiesListView, 
    PropertyDetailView, 
    AddressListView, 
    AddressDetailView,
    AddressCreateView
)

from . import views


urlpatterns = [
    path('', views.home, name='tnt-mgmt-home'),
    path('issues/', IssuesListView.as_view(), name='issues'),
    path('issues/new/', IssuesListView.as_view(), name='newIssue'),
    path('addresses/', AddressListView.as_view(), name='addresses'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='addressDetails'),
    path('addresses/new/', AddressCreateView.as_view(), name='newAddress'),
    path('properties/', PropertiesListView.as_view(), name='properties'),
    path('properties/new/', views.newProperty, name='newProperty'),
    path('properties/<int:pk>/', PropertyDetailView.as_view(), name='propertyDetails')
    # path('users/', views.list_users, name='tnt-mgmt-list-users')
    # path('admin/', admin.site.urls),
]
