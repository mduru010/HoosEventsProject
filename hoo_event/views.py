# /***************************************************************************************
# *  REFERENCES
# *  Title: Using the Django authentication system
# *  Author: Django Documentation
# *  Date: October 7th, 2023
# *  Version: 4.2
# *  URL: https://docs.djangoproject.com/en/4.2/topics/auth/default/
# *
# ***************************************************************************************/


from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return render(request, 'index.html')