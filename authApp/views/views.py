# msm/views.py
from django.shortcuts import render
import pywhatkit as pwk
import datetime

def enviar_mensaje(request):
    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        mensaje = request.POST.get('mensaje')

        # Agregar el prefijo "+57" al número de teléfono si no lo tiene
        if not telefono.startswith('+57'):
            telefono = '+57' + telefono

        # Obtener la hora y el minuto actuales
        now = datetime.datetime.now()
        hora = now.hour
        minuto = now.minute + 1  # Sumamos 1 minuto para que el mensaje se envíe en el próximo minuto

        # Enviar el mensaje utilizando pywhatkit
        try:
            pwk.sendwhatmsg(telefono, mensaje, hora, minuto)
            return render(request, 'exito.html', {'telefono': telefono, 'mensaje': mensaje})
        except Exception as e:
            return render(request, 'error.html', {'mensaje': f'Error al enviar el mensaje: {str(e)}'})

    return render(request, 'enviar_mensaje.html')


def index(request):
    # Código de la vista index (página principal)
    return render(request, 'index.html')
