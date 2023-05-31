# Selecciona una imagen base adecuada
FROM python:3.9

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install -r requirements.txt

# Copia el código de la aplicación al contenedor
COPY . /app

# Expone el puerto en el que tu aplicación escucha
EXPOSE 8000

# Define las variables de entorno (si es necesario)
# ENV VARIABLE1 valor1
# ENV VARIABLE2 valor2



# Comando de inicio de la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
