# Prototipos de rediseño · tecnobg.com

Sitio estático de presentación con 3 propuestas. No necesita compilación: se sube la carpeta tal cual.

## Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | Portada: botón a la versión final en vivo y las 3 propuestas como referencia |
| `operacion.html` / `operacion-paginas.html` | Propuesta 02 · Operación primero, y sus páginas internas |
| `tecnico.html` / `tecnico-paginas.html` | Propuesta 03 · Ficha técnica, y sus páginas internas |
| `cinematico.html` / `cinematico-paginas.html` | Propuesta 05 · Cinemático, y sus páginas internas |
| `final.html` | Versión final en construcción (base: propuesta 05 + diseño del diseñador) |
| `final-paginas.html` | Páginas internas de la versión final, por `#hash`. Las 4 de servicios ya tienen el diseño del diseñador; Nosotros, Bolsa de trabajo, Blog y legales siguen en diseño preliminar. Se genera con `python3 herramientas/generar-paginas.py` |
| `api/cotizacion.js` | Función de Vercel que envía el formulario de cotización al correo de ventas |
| `fonts/` | Tipografías del diseñador en WOFF2 (Recharge Bold y HP Simplified) |
| `img/` | Logo y fotografías optimizadas (WebP); `img/final/` trae los recursos sacados de los PDF del diseñador (`img/final/servicios/`: páginas de servicios) |
| `robots.txt` | Bloquea la indexación en buscadores |

El CSS y el JavaScript de cada página están dentro de su propio HTML. Las animaciones usan GSAP 3.12.5 desde cdnjs, así que se necesita conexión a internet.

Las páginas internas cambian de sección con el hash de la URL, por ejemplo `operacion-paginas.html#polizas` o `#bolsa-de-trabajo`.

## Botón a la versión final

En `index.html`, al final, cambia `const FINAL_URL = "";` por la URL del sitio final (por ejemplo `"https://tecnobg-final.vercel.app"`). Mientras esté vacía, el botón muestra "Próximamente" y no se puede pulsar.

## Formulario de la versión final

El formulario de `final.html` envía a `/api/cotizacion`, que manda el correo con [Resend](https://resend.com). En Vercel › Settings › Environment Variables agrega:

- `RESEND_API_KEY`: la clave de Resend (obligatoria; sin ella el formulario responde que aún no está conectado).
- `MAIL_FROM`: remitente con el dominio verificado en Resend, por ejemplo `Sitio Tecnobg <sitio@tecnobg.com>`.
- `MAIL_TO`: destinatario (por defecto `ventas@tecnobg.com`).

## Publicar

**Vercel**
1. Sube esta carpeta a un repositorio de GitHub (o usa `vercel` desde la terminal dentro de la carpeta).
2. En Vercel: Add New › Project › importa el repositorio.
3. Framework Preset: **Other**. Sin comando de build. Output directory: la raíz.

**GitHub Pages**
1. Sube la carpeta a un repositorio.
2. Settings › Pages › Source: *Deploy from a branch* › rama `main`, carpeta `/ (root)`.

**Netlify (lo más rápido)**
Arrastra la carpeta completa a https://app.netlify.com/drop.

## Importante

- Todas las páginas llevan `noindex, nofollow` y hay un `robots.txt` que bloquea buscadores. Así el prototipo no compite en Google con tecnobg.com por contenido duplicado. Quítalos solo en el sitio definitivo.
- Los formularios son de demostración: no envían datos.
- Las marcas amarillas "Pendiente" se ocultan con el botón **Pendientes** de la barra superior.
