# 📋 Hito 1: Repositorio y Definición del Proyecto

## 🎯 Objetivos del Hito

Este primer hito tiene como objetivo:

1. ✅ Configurar correctamente el entorno de desarrollo (Git, GitHub, SSH)
1. ✅ Crear el repositorio del proyecto con estructura profesional
1. ✅ Definir claramente el problema que resuelve CultureMap
1. ✅ Justificar por qué necesita despliegue en la nube
1. ✅ Establecer las historias de usuario (User Stories)
1. ✅ Configurar Issues e Hitos para organizar el trabajo
1. ✅ Documentar las decisiones tomadas

---

## 📦 Estructura del Repositorio

El repositorio sigue una estructura profesional y organizada:

CultureMap/
├── .gitignore              # Archivos ignorados por Git
├── LICENSE                 # Licencia MIT del proyecto
├── README.md               # Documentación principal del proyecto
└── docs/                   # Documentación adicional
├── hitos/
│   └── hito1.md       # Este documento
├── images/            # Capturas de pantalla y diagramas
├── arquitectura/      # Documentación técnica de arquitectura
│   └── diagrama_arquitectura.md
└── configuracion_entorno.md  # Guía de configuración

---

## 🔧 Configuración del Entorno

### **Git y GitHub**

Se ha configurado correctamente el entorno de desarrollo:

✅ **Git configurado localmente**
- Nombre de usuario configurado
- Email configurado
- Editor por defecto establecido

✅ **Claves SSH generadas y añadidas a GitHub**
- Par de claves ED25519 generado
- Clave pública añadida a GitHub
- Conexión SSH verificada correctamente

✅ **Perfil de GitHub completado**

✅ **Autenticación de dos factores (2FA) activada**
- Mayor seguridad en la cuenta
- Códigos de recuperación guardados

📸 **Evidencias**: Ver [Configuración del Entorno](../configuracion_entorno.md)

---

## 🎯 Definición del Problema

### **Problema Identificado**

Los sitios a visitar en Granada (y en general) son siempre los mismos, y para encontrar nuevos, es necesario buscar entre muchas páginas  

❌ **Eventos pequeños e invisibles**: Conciertos en bares, exposiciones en galerías pequeñas, charlas en espacios culturales no aparecen en plataformas grandes

❌ **Sitios auténticos ocultos**: Miradores únicos, bares con encanto, tiendas locales, arte urbano... no están bien documentados

❌ **Información dispersa**: Los eventos culturales están repartidos en Instagram, Facebook, carteles físicos, boca a boca

❌ **Turismo masificado**: Los turistas siempre terminan en los mismos lugares (Alhambra, Albaicín), perdiendo la esencia local de barrios como Realejo, Zaidín o Chana

❌ **Difícil descubrir eventos universitarios**: La Universidad de Granada tiene mucha actividad cultural (conferencias, exposiciones, música) que no se visibiliza bien

### **Solución Propuesta: CultureMap**

Una plataforma web colaborativa que:

✅ **Centraliza** toda la oferta cultural de Granada en un solo mapa interactivo

✅ **Da fuerza a la comunidad** para proponer y validar contenidos (sitios y eventos)

✅ **Diferencia contenido temporal y permanente**:
- **Eventos**: Conciertos, exposiciones, charlas (con fecha de inicio/fin)
- **Sitios**: Miradores, bares, galerías, tiendas (permanentes)

✅ **Sistema de roles**:
- **Administradores**: Moderan contenido
- **Organizadores**: Grupos culturales que publican directamente
- **Usuarios**: Proponen sitios/eventos, votan, comentan
- **Visitantes**: Consultan el mapa sin necesidad de registrarse

✅ **Funcionalidades sociales**:
- Guardar favoritos
- Comentar y valorar sitios/eventos
- Compartir descubrimientos
- Valorar y puntuar los lugares y/o eventos

---

## ☁️ Justificación del Despliegue en la Nube

CultureMap **necesita la nube** por las siguientes razones:

### **1. Naturaleza Multiusuario y Colaborativa**
- Múltiples usuarios crean contenido simultáneamente
- Sincronización en tiempo real del mapa
- Gestión de permisos y roles

### **1. Alta Disponibilidad y Accesibilidad**
- Acceso 24/7 desde web y móvil
- Usuarios acceden desde diferentes ubicaciones
- No puede caerse durante eventos importantes
- **Necesita**: Load Balancer, Multi-AZ deployment

### **1. Escalabilidad según Demanda**
- Crecimiento progresivo de usuarios

### **1. Backup y Recuperación**
- Datos comunitarios valiosos (contenido generado por usuarios)
- Necesidad de backups automáticos
- **Necesita**: Snapshots automáticos, Replicación de BD

---

## 📊 Lógica de Negocio

CultureMap **no es un simple CRUD**. Incluye lógica de negocio compleja:

### **1. Moderación y Calidad de Contenido**
- **Flujo de aprobación**: cada propuesta (evento o sitio) pasa de Pendiente a Aprobado/Rechazado por parte de moderadores u organizadores.
- **Priorización de contenidos**: Sitios con más votos aparecen primero
- **Detección de duplicados**: Evitar que se propongan sitios repetidos
- **Sistema de reportes**: Usuarios pueden reportar contenido inapropiado

### **2. Gestión Temporal de Eventos**
- **Auto-archivado**: Eventos pasados se ocultan del mapa automáticamente
- **Recordatorios**: Notificaciones X días antes del evento
- **Eventos recurrentes**: soporte para actividades que se repiten de forma periódica (ej. “Todos los jueves, mercadillo cultural”).

