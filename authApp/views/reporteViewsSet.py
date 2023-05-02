import io
from django.http import FileResponse, HttpResponse
from django.template.loader import get_template
from rest_framework import viewsets
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from authApp.models.reporte import Reporte
from authApp.serializers.reporteSerializers import ReporteSerializer
import xhtml2pdf.pisa as pisa

class ReporteViewSet(viewsets.ModelViewSet):
    queryset = Reporte.objects.all()
    serializer_class = ReporteSerializer

    
   