from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_statistiques(request):
    return render(request, 'statistiques/dashboard.html')