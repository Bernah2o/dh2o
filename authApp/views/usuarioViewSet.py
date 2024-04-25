from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework import status

from authApp.serializers.usuarioSerializer import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsuarioSerializer

    @action(detail=False, methods=["post"])
    def login(self, request):
        # Obtener credenciales de la solicitud
        username = request.data.get("username")
        password = request.data.get("password")

        # Validar datos de entrada
        if not username or not password:
            return Response(
                {"message": "Nombre de usuario y contraseña son requeridos"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Autenticar al usuario
        user = authenticate(username=username, password=password)

        if user is not None:
            # Iniciar sesión
            login(request, user)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"message": "Credenciales inválidas"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
