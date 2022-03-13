from django.contrib.auth.models import User, Group

def is_admin_or_manager(user):
    return is_admin(user) or is_manager(user)

def is_admin(user):
    return Group.objects.get(name='administrator') in user.groups.all()

def is_manager(user):
    return Group.objects.get(name='manager') in user.groups.all()
    
def is_employee(user):
    return Group.objects.get(name='employee') in user.groups.all()
    