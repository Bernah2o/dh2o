from django import forms
from authApp.models.reporte import Reporte

class ReporteForm(forms.ModelForm):
    actividades_desarrolladas = forms.MultipleChoiceField(
        choices=Reporte.ACTIVIDADES_CHOICES,
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    imagen_antes_lavado = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )
    imagen_despues_lavado = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Reporte
        fields = '__all__'

