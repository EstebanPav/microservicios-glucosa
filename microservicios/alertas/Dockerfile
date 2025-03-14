# Usa la imagen base de Python
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .

# Instalar dependencias (IMPORTANTE: instala compilers para psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Exponer el puerto
EXPOSE 5002

# Ejecutar solo el microservicio (SIN RabbitMQ)
CMD ["python", "app.py"]
