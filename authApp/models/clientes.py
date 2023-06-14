from django.db import models
from datetime import timedelta
from django.utils import timezone
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys



class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    cedula = models.IntegerField(unique=True, null=True, blank=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=11, unique=True)
    correo = models.EmailField(max_length=100, blank=True)
    creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.CharField(max_length=200, blank=True) 
    ultima_limpieza = models.DateField(null=True, blank=True) # Fecha de última limpieza
    proxima_limpieza = models.DateField(null=True, blank=True) # Fecha de próxima limpieza
      
   
    def __str__(self):
        texto = "{0} {1}"
        return texto.format(self.nombre,self.apellido)    
        
      
    @staticmethod   
    def proximas_limpiezas(self):
        """Retorna una lista de clientes que tienen próxima limpieza"""
        hoy = timezone.now().date() # Fecha actual
        proximos = [] # Lista de clientes con próxima limpieza
        for cliente in Cliente.objects.all(): # Iterar sobre todos los clientes
            if cliente.proxima_limpieza and cliente.proxima_limpieza <= hoy:
                proximos.append(cliente) # Agregar el cliente a la lista si su próxima limpieza es anterior o igual a la fecha actual
        return Cliente.objects.filter(proxima_limpieza__lte=hoy)            
           
    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper() # Convertir el nombre a mayúsculas antes de guardar
        self.apellido = self.apellido.upper() # Convertir el apellido a mayúsculas antes de guardar
        self.direccion = self.direccion.upper() # Convertir la dirección a mayúsculas antes de guardar
        
        if self.ultima_limpieza:
            # Calcular fecha de próxima limpieza
            frecuencia_meses = 6 # Frecuencia de limpieza en meses, cambiar según necesidades
            delta_meses = timedelta(days=30*int(frecuencia_meses)) # Duración en días de la frecuencia de limpieza
            self.proxima_limpieza = self.ultima_limpieza + delta_meses # Calcular la fecha de próxima limpieza
            
        super().save(*args, **kwargs)
        
        
        
        
"""    
def enviar_whatsapp(clientes, mensaje):
    # Inicializar el navegador Google Chrome con el controlador de selenium
    driver = webdriver.Chrome('D:\MINTIC\PROGRAMACION\CICLO 3\BACKEND\driver\chromedriver.exe')

    # Abrir WhatsApp Web en una nueva pestaña
    driver.execute_script("window.open('https://web.whatsapp.com');")
    driver.switch_to.window(driver.window_handles[-1])

    for cliente in clientes:
        # Buscar el chat del número de teléfono especificado
        search_box = driver.find_element_by_xpath('//div[@class="_2S1VP copyable-text selectable-text"]')
        search_box.send_keys(cliente.telefono)
        time.sleep(2)
        search_box.submit()

        # Esperar a que el chat se abra
        time.sleep(2)

        # Escribir el mensaje y enviarlo
        message_box = driver.find_element_by_xpath('//div[@class="_3uMse"]')
        message_box.send_keys(mensaje)
        
        # Presionar la tecla Enter para enviar el mensaje
        message_box.send_keys(Keys.ENTER)
        
        # Esperar unos segundos para asegurarnos de que el mensaje se haya escrito completamente
        time.sleep(2)   

    # Cerrar el navegador
    driver.quit()
    """
    
   
        
        
  
    
    
    
        
    
    