### **3. Gamificación**
- **Sistemas de reputación**: los usuarios que más contribuyen con propuestas aprobadas ganan puntos de reputación.
- **Logros y badges**: reconocimiento simbólico (“Explorador local”, “Cazador de eventos”).
- **Ranking de usuarios activos**: refuerza la motivación y la sensación de comunidad.


---

## 👥 Historias de Usuario (User Stories)

Las historias de usuario están organizadas por **Épicas** (grupos funcionales):

### **Épica 1: Autenticación y Gestión de Usuarios**

**US-01**: Como usuario nuevo, quiero registrarme con email y contraseña para poder participar en la comunidad.

**US-02**: Como usuario registrado, quiero iniciar sesión para acceder a mis funcionalidades.

**US-03**: Como administrador, quiero asignar roles a usuarios (ej. organizadores) para dar permisos especiales.

### **Épica 2: Gestión de Sitios Culturales**

**US-04**: Como usuario, quiero proponer un nuevo sitio cultural para compartirlo con la comunidad

**US-05**: Como administrador, quiero aprobar o rechazar sitios propuestos para mantener la calidad del mapa.

**US-06**: Como visitante, quiero ver todos los sitios aprobados en el mapa para descubrir lugares

**US-07**: Como usuario, quiero filtrar sitios por categoría para encontrar lo que busco
---

### **Épica 3: Interacción Social**

**US-08**: Como usuario, quiero guardar sitios como favoritos para visitarlos después

**US-9**: Como usuario, quiero comentar en un sitio para compartir mi experiencia

**US-10**: Como usuario, quiero comentar en un sitio para compartir mi experiencia con la comunidad.

---

### **Épica 4: Eventos Temporales** (Fase 2)

**US-11**: Como organizador, quiero publicar un evento cultural para darle visibilidad

**US-12**: Como usuario, quiero ver eventos próximos en el mapa para planificar mi agenda

**US-13**: Como usuario, quiero recibir notificaciones de eventos cerca de mis sitios favoritos

---

### **Épica 5: Búsqueda y Descubrimiento**

**US-14**: Como usuario, quiero buscar sitios por nombre o categoría para localizarlos fácilmente.

---

## 🎯 Producto Mínimo Viable (MVP)

### **Definición del MVP**

El MVP de CultureMap incluye las funcionalidades **mínimas e indispensables** para validar el concepto:

**Incluido en MVP (Fases 1-2)**:
✅ Autenticación básica (registro/login)
✅ Roles: Admin y Usuario (sin Organizador todavía)
✅ CRUD de Sitios culturales
✅ Mapa interactivo con Leaflet
✅ Sistema de moderación (aprobar/rechazar)
✅ Favoritos
✅ Comentarios y votos
✅ Filtros por categoría

**NO incluido en MVP** (se añadirá después):
❌ Eventos temporales
❌ Notificaciones push
❌ Sistema de recomendaciones
❌ Heatmap
❌ Rutas culturales
❌ Rol "Organizador"

---

## 📋 Issues y Milestones

### **Milestones Configurados**

Los hitos del proyecto están organizados en GitHub Milestones:

1. **Milestone 1**: Hito 1 - Repositorio de pácticas y definición del proyecto. (actual)
   - Fecha límite: [tu fecha]
   - Issues: #1, #2, #3

2. **Milestone 2**: Integración continua
   - Fecha límite: +2 semanas
   - Issues pendientes de crear

3. **Milestone 3**: Frontend + Mapa Interactivo
   - Fecha límite: +4 semanas

4. **Milestone 4**: Deploy en Cloud + CI/CD
   - Fecha límite: +6 semanas

5. **Milestone 5**: Features Avanzadas
   - Fecha límite: +8 semanas

### **Issues Creados para el Hito 1**

Los siguientes Issues han sido creados y asignados al Milestone 1:

- **#1**: Configurar entorno Git y GitHub (SSH, 2FA, perfil) ✅ CERRADO
- **#2**: Crear estructura del repositorio y documentación ✅ CERRADO
- **#3**: Redactar README con descripción del problema
- **#4**: Definir User Stories y asignarlas a Issues
- **#5**: Crear diagrama de arquitectura cloud
- **#6**: Documentar configuración del entorno

---

## 🏗️ Decisiones Técnicas

***(En proceso)***

### **Licencia del Proyecto**

Se ha elegido **MIT License** porque:
- ✅ Permite uso comercial y modificación
- ✅ Es la más usada en proyectos open source
- ✅ Fomenta la colaboración

---

## 📸 Evidencias

### **Configuración del Entorno**

Todas las capturas de pantalla están en: [`docs/configuracion_entorno.md`](../configuracion_entorno.md)

Incluyen:
- ✅ Git config global
- ✅ Claves SSH en GitHub
- ✅ Perfil de GitHub completado
- ✅ 2FA activado

---

## ✅ Checklist de Completitud del Hito 1

- [✅] Repositorio creado en GitHub
- [✅] README.md completo con descripción del problema
- [✅] LICENSE (MIT) añadida
- [✅] .gitignore configurado
- [✅] Estructura de carpetas profesional (`docs/`, `docs/hitos/`, etc.)
- [✅] Git configurado localmente (nombre, email)
- [✅] Claves SSH generadas y añadidas a GitHub
- [✅] Perfil de GitHub completado (foto, bio, ubicación)
- [✅] 2FA activado en GitHub
- [✅] Documentación de configuración del entorno
- [✅] User Stories definidas y documentadas
- [x] Issues creados y asignados a Milestones
- [x] Commits descriptivos y bien formateados
- [✅] Justificación clara del despliegue en la nube
- [✅] Lógica de negocio explicada (más allá de CRUD)

---

_Documento completado el [3/10/2025]_