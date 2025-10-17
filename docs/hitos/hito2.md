# 📋 Hito 2: Integración Continua (CI)

## 🎯 Objetivos del Hito

El objetivo principal de este hito es implementar **Integración Continua (CI)** en el proyecto. Para ello primero deberemos de tener una serie de funciones básicas en la aplicación para poder probar los test. Por ello, este será el planning para desarrollar el hito2:

1.  **Desarrollar una base para el backend** sobre la cual poder ejecutar los tests.
2.  **Rellenar la base de datos** con datos de prueba.
3.  **Elegir y configurar un gestor de tareas** y un marco de pruebas.
4.  **Escribir tests** para la lógica de negocio principal.
5.  **Configurar un servicio de CI (GitHub Actions)** para que ejecute los tests automáticamente.

---

## 🏗️ Desarrollo del Backend (CRUD Básico)

Antes de comenzar con la ejecución de los test, he creado el modelo `Lugar` donde 

Antes de poder probar la aplicación, he desarrollado las funcionalidades de **leer y listar** para el modelo `Lugar`. Esto nos permite tener una base para poder escribir y probar los test.

### **Vistas y Lógica de Negocio (`views.py`)**

Se han implementado las siguientes vistas principales:

-   **`listar_lugares_todos`**: Muestra una lista de todos los lugares.
-   **`listar_lugares_aprobados`**: Muestra una lista de todos los lugares que han sido aprobados por un administrador y están marcados como publicados. Esto asegura que solo el contenido validado es visible para el público.
-   **`detalle_lugar`**: Muestra la página de detalle de un lugar específico. Utiliza `get_object_or_404` para devolver un error 404 si se intenta acceder a un lugar que no existe o no está aprobado, protegiendo el acceso a contenido no validado.

Se han creado dos vistas para listar los lugares. Un de ellas muestra todos los lugares y la otra, solo muestra aquellos que estan aprobados. Probablemente esto varíe a lo largo del desarrollo de la aplicación, pero de momento lo he implementado para comprobar que se esten ejecutando distintos métodos correctamente.

### **Sistema de Rutas (`urls.py`)**

-   `/lugares/`: Muestra todos los lugares.
-   `/lugares/aprobados/`: Dirige a la lista de lugares públicos.
-   `/lugares/<int:pk>/`: URL dinámica que captura el ID de un lugar y lo pasa a la vista de detalle.

### **Plantillas HTML (`templates`)**

Se han creado las plantillas HTML necesarias para renderizar la información. Estas plantillas no son las definitivas pero sirven para comprobar el correcto funcionamiento de los métodos:

-   `listar_lugares_aprobados.html` y `listar_lugares_aprobados.html`: Usa un bucle `{% for %}` para iterar sobre la lista de lugares y la etiqueta `{% url %}` para generar enlaces dinámicos a la página de detalle.
-   `detalle_lugar.html`: Muestra los atributos del objeto `lugar` que le pasa la vista.

---

##  Añadir Datos

Para facilitar el desarrollo y las pruebas, se ha creado una **migración de datos** (`0002_anadir_datos_iniciales.py`) que rellena la base de datos con un conjunto de lugares de ejemplo en Granada.

**Ventajas de este enfoque:**
-   **Rapidez**: Permite insertar múltiples registros con un solo comando (`python manage.py migrate`).
-   **Consistencia**: Asegura que todos los miembros del equipo (o los sistemas de CI) trabajen con los mismos datos iniciales.
-   **Versionado**: Los datos de prueba están versionados en Git junto con el resto del código.

---

## 🔧 Elección de Herramientas de Testing (En Progreso)


### **1. Gestor de Tareas**

* **Decisión**: `manage.py` de Django.
* **Justificación**: Para un proyecto Django, `manage.py` es la herramienta estándar para ejecutar tareas del proyecto, incluyendo los tests (`python manage.py test`). Integrar un gestor de tareas externo como `make` sería añadir un nivel de complejidad extra y que resulta innecesario. La gestión de dependencias se realiza con `pip` y `requirements.txt`, que es el estándar en el ecosistema de Python.

### **2. Marco de Pruebas y Biblioteca de Aserciones**

* **Decisión**: Framework de testing integrado de Django (`unittest`).
* **Justificación**: *(...pendiente...)*

---

## ⚙️ Integración Continua (CI)

* **Sistema Elegido**: GitHub Actions.
* **Justificación**: *(...pendiente...)*

---

_Documento actualizado el [14/10/2025]_