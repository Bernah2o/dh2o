from rest_framework import serializers
from authApp.models.user import User
from authApp.models.clientes import Cliente
from authApp.serializers.clientesSerializer import ClienteSerializer
""""
from authApp.models.account import Account
from authApp.serializers.accountSerializer import AccountSerializer
"""
class UserSerializer(serializers.ModelSerializer):
    clientes = ClienteSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'name', 'email', 'cliente']

    def create(self, validated_data):
        accountData = validated_data.pop('clientes')
        userInstance = User.objects.create(**validated_data)
        Cliente.objects.create(user=userInstance, **accountData)
        return userInstance

    def to_representation(self, obj):
        user = User.objects.get(id=obj.id)
        clientes = Cliente.objects.get(user=obj.id)       
        return {
                    'id': user.id, 
                    'username': user.username,
                    'name': user.name,
                    'email': user.email,
                    'cliente': {
                        'id': clientes.id,
                        'balance': clientes.balance,
                        'lastChangeDate': clientes.lastChangeDate,
                        'isActive': clientes.isActive
                    }
                }