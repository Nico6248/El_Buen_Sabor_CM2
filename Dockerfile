# Usa una imagen base de Python más reciente
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requerimientos al contenedor
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación al contenedor
COPY . .

# Expone el puerto 8000 para que la aplicación sea accesible
EXPOSE 8000

# Comando para ejecutar la aplicación (se sobreescribe en docker-compose.yml para desarrollo)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
