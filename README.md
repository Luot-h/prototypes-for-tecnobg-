# Prototipos de rediseño · tecnobg.com

Sitio estático de presentación con 3 propuestas. No necesita compilación: se sube la carpeta tal cual.

## Contenido

| Archivo | Qué es |
|---|---|
| `index.html` | Portada con las 3 propuestas |
| `operacion.html` / `operacion-paginas.html` | Propuesta 02 · Operación primero, y sus páginas internas |
| `tecnico.html` / `tecnico-paginas.html` | Propuesta 03 · Ficha técnica, y sus páginas internas |
| `cinematico.html` / `cinematico-paginas.html` | Propuesta 05 · Cinemático, y sus páginas internas |
| `img/` | Logo y fotografías optimizadas (WebP) |
| `robots.txt` | Bloquea la indexación en buscadores |

El CSS y el JavaScript de cada página están dentro de su propio HTML. Las animaciones usan GSAP 3.12.5 desde cdnjs, así que se necesita conexión a internet.

Las páginas internas cambian de sección con el hash de la URL, por ejemplo `operacion-paginas.html#polizas` o `#bolsa-de-trabajo`.

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
