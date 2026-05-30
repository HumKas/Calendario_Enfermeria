from django import forms
from .models import Cita
from datetime import time


class CitaForm(forms.ModelForm):

    HORARIOS = []

    hora_actual = 10

    while hora_actual <= 17:

        HORARIOS.append(
            (
                f"{hora_actual:02d}:00",
                f"{hora_actual:02d}:00"
            )
        )

        if hora_actual != 17:
            HORARIOS.append(
                (
                    f"{hora_actual:02d}:30",
                    f"{hora_actual:02d}:30"
                )
            )

        hora_actual += 1

    hora = forms.ChoiceField(
        choices=HORARIOS
    )

    class Meta:

        model = Cita

        fields = [
            'nombre',
            'fecha',
            'hora',
            'motivo'
        ]

        widgets = {
            'fecha': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'motivo': forms.Textarea(
                attrs={'rows': 3}
            )
        }

    def clean(self):

        cleaned_data = super().clean()

        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        # Bloquear domingos
        if fecha and fecha.weekday() == 6:
            raise forms.ValidationError(
                'Los domingos no hay atención.'
            )

        # Evitar citas repetidas
        if fecha and hora:

            existe = Cita.objects.filter(
                fecha=fecha,
                hora=hora
            ).exists()

            if existe:
                raise forms.ValidationError(
                    'Ese horario ya está ocupado.'
                )

        return cleaned_data