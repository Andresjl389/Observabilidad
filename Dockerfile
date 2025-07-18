FROM python:3.10-slim

# Instala bash y curl
RUN apt-get update && apt-get install -y bash curl && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copia solo requirements primero (mejor caché)
COPY requirements.txt .

# Instala dependencias
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copia todo el código
COPY . .

# Variables de entorno
ENV PYTHONPATH=/app
ENV PORT=8080

# Exponer puerto para Cloud Run
EXPOSE 8080

# Descargar wait-for-it
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /wait-for-it.sh && chmod +x /wait-for-it.sh

# Comando de inicio
CMD [ "sh", "-c", "/wait-for-it.sh $DB_HOST:$DB_PORT -- alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT" ]
