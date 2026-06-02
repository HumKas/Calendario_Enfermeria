from django import forms
from .models import Cita
from datetime import datetime, date


class CitaForm(forms.ModelForm):

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

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        horarios = []

        # Generar horarios 10:00 a 17:00 cada 30 min
        hora_actual = 10

        while hora_actual <= 17:

            horarios.append(
                (
                    f"{hora_actual:02d}:00",
                    f"{hora_actual:02d}:00"
                )
            )

            if hora_actual != 17:
                horarios.append(
                    (
                        f"{hora_actual:02d}:30",
                        f"{hora_actual:02d}:30"
                    )
                )

            hora_actual += 1

        fecha = None

        # Obtener fecha seleccionada
        if self.data.get('fecha'):
            fecha = self.data.get('fecha')

        # Si ya eligió fecha, quitar horas ocupadas
        if fecha:

            citas_ocupadas = Cita.objects.filter(
                fecha=fecha
            ).values_list(
                'hora',
                flat=True
            )

            horas_ocupadas = [
                hora.strftime('%H:%M')
                for hora in citas_ocupadas
            ]

            horarios = [
                horario
                for horario in horarios
                if horario[0]
                not in horas_ocupadas
            ]

        self.fields['hora'] = forms.ChoiceField(
            choices=horarios
        )

    def clean(self):

        cleaned_data = super().clean()

        fecha = cleaned_data.get('fecha')
        hora = cleaned_data.get('hora')

        hoy = date.today()

        # Bloquear fechas pasadas
        if fecha and fecha < hoy:
            raise forms.ValidationError(
                'No puedes agendar fechas pasadas.'
            )

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