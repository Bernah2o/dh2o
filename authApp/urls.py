# Importamos los módulos necesarios
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework import permissions
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import views as auth_views
from authApp.views.activoViewSet import ActivoViewSet
from authApp.views.loginViewSet import LoginView
from rest_framework.routers import DefaultRouter

# Importamos las vistas necesarias
from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.ordendetrabajoViewsSet import OrdenDeTrabajoViewSet
from authApp.views.reporteViewsSet import ReporteViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
from authApp.views.mpagoViewSet import MpagoViewSet
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.productoViewSet import ProductoViewSet, reporte_productos_view

# Importaciones para swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from authApp.views.usuarioViewSet import UsuarioViewSet


# Definimos nuestro router para manejar todas las vistas de la API
router = DefaultRouter()
router.register(r"clientes", ClienteViewSet, "clientes")
router.register(r"facturas", FacturaViewSet, "facturas")
router.register(r"servicios", ServicioViewSet, "servicios")
router.register(r"operadores", OperadorViewSet, "operadores")
router.register(r"mpagos", MpagoViewSet, "mpagos")
router.register(r"ordenesdetrabajo", OrdenDeTrabajoViewSet, "ordenesdetrabajo")
router.register(r"reportes", ReporteViewSet, "reportes")
router.register(r"producto", ProductoViewSet, "producto")
router.register(r"activo", ActivoViewSet, "activo")
router.register(r"usuarios", UsuarioViewSet, "usuarios")


# Personalizacion del panel de admin
admin.site.site_header = "Bienvenido"
admin.site.site_title = "www.dh2o.com"
admin.site.index_title = "Bienvenido a Dh2o"

# Configuracion Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Dh2oCol",
        default_version="v1",
        description="Test description",
        terms_of_service="https://dh2o.com.co/",
        contact=openapi.Contact(email="dh2ovpar@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Configuramos las URLs
urlpatterns = [
    path("api/", include(router.urls)),
    # Agregamos la URL para la autenticación de la API
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # Agregamos la URL para obtener un token JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Agregamos la URL para refrescar un token JWT
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Agregamos la URL para imprimir un reporte
    path(
        "reportes/<int:pk>/pdf/",
        ReporteViewSet.as_view({"get": "generar_pdf"}),
        name="generar_reporte_pdf",
    ),
    # Agregamos la URL para ventas mensuales
    path(
        "ventas-mensuales/",
        FacturaViewSet.as_view({"get": "ventas_mensuales"}),
        name="ventas_mensuales",
    ),
    # Agregamos la URL para comisiones
    path(
        "comisiones/<int:pk>/",
        OrdenDeTrabajoViewSet.calcular_comision_view,
        name="authApp_ordendetrabajo_comisiones",
    ),
    # URL para solicitar la recuperación de contraseña
    path(
        "reset_password/", auth_views.PasswordResetView.as_view(), name="reset_password"
    ),
    # URL para mostrar el mensaje de éxito después de enviar la solicitud de recuperación de contraseña
    path(
        "reset_password_done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    # URL para confirmar el restablecimiento de contraseña
    path(
        "reset_password_confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # URL para mostrar el mensaje de éxito después de restablecer la contraseña
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    # Api para login html
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LoginView.as_view(), name="logout"),
    # Api para UsuarioLogin de angular
    # Api para Swagger
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redocs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Generar factura en html
    path(
        "generar_factura/<int:pk>/",
        FacturaViewSet.generar_factura,
        name="generar_factura",
    ),
    # Generar informe de productos en html
    path("reporte-productos/", reporte_productos_view, name="reporte_productos"),
    path(
        "ordenes-de-trabajo/<int:orden_de_trabajo_id>/reportes/",
        ReporteViewSet.as_view({"post": "create"}),
        name="crear-reporte",
    ),
    # path("login/",UsuarioViewSet.as_view({"post": "login"}),name="usuario-login",),
    # otras rutas ...
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# Rutas
