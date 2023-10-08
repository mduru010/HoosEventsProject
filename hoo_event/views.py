from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
    if request.user.is_staff:
        return redirect('admin:index')
    return render(request, 'index.html')