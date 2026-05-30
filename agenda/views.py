from django.shortcuts import render, redirect
from .forms import CitaForm


def agendar_cita(request):

    if request.method == 'POST':
        form = CitaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('agendar')

    else:
        form = CitaForm()

    return render(
        request,
        'agenda/agendar.html',
        {'form': form}
    )