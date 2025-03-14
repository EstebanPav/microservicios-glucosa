# Usa la imagen base de Python
FROM python:3.12-slim

# Instala las dependencias de PostgreSQL para conectar con psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    pip install --upgrade pip

# Crea el directorio de trabajo
WORKDIR /app

# Copia todos los archivos al contenedor
COPY . .

# Instala las dependencias desde requirements.txt
RUN pip install -r requirements.txt

# ✅ Ejecuta el script SQL para crear las tablas
# Usa las variables de entorno para autenticación automática
ENV PGPASSWORD=password
RUN apt-get install -y postgresql-client && \
    psql -h postgres-db -U user -d glucosa_db -f /app/sql/init.sql || true

# Expone el puerto 5000
EXPOSE 5000

# Comando para correr el servicio
CMD ["python", "app.py"]
