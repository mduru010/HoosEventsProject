# /***************************************************************************************
# *  REFERENCES
# *  Title: Using the Django authentication system
# *  Author: Django Documentation
# *  Date: October 7th, 2023
# *  Version: 4.2
# *  URL: https://docs.djangoproject.com/en/4.2/topics/auth/default/
# *
# *  Title: User group get method filter.exists
# *  Author: Charlesthk
# *  Date: October 18th, 2023
# *  URL: https://stackoverflow.com/questions/4789021/in-django-how-do-i-check-if-a-user-is-in-a-certain-group
# *
# ***************************************************************************************/


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    if request.user.groups.filter(name='admin_users').exists() or (request.user.email == "pointlssus1@gmail.com") or (request.user.email == "cs3240.super@gmail.com"):
        return redirect('admin_event')
    elif request.user.is_staff:
        return redirect('admin:index')
    elif request.user.groups.filter(name='regular_users').exists() or (request.user.email == "cs3240.student@gmail.com"):
        return redirect('index')
    return redirect('index') # delete once we properly define all users that sign up as regular users