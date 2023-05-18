from rest_framework import serializers
from authApp.models.reporte import Reporte

class ReporteSerializer(serializers.ModelSerializer):
    imagen = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    
    
    class Meta:
      model = Reporte
      fields = ['id_reporte', 'orden_de_trabajo', 'cliente', 'fecha', 'descripcion', 'imagen','creacion','proxima_limpieza']