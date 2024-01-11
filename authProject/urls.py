# Importamos los módulos necesarios

from django.contrib import admin
from django.urls import include, path

# Configuramos las URLs
urlpatterns = [
    # Agregamos la URL del admin de Django
    path("admin/", admin.site.urls),
    # Agregamos las URLs del router
    path("", include("authApp.urls")),
]
