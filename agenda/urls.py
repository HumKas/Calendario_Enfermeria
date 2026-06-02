from django.urls import path, include
from .views import agendar_cita, CitaViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(
    r'citas',
    CitaViewSet
)


urlpatterns = [
    path(
        '',
        agendar_cita,
        name='agendar'
    ),

    path(
        'api/',
        include(router.urls)
    ),
]