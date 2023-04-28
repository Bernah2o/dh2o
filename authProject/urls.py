from django.contrib import admin
from django.urls import include, path

from rest_framework import routers




#creacion de API
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
from authApp.views.mpagoViewSet import MpagoViewSet
from authApp.views.detalleFacturaViewSet import DetalleFacturaViewSet



from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp import views
from authApp.views.views import alerta_limpieza


router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'operadores', OperadorViewSet)
router.register(r'mpagos', MpagoViewSet)
router.register(r'detalles-factura', DetalleFacturaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
