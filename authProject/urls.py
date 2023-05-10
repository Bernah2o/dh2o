from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.ordendetrabajoViewsSet import OrdenDeTrabajoViewSet
from authApp.views.reporteViewsSet import ReporteViewSet
from authApp.views.repuestoViewsSet import RepuestoViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
from authApp.views.mpagoViewSet import MpagoViewSet
from authApp.views.tanqueViewSet import TanqueViewSet
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.facturaViewSet import ventas_mensuales



# from authApp.views.reporteViewsSet import GeneratePdf


# Definimos nuestro router para manejar todas las vistas de la API
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



# Configuramos las URLs
urlpatterns = [
    # Agregamos las URLs del router
    path('', include(router.urls)),
    # Agregamos la URL del admin de Django
    path('admin/', admin.site.urls),
    # Agregamos la URL para la autenticación de la API
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Agregamos la URL para obtener un token JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # Agregamos la URL para refrescar un token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # Agregamos la URL para imprimir un reporte
    path('reportes/<int:reporte_id>/pdf/',
         ReporteViewSet.as_view ({'get': 'generar_reporte_pdf'}), name='generar_reporte_pdf'),
    # Agregamos la URL para obtener los clientes próximos
    path('clientes/proximos/',
         ClienteViewSet.as_view({'get': 'clientes_proximos'}), name='clientes_proximos'),
    # Agregamos la URL para el panel de clientes
    path('clientes/panel/', ClienteViewSet.panel_clientes, name='panel_clientes'),
    
    path('ventas-mensuales/', ventas_mensuales, name='ventas_mensuales'),
    
    
    
    
    # otras rutas ...

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
