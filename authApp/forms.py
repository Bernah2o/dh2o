from django import forms
from dal import autocomplete
from authApp.models.clientes import Cliente


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
