# NICHO Academy: rutas que deben conservarse

Restauración del 26 de octubre de 2026 a partir del HTML `nicho_academy_whatsapp_api.html` del 1 de septiembre de 2026 y del PDF original `GUIA WHATSAPP API .pdf` (30 páginas).

- Curso: `/curso-basico-de-como-integrar-tu-api/`.
- Guía: `/wp-content/uploads/2026/09/GUIA-WHATSAPP-API-.pdf`.

Estos archivos pertenecían al sitio anterior y no estaban en el repositorio migrado. El diseño, contenido, playlists y funcionamiento de acceso del HTML recuperado se conservan. Solo se añaden canonical y noindex; el centro de capacitación no se incluye en el sitemap comercial. El PDF se conserva byte por byte.

No sustituir estas rutas por la página comercial de WhatsApp API ni por la portada. `tools/check_site.py` exige su presencia, incluso si dejan de estar enlazadas desde otras páginas. Los generadores de contenido no deben eliminarlas.

El control de acceso conserva la implementación original en JavaScript y sessionStorage; no es autenticación en servidor. No usar esta recuperación como prueba de seguridad del contenido.
