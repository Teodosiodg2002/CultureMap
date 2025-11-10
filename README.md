# 🗺️ CultureMap

> Plataforma colaborativa para descubrir, proponer y compartir eventos culturales y lugares singulares en un mapa interactivo.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub issues](https://img.shields.io/github/issues/Teodosiodg2002/CultureMap)](https://github.com/Teodosiodg2002/CultureMap/issues)

---

## 📖 Índice

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Problema que Resuelve](#-problema-que-resuelve)
- [Público Objetivo](#-público-objetivo)
- [Arquitectura Cloud](#️-arquitectura-cloud)
- [Documentación de Hitos](#-documentación-de-hitos)
- [Tecnologías](#-tecnologías)
- [Autor](#-autor)

---

## 🎯 Descripción del Proyecto

**CultureMap** es una plataforma web multiusuario que permite explorar, proponer y guardar **eventos culturales** (conciertos, exposiciones, charlas) y **lugares únicos** (miradores, bares con encanto, galerías, tiendas locales) sobre un mapa interactivo.

Combina:
- 📅 Eventos puntuales con fechas concretas
- 📍 Sitios permanentes que merecen ser visitados
- 👥 Los usuarios proponen, validan y sanean el contenido
- 🛡️ Distintos roles y permisos

---

## 🔍 Problema que Resuelve

### **Situación Actual**
Actualmente, cuando se visita cualquier ciudad o pueblo, los sitios para ver o los sitios donde ir **son siempre los mismos**, por lo que se masifican y pierden el encanto que tienen, asi como su esencia. Algunos de los puntos que trata de corregir esta idea son los siguiente:

1. **Eventos pequeños invisibles y en decadencia**: Conciertos en bares, charlas en librerías, exposiciones en galerías pequeñas no aparecen en plataformas grandes  
1. **Sitios auténticos ocultos**: Los mejores miradores, tiendas locales o bares con encanto no están en Google Maps  
1. **Información dispersa**: Instagram, Facebook, carteles, boca a boca... todo separado   
1. **Turismo repetitivo**: Masificación de los sitios turísticos y pérdida de la esencia local  

### **Solución: CultureMap**

- ✅ **Un solo mapa** para descubrir toda la oferta cultural local  (Se centrará en Granada)
- ✅ **Comunidad activa** que propone y valida contenidos  
- ✅ **Dar visibilidad** a organizaciones pequeñas  
- ✅ **Descubrimiento auténtico** de la ciudad 

---

## Público Objetivo

1. **Personas curiosas y turistas responsables**
   - Buscan experiencias locales auténticas
   - Quieren evitar trampas turísticas
   - Valoran la cultura independiente
   - Respetan el entorno y la ciudad que visitan

2. **Organizaciones culturales pequeñas**
   - Pequeños artistas locales
   - Galería de fotos callejera
   - Actos de voluntariado y ayuda pública


3. **Comunidades universitarias**
   - Interesados en compartir y descubrir cultura local
   - Organizadores de eventos comunitarios
   - Estudiantes que buscan planes alternativos

---
## Arquitectura Cloud

Tras el Hito 3, el proyecto ha pasado de tener una arquitectura monolítica (todo en un mismo sitio) a una arquitectura de microservicios bajo un esquema "Monorepo"(un único repositorio).
La aplicación se ha separado en servicios independientes, cada uno con su propio proyecto Django y su propia base de datos.

Los servicios implementados actualmente son:

- **services/web_frontend:** El monolito original del Hito 2, que sirve la interfaz de usuario (mapa, plantillas HTML).
- **services/service_usuarios:** Un microservicio de API (DRF) que gestiona la identidad (registro y login con tokens JWT).
- **services/service_lugares:** Un microservicio de API (DRF) que gestiona el CRUD del catálogo de lugares.
- **services/service_interacciones:** Un microservicio de API (DRF) que gestiona la lógica social (votos, comentarios, etc.).

Esta separación es fundamental para el Hito 4, donde cada servicio se desplegará como un contenedor Docker independiente.

## 📚 Documentación de Hitos

- 📄 [**Hito 1**: Repositorio y Definición del Proyecto](docs/hitos/hito1.md)
- 📄 [**Hito 2**: Integración Continua (CI)](docs/hitos/hito2.md)
- 📄 [**Hito 3**: Diseño de microservicios](docs/hitos/hito3.md)

---

## 🛠️ Tecnologías

Este proyecto cuenta con muchas nuevas tecnologías:

- **Backend y API:** Django y Django REST Framework (DRF).
- **Autenticación de API:** Simple JWT (JSON Web Tokens).
- **Frontend:** Plantillas de Django (HTML) con Bootstrap 5.
- **Mapas:** Leaflet.js.
- **Logging:** python-json-logger (para logs estructurados a stdout).
- **CI/CD:** GitHub Actions (testeando 4 servicios en paralelo).

---

## 👤 Autor

**[Teodosio Donaire González]**  
Estudiante de Máster en Ingeniería Informática  
Universidad de Granada

- GitHub: [@Teodosiodg2002](https://github.com/Teodosiodg2002)
- Email: teodonaire@gmail.com

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 🙏 Agradecimientos

Proyecto desarrollado como parte de la asignatura de **Cloud Computing** del Máster en Ingeniería Informática.

---

_Última actualización: [10/11/2025]_
