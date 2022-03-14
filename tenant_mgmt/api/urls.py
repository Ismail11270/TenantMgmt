from django.urls import path, include
from tenant_mgmt.api.views import AddressViewSet, UserViewSet, PropertyViewSet, IssueCategoryViewSet, IssueViewSet, CommentsViewSet
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token


routers = routers.DefaultRouter()
routers.register(r'Addresses', AddressViewSet)
routers.register(r'Users', UserViewSet)
routers.register(r'Properties', PropertyViewSet)
routers.register(r'IssueCategories', IssueCategoryViewSet)
routers.register(r'Issues', IssueViewSet)
routers.register(r'Comments', CommentsViewSet)


urlpatterns = [
    path('', include(routers.urls)),
    path('auth-token/', obtain_auth_token, name='api_token_auth')
]
