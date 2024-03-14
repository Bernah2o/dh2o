from django import forms
from dal import autocomplete
from authApp.models.clientes import Cliente
from authApp.models.ordendetrabajo import ServicioEnOrden
from authApp.models.reporte import Reporte


class ReporteForm(forms.ModelForm):
    servicios_en_orden = forms.ModelMultipleChoiceField(
        queryset=ServicioEnOrden.objects.none(),
        required=False,
        widget=forms.SelectMultiple(),
    )
    class Meta:
        model = Reporte
        fields = ['orden_de_trabajo', 'servicio_en_orden', 'fecha', 'imagen_antes_lavado_1', 'imagen_antes_lavado_2', 'imagen_despues_lavado_1', 'imagen_despues_lavado_2', 'proxima_limpieza']

    def __init__(self, *args, **kwargs):
        orden_de_trabajo_instance = kwargs.pop("orden_de_trabajo_instance", None)
        super().__init__(*args, **kwargs)
        if orden_de_trabajo_instance:
            servicios_en_orden = (
                orden_de_trabajo_instance.servicios_en_orden_detalle.all()
            )
            self.fields["servicios_en_orden"].queryset = servicios_en_orden

            for servicio in servicios_en_orden:
                cantidad_disponible = servicio.cantidad_servicio
                self.fields[f"servicio_{servicio.id}"] = forms.IntegerField(
                    label=f"Servicio: {servicio.servicio.nombre} - Cantidad disponible: {cantidad_disponible}",
                    required=False,
                    min_value=0,
                    max_value=cantidad_disponible,
                    widget=forms.NumberInput(attrs={"class": "form-control"}),
                )

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
