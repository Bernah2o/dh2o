from django import forms
from dal import autocomplete
from authApp.models.clientes import Cliente
from authApp.models.reporte import Reporte


class ReporteForm(forms.ModelForm):
    class Meta:
        model = Reporte
        fields = "__all__"

    def clean_actividades_desarrolladas(self):
        actividades_desarrolladas = self.cleaned_data["actividades_desarrolladas"]
        if actividades_desarrolladas and "All" in actividades_desarrolladas:
            return [choice[0] for choice in Reporte.ACTIVIDADES_CHOICES]
        return actividades_desarrolladas

    def clean_orden_de_trabajo(self):
        orden_de_trabajo = self.cleaned_data["orden_de_trabajo"]
        if orden_de_trabajo:
            self.cleaned_data["cliente"] = orden_de_trabajo.cliente
        return orden_de_trabajo


class LoginForm(forms.Form):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nombre': autocomplete.ModelSelect2(url='nombre-autocomplete'),
            'apellido': autocomplete.ModelSelect2(url='apellido-autocomplete'),
            # Agrega otros campos y sus autocompletados aquí
        }