# Importamos los módulos necesarios
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers, permissions
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from authApp.views.loginViewSet import LoginView
from authApp.views import views

# Importamos las vistas necesarias
from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.ordendetrabajoViewsSet import OrdenDeTrabajoViewSet, CalcularComisionView
from authApp.views.reporteViewsSet import ReporteViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
from authApp.views.mpagoViewSet import MpagoViewSet
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.productoViewSet import ProductoViewSet


#Importaciones para swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Definimos nuestro router para manejar todas las vistas de la API
router = routers.DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'facturas', FacturaViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'operadores', OperadorViewSet)
router.register(r'mpagos', MpagoViewSet)
router.register(r'ordenesdetrabajo', OrdenDeTrabajoViewSet)
router.register(r'reportes', ReporteViewSet)
router.register(r'producto', ProductoViewSet)

# Personalizacion del panel de admin
admin.site.site_header = 'Bienvenido'
admin.site.site_title = 'www.dh2o.com'
admin.site.index_title = 'Bienvenido a Dh2o'

#Configuracion Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="API Dh2oCol",
      default_version='v1',
      description="Test description",
      terms_of_service="https://dh2ocol.my.canva.site",
      contact=openapi.Contact(email="dh2ovpar@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

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
    path('reportes/<int:reporte_id>/pdf/',ReporteViewSet.as_view ({'get': 'generar_reporte_pdf'}), name='generar_reporte_pdf'),
    #path('reportes/<int:id_reporte>/pdf/', ReporteViewSet.as_view({'get': 'generar_reporte_pdf'}), name='generar_reporte_pdf'),
    # Agregamos la URL para obtener los clientes próximos
    path('clientes/proximos/',
         ClienteViewSet.as_view({'get': 'clientes_proximos'}), name='clientes_proximos'),
    # Agregamos la URL para el panel de clientes
    path('clientes/panel/', ClienteViewSet.panel_clientes, name='panel_clientes'),
    # Agregamos la URL para ventas mensuales
    path('ventas-mensuales/', FacturaViewSet.as_view({'get': 'ventas_mensuales'}), name='ventas_mensuales'),
    
    # Agregamos la URL para comisiones
    #path('comisiones/<int:pk>/', OrdenDeTrabajoViewSet.as_view({'get': 'calcular_comision'}), name='authApp_ordendetrabajo_comisiones'),
    path('comisiones/<int:pk>/', CalcularComisionView.as_view(), name='authApp_ordendetrabajo_comisiones'), 
          
    # URL para solicitar la recuperación de contraseña
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),

    # URL para mostrar el mensaje de éxito después de enviar la solicitud de recuperación de contraseña
    path('reset_password_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # URL para confirmar el restablecimiento de contraseña
    path('reset_password_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # URL para mostrar el mensaje de éxito después de restablecer la contraseña
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LoginView.as_view(), name='logout'),
    #Api para Swagger
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    #Generar factura en html
    path('generar_factura/<int:pk>/', FacturaViewSet.generar_factura, name='generar_factura'),
    
    path('enviar-mensaje/', views.enviar_mensaje, name='enviar_mensaje'),
    path('', views.index, name='index'),
    
    
    
   
    # otras rutas ...

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#Rutas