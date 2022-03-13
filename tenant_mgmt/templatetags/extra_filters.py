from django import template
from django.contrib.auth.models import Group 

register = template.Library()

@register.filter(name='has_groups')
def has_groups(user, group_names): 
    groups = list(group_names.split('|'))
    userGroups = user.groups.all()
    for groupName in groups:
        group = Group.objects.get(name=groupName) 
        if group in userGroups:
            return True
    return False

@register.filter(name='is_active')
def is_active(user):
    return len(user.groups.all()) > 0