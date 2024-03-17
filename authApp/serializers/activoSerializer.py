from rest_framework import serializers

from authApp.models.activo import Activo

class ActivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activo
        fields = "__all__"
