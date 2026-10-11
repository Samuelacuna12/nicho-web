# NICHO AI — SEO y publicación

## Estado
SEO **implementado en el repositorio**. Falta confirmar dominio, desplegar en producción y configurar Search Console; no se garantiza posicionamiento ni indexación.

## Implementado
- 15 URLs con títulos, metas, canonicals, Open Graph y Twitter.
- Datos estructurados JSON-LD: Organization/WebSite (inicio), Service (servicios), Article (guías) y BreadcrumbList (internas).
- `sitemap.xml` y `robots.txt` preparados para `https://nichoagenciadigital.com`.
- Enlaces internos, secciones FAQ visibles y tres guías originales; sin testimonios ni direcciones inventadas.
- Noindex temporal por JavaScript para staging en github.io; el dominio de producción permanece como canónico.
- Error 404 con navegación útil.

## Antes de activar el dominio
1. Confirmar cuál será la URL canónica (con www o sin www). Configurar 301 entre variantes del host.
2. Exportar/inventariar URLs del sitio anterior y redirigir antiguas rutas mediante 301 individual a su equivalente (no todas al inicio).
3. Revisar enlaces y comprobar respuestas HTTP, HTTPS y certificados desde hosting real.
4. Verificar `https://nichoagenciadigital.com` en Google Search Console; enviar `https://nichoagenciadigital.com/sitemap.xml`.
5. Conectar analítica respetando políticas de privacidad y consentimiento; configurar conversiones de agenda.
6. Validar schema con Rich Results Test, Core Web Vitals y PageSpeed Insights desde el dominio definitivo.
7. Completar contacto, identidad de marca y enlaces sociales solo con datos verificados.
8. Crear calendario editorial basado en consultas reales y revisar Search Console mensualmente.
9. Si hay una sede real, verificar Google Business Profile y solo entonces considerar LocalBusiness con datos auténticos.

## Palabras/temas objetivo
- Desarrollo de software a medida Colombia: `sistemas.html`.
- CRM personalizado: `crm-personalizado.html`.
- Agentes IA para ventas: `agentes-ia.html`.
- Automatización de ventas: `automatizaciones.html`.
- WhatsApp API para empresas: `whatsapp-api-empresas.html`.
- Desarrollo web profesional: `desarrollo-web.html`.
- Contenido educativo: `recursos/`.

## Fuentes
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=es
- https://developers.google.com/search/docs/appearance/structured-data/organization
- https://developers.google.com/search/docs/appearance/core-web-vitals
