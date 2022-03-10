from django.contrib import admin
from .models import IssueCategory

# Register your models here.
admin.site.site_header = 'Happy Tenant Admin Panel'
admin.site.index_title = 'Admin Panel'
admin.site.site_title = 'Happy Tenant'

admin.site.register(IssueCategory)
