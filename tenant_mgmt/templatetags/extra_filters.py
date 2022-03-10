from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    group = Group.objects.get(name=group_name) 
    return True if group in user.groups.all() else False

@register.filter(name='is_active')
def is_active(user):
    print(len(user.groups.all())>0)
    return len(user.groups.all()) > 0