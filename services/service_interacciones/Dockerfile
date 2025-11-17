# 1. Imagen Base 
FROM python:3.12-slim-bookworm

# 2. Variables de entorno 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 3. Instalar dependencias del S.O.
RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# 4. Crear directorio de trabajo
WORKDIR /app

# 5. Copiar e instalar dependencias de Python
COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install gunicorn psycopg2-binary
RUN python -m pip install -r requirements.txt

# 6. Copiar el código del proyecto
COPY . .

# 7. Levantar el puerto
EXPOSE 8000

# 8. Comando de Ejecución
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_interacciones.wsgi:application"]