# NICHO AI — Website Experience 2026

Sitio web corporativo **multipágina** de NICHO AI, enfocado en desarrollo de sistemas a medida, agentes de inteligencia artificial, automatización de procesos comerciales y desarrollo web avanzado.

## Diseño (v0.2)

Dirección editorial/cinematográfica: negro absoluto, blanco, plata y tipografía monumental. Inspirado por los principios visuales de la referencia *Hyper Tria* aportada por el cliente: escena oscura de marca, espacios blancos de lectura, bloques de composición editorial, transiciones y navegación sencilla. No es un clon de la referencia.

- Página de inicio con elementos cinematográficos optimizados de Envato y secciones interactivas.
- Páginas de Sistemas, Soluciones, Agentes IA, Automatizaciones, Desarrollo web, Metodología, Nosotros y Contacto.
- Demo conceptual interactiva en la home de tres flujos: ventas, atención y operación.
- Diseño responsive, navegación móvil, respeto de `prefers-reduced-motion`, rutas relativas compatibles con GitHub Pages.
- Se eliminan ejemplos de marcas ajenas de la web pública; NICHO y sus capacidades son el enfoque.

## Archivos

- `index.html`: home renovada.
- `soluciones.html`, `sistemas.html`, `agentes-ia.html`, `automatizaciones.html`, `desarrollo-web.html`, `metodologia.html`, `nosotros.html`, `contacto.html`: páginas internas.
- `assets/styles.css`: estilos base.
- `assets/hyper-nicho.css`: sistema editorial y diseño de marca.
- `assets/site.js`: navegación, año y reveals.
- `assets/hyper-nicho.js`: interacción del hero y demo de flujos.
- `assets/media/`: recursos de Envato **transformados para uso web**. Los ZIPs originales/licencias están en Drive, no se publican.
- `ENVATO-RECURSOS-NICHO.md`: registro de recursos y links.

## Preparación para producción

1. Revisar elementos visuales y validar dirección artística.
2. Incorporar logo/identidad oficial aprobada si difiere de la versión tipográfica.
3. Validar licencias para uso online de cada recurso, especialmente tipografías.
4. Completar meta tags, analytics, políticas legales y optimización de accesibilidad.
5. Habilitar GitHub Pages en Settings → Pages → Deploy from branch `main` / root.
6. Solo asociar el dominio principal cuando el sitio haya sido probado y aprobado.

### Desarrollo local
Inicia un servidor de archivos: `python3 -m http.server 8000` y abre `http://localhost:8000`.

Esta es una versión en progreso. Los recursos visuales son de Envato con edición y optimización, las ilustraciones de procesos son demostraciones conceptuales y no datos de clientes.
