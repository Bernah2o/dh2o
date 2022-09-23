"""authProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

#creacion de API
from authApp.views.clienteViewSet import ClienteViewSet
from authApp.views.facturaViewSet import FacturaViewSet
from authApp.views.servicioViewSet import ServicioViewSet
from authApp.views.operadorViewSet import OperadorViewSet
#ejemplo de banco

from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp import views


urlpatterns = [
    
    path('admin/',admin.site.urls),
    
    #path('person/list',ClienteViewSet.as_view({'get':'list'})),
    #path('factura/list',FacturaViewSet.as_view({'get':'list'})),
    #path('servicio/list',ServicioViewSet.as_view({'get':'list'})),
    #path('operador/list',OperadorViewSet.as_view({'get':'list'})),
    
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('user/', views.UserCreateView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    ]


