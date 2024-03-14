from django import forms
from dal import autocomplete
from django.db.models import Count
from authApp.models.clientes import Cliente
from authApp.models.ordendetrabajo import OrdenDeTrabajo, ServicioEnOrden
from authApp.models.reporte import Reporte


class ReporteForm(forms.ModelForm):
    servicios_en_orden = forms.ModelMultipleChoiceField(
        queryset=ServicioEnOrden.objects.none(),
        required=False,
        widget=forms.SelectMultiple(),
    )

    orden_de_trabajo = forms.ModelChoiceField(
        queryset=OrdenDeTrabajo.objects.all(), required=True
    )  # Agregamos este campo

    class Meta:
        model = Reporte
        fields = ['orden_de_trabajo', 'servicio_en_orden', 'fecha', 'imagen_antes_lavado_1', 'imagen_antes_lavado_2', 'imagen_despues_lavado_1', 'imagen_despues_lavado_2', 'proxima_limpieza']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "orden_de_trabajo_instance" in kwargs:
            orden_de_trabajo_instance = kwargs.pop("orden_de_trabajo_instance")
            servicios_en_orden = (
                orden_de_trabajo_instance.servicios_en_orden_detalle.all()
            )
            self.fields["servicios_en_orden"].queryset = servicios_en_orden

            ordenes_no_completas = OrdenDeTrabajo.objects.exclude(
                id=orden_de_trabajo_instance.id
            )
            ordenes_no_completas = ordenes_no_completas.filter(completa=False)
            servicios_pendientes = (
                orden_de_trabajo_instance.servicios_en_orden_detalle.filter(
                    reporte__isnull=True
                )
            )
            ordenes_no_completas = ordenes_no_completas.annotate(
                num_reportes=Count("servicios_en_orden_detalle__reporte")
            ).filter(num_reportes__lt=servicios_pendientes.count())
            self.fields["orden_de_trabajo"].queryset = ordenes_no_completas

    def clean(self):
        cleaned_data = super().clean()
        servicios_en_orden = cleaned_data.get("servicios_en_orden", [])
        for servicio_en_orden in servicios_en_orden:
            servicio_id = servicio_en_orden.id
            cantidad_disponible = servicio_en_orden.cantidad_servicio
            cantidad_seleccionada = cleaned_data.get(f"servicio_{servicio_id}", 0)
            if cantidad_seleccionada > cantidad_disponible:
                self.add_error(
                    f"servicio_{servicio_id}",
                    f"La cantidad seleccionada no puede ser mayor que {cantidad_disponible}",
                )
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = "__all__"
        widgets = {
            "nombre": autocomplete.ModelSelect2(url="nombre-autocomplete"),
            "apellido": autocomplete.ModelSelect2(url="apellido-autocomplete"),
            # Agrega otros campos y sus autocompletados aquí
        }
