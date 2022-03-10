from django.urls import path
from .views import IssuesListView, PropertiesListView
from . import views


urlpatterns = [
    path('', views.home, name='tnt-mgmt-home'),
    path('properties/', PropertiesListView.as_view(), name='properties'),
    path('issues/', IssuesListView.as_view(), name='issues'),
    path('properties/newProperty', views.newProperty, name='newProperty')
    # path('users/', views.list_users, name='tnt-mgmt-list-users')
    # path('admin/', admin.site.urls),
]
