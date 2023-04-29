from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from rest_framework import routers
from django.conf.urls.static import static

#creacion de API
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.ordendetrabajoViewsSet import OrdenDeTrabajoViewSet
from authApp.views.reporteViewsSet import ReporteViewSet

from authApp.views.repuestoViewsSet import RepuestoViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
from authApp.views.mpagoViewSet import MpagoViewSet
from authApp.views.tanqueViewSet import TanqueViewSet



from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp import views

router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'operadores', OperadorViewSet)
router.register(r'mpagos', MpagoViewSet)
router.register(r'tanques', TanqueViewSet)
router.register(r'repuestos', RepuestoViewSet)
router.register(r'ordenesdetrabajo', OrdenDeTrabajoViewSet)
router.register(r'reportes', ReporteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reportes/<int:pk>/imprimir/', ReporteViewSet.as_view({'get': 'imprimir_reporte'}), name='imprimir_reporte'),

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
