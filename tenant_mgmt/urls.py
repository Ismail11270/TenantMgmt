from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='tnt-mgmt-home'),
    path('users/', views.list_users, name='tnt-mgmt-list-users')
    # path('admin/', admin.site.urls),
]
