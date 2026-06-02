from django.shortcuts import render, redirect
from .forms import CitaForm
from .models import Cita
from rest_framework import viewsets
from .serializers import CitaSerializer

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
class CitaViewSet(viewsets.ModelViewSet):

    queryset = Cita.objects.all().order_by(
        'fecha',
        'hora'
    )

    serializer_class = CitaSerializer