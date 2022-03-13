from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def manager_requred(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: is_allowed(u, ['administrator', 'manager']),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def no_employee_allowed(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: not is_allowed(u, ['employee']),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_requred(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):

    actual_decorator = user_passes_test(
        lambda u: is_allowed(u, ['administrator']),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def is_allowed(usr, groups):
    allowed_group = set(groups)
    groups = [ x.name for x in usr.groups.all()]
    if allowed_group.intersection(set(groups)):
       return True
    return False

# def admin_requred(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):


# def group_required(group):
#     actual_decorator = user_passes_test(
#         lambda u: user.groups.filter(name='manager').exists(),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if function:
#         return actual_decorator(function)
#     return actual_decorator