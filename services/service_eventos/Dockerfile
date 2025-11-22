FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y --no-install-recommends postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN python -m pip install gunicorn psycopg2-binary
RUN python -m pip install -r requirements.txt

COPY . .

EXPOSE 8000

# Cambiamos el nombre del proyecto a 'service_eventos'
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "service_eventos.wsgi:application"]