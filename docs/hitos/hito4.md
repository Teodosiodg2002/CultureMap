# 📋 Hito 4: Composición de Servicios (Docker)

## 🎯 Objetivos del Hito

El objetivo de este hito es tomar la arquitectura de microservicios diseñada en el Hito 3 y desplegarla en un **clúster de contenedores** local usando Docker.

Esto implica "dockerizar" cada servicio (creando un `Dockerfile`) y orquestar el clúster (con un `compose.yaml`) para que todos los servicios se comuniquen entre sí y funcionen como una aplicación cohesiva.

---

## 🔧 1. Justificación de la Infraestructura del Clúster

### 1.1. Contenedor de Base de Datos: PostgreSQL

En el Hito 3, cada servicio usaba su propia base de datos `db.sqlite3`. Para un entorno de producción y de contenedores real, esta solución no es viable.

* **Problema de `sqlite3`**: Es una base de datos basada en un solo archivo, que no maneja bien la concurrencia (múltiples peticiones a la vez) y presenta problemas de bloqueo (`Database is locked`).
* **Decisión Técnica**: Se migrarán todos los servicios a **PostgreSQL**.
* **Justificación**:
    1. **Estándar de Producción**: PostgreSQL es la base de datos relacional de código abierto más utilizada y recomendada para aplicaciones Django en producción.
    2. **Contenedor Exclusivo (Rúbrica)**: La rúbrica pide "un contenedor cuyo contenido exclusivo sea almacenar datos". Implementaremos esto creando **contenedores PostgreSQL separados**, uno para cada microservicio
    3. **Escalabilidad y Fiabilidad**: A diferencia de `sqlite3`, PostgreSQL está diseñado para alta concurrencia y operaciones complejas.

### 1.2. Justificación de la Imagen Base de Docker

La elección de la imagen base para los `Dockerfile` de los servicios es una decisión de arquitectura clave. Se ha realizado un "Estado del Arte" de las opciones más comunes:

1. **Imagen `django` (Oficial de Django):**
    * **Pros:** Es la imagen oficial del proyecto Django. Viene con una versión de Python y Django ya preinstalada y configurada.
    * **Contras:** Como podemos ver en la siguiente imagen, está obsoleta y ella misma te indica usar contenedores python.

![Django Deprecated](../images/django_deprecated.png)

1. **Imagen `python:3.12-alpine` (Minimalista):**
    * **Pros:** Es la imagen más pequeña posible (a menudo < 100MB), lo que la hace muy rápida y segura.
    * **Contras:** Utiliza *Alpine Linux*, conocido por causar fallos de compilación con algunas funcionalidades de Python, especialmente `psycopg2` (PostgreSQL). El riesgo de compatibilidad es alto.

2. **Imagen `python:3.12-slim-bookworm`:**
    * **Pros:** Proporciona un equilibrio ideal. Es la última versión estable de Python (`3.12`) sobre la última versión estable de Debian (`bookworm`) en un formato ligero (`slim`) que mantiene la compatibilidad total de `glibc`.
    * **Contras:** Sigue siendo más grande que `alpine`.

### Decisión Técnica: `python:3.12-slim-bookworm`

Se ha elegido `python:3.12-slim-bookworm` como imagen base para todos los servicios.

**Justificación:** Se descarta `alpine` por los altos riesgos de compatibilidad con `psycopg2`. Se descarta la imagen oficial `django` porque esta obsoleta. La imagen `python:3.12-slim-bookworm` da un control total sobre el entorno: nosotros instalamos `psycopg2-client`, `gunicorn`, y las dependencias de cada `requirements.txt`.

---

## 🚀 2. Implementación de Dockerfiles y Compose

*(...Esta sección se rellenará con el código a medida que se implemente...)*

---

## 🛡️ 3. Implementación de Lógica de Negocio (Roles)

Para cumplir con la visión de la aplicación, se implementará un sistema de roles.

* **`service_usuarios`**: Se modificará el modelo `User` para incluir un campo `rol` (con opciones: `USER`, `ORGANIZADOR`, `ADMIN`).
* **`service_lugares`**: Se implementará un nuevo *endpoint* (`POST /api/catalogo/lugares/<id>/aprobar/`) protegido por permisos de DRF, que solo permitirá el acceso a usuarios con rol `ORGANIZADOR` o `ADMIN`.

---

## 🗓️ 4. Implementación del `service_eventos`

Para completar la funcionalidad de la plataforma, se creará el microservicio `service_eventos`, separado de `service_lugares`.

* **Responsabilidad**: CRUD de eventos con fecha (conciertos, charlas, exposiciones).
* **Implementación**: Se creará un nuevo proyecto Django (`services/service_eventos`) con su `Dockerfile` y su servicio `postgres-eventos` en el `compose.yaml`.

---

## 🌐 5. Interconexión del Frontend

Un objetivo clave de este hito es que la aplicación **funcione de manera interconectada**. El `service_web_frontend` será refactorizado para actuar como un cliente de las APIs de *backend*.

* **Implementación**: Las vistas de `web_frontend` (ej. `index_lugares`) serán modificadas. En lugar de consultar su propia BBDD (`Lugar.objects.all()`), usarán la librería `requests` para llamar a las otras APIs a través de la red interna de Docker (ej. `requests.get('http://service_lugares:8000/api/catalogo/lugares/')`).

---

## 📦 6. Despliegue en GitHub Packages y Tests de CI

*(...Sección para documentar la configuración de CI y los tests de integración del clúster...)*

---

## 📝 7. Implementación del Servicio de Logs

Para cumplir con el requisito de un "servicio de logs separado" y dar visibilidad al clúster, se implementará un stack de agregación de logs.

* **Diseño (Hito 3)**: En el Hito 3, todos los servicios (`web_frontend`, `service_usuarios`, etc.) fueron configurados para emitir sus logs a `stdout` (consola) en formato JSON.
* **Implementación (Hito 4)**: Se añadirá al `compose.yaml` el stack **Loki y Promtail**.
* **Loki**: Actuará como el microservicio de "base de datos de logs", recibiendo y almacenando los logs.
* **Promtail**: Actuará como el "agente colector". Se configurará para descubrir automáticamente los contenedores de los otros servicios y "leer" sus *streams* de `stdout` para enviarlos a Loki.
* **Visualización**: (Opcional, si el tiempo lo permite) Se añadirá un contenedor de **Grafana** al clúster, configurado con Loki como fuente de datos para poder visualizar y buscar en todos los logs de la aplicación desde una única interfaz web.
