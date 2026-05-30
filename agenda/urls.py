from django.urls import path
from .views import agendar_cita

urlpatterns = [
    path('', agendar_cita, name='agendar'),
]