from django.contrib import admin
from .models import IssueCategory, Property, Address, Issue, Comment

# Register your models here.
admin.site.site_header = 'Happy Tenant Admin Panel'
admin.site.index_title = 'Admin Panel'
admin.site.site_title = 'Happy Tenant'

admin.site.register(IssueCategory)
admin.site.register(Property)
admin.site.register(Issue)
admin.site.register(Comment)

