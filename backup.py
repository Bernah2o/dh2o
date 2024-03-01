import os
import subprocess
from datetime import datetime

# Definir las variables de entorno para la base de datos
os.environ["PGPASSWORD"] = "Mateo2023"
os.environ["PGUSER"] = "postgres"
os.environ["PGHOST"] = "127.0.0.1"
os.environ["PGPORT"] = "5432"
os.environ["PGDATABASE"] = "bd_dh2o"

# Ruta donde se guardarán los archivos de respaldo
backup_path = r"D:\Fondo Emprender\Lavado de Tanques\APP\BackupBD"

# Nombre del archivo de respaldo (incluyendo la fecha y hora actual)
backup_filename = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"

# Crear la ruta completa del archivo de respaldo
backup_file_path = os.path.join(backup_path, backup_filename)

# Comando para realizar el respaldo usando pg_dump
pg_dump_command = [
    "pg_dump",
    "-U",
    os.environ["PGUSER"],
    "-h",
    os.environ["PGHOST"],
    "-p",
    os.environ["PGPORT"],
    os.environ["PGDATABASE"],
]

try:
    # Abrir el archivo de respaldo para escritura
    with open(backup_file_path, "w") as backup_file:
        # Ejecutar el comando de respaldo y redirigir la salida al archivo
        subprocess.run(pg_dump_command, stdout=backup_file, check=True)
        print("Backup realizado exitosamente:", backup_file_path)
except subprocess.CalledProcessError as e:
    print("Error al hacer el backup:", e)
