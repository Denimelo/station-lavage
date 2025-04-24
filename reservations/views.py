from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Reservation
from .forms import ReservationForm, AssignationForm

@login_required
def create_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.client = request.user
            reservation.save()
            return redirect('reservations:list')
    else:
        form = ReservationForm()
    return render(request, 'reservations/create.html', {'form': form})

@login_required
def list_reservations(request):
    reservations = Reservation.objects.filter(client=request.user)
    return render(request, 'reservations/list.html', {'reservations': reservations})

@login_required
def prendre_rdv(request):
    return render(request, 'reservations/prise_rdv.html')

@login_required
def reservations_employe(request):
    if hasattr(request.user, 'employe'):
        reservations = Reservation.objects.filter(employe=request.user.employe)
        return render(request, 'reservations/reservations_employe.html', {'reservations': reservations})
    else:
        return redirect('home')

@login_required
def reservations_gestionnaire(request):
    if hasattr(request.user, 'gestionnaire'):
        reservations = Reservation.objects.all()
        return render(request, 'reservations/reservations_gestionnaire.html', {'reservations': reservations})
    else:
        return redirect('home')
    
@login_required
def assigner_employe(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if hasattr(request.user, 'gestionnaire'):
        if request.method == 'POST':
            form = AssignationForm(request.POST, instance=reservation)
            if form.is_valid():
                form.save()
                return redirect('reservations:reservations_gestionnaire')
        else:
            form = AssignationForm(instance=reservation)
        return render(request, 'reservations/assigner_employe.html', {'form': form, 'reservation': reservation})
    else:
        return redirect('home')