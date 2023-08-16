from authApp.models.operador import Operador
from rest_framework import serializers


class OperadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operador
        fields = "__all__"
