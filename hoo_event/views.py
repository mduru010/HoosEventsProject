from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    if request.user.is_staff:
        return redirect('admin:index')
    elif request.user.email == "durumichael010@gmail.com" or request.user.email == "danielhuynh523@gmail.com" or request.user.email == "seankatauskas1@gmail.com":
        return redirect('admin:index')
    return render(request, 'index.html')