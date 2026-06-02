from django.shortcuts import render, redirect
from .forms import CitaForm
from .models import Cita


def agendar_cita(request):

    if request.method == 'POST':

        form = CitaForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('agendar')

    else:
        form = CitaForm()

    citas = Cita.objects.all().order_by(
        'fecha',
        'hora'
    )

    context = {
        'form': form,
        'citas': citas
    }

    return render(
        request,
        'agenda/agendar.html',
        context
    )