# SEO y lanzamiento — Nicho Agencia Digital

## Implementado en la entrega
24 rutas conservadas, HTML visible sin JavaScript, un H1 por página, títulos y descripciones únicos, canonical al dominio oficial, sitemap con rutas reales, robots.txt, imágenes con dimensiones, navegación por teclado, textos alternativos y metadatos sociales con imagen 1200 × 630.

Los datos estructurados describen Organization y WebSite en inicio, páginas y migas de pan, Service en servicios, Article en guías y CreativeWork en casos. No se incluyen calificaciones, testimonios, precios, horarios o coordenadas no verificados. No se usa el marcado como promesa de resultados enriquecidos.

## Arquitectura de intención de búsqueda

| Página | Tema y propósito |
|---|---|
| Inicio | Nicho Agencia Digital; software e inteligencia aplicada a empresas |
| sistemas.html | Desarrollo de software empresarial a medida |
| crm-personalizado.html | CRM y gestión comercial personalizados |
| agentes-ia.html | Agentes IA para atención y ventas |
| automatizaciones.html | Automatización de procesos y seguimiento comercial |
| desarrollo-web.html | Webs corporativas, plataformas e interfaces |
| whatsapp-api-empresas.html | Integraciones de WhatsApp con procesos empresariales |
| bucaramanga.html | Presencia real de Nicho en Bucaramanga |
| portafolio/ | Seis estudios de caso con contexto, alcance, módulos y estado |
| recursos/ | Tres guías de decisión enlazadas con casos concretos |

No se multiplicaron páginas casi idénticas para ciudades sin evidencia local.

Los temas son una propuesta editorial; no se han medido volúmenes de búsqueda ni dificultad de palabras clave. Para priorizar inversión hacen falta las consultas y conversiones de Search Console y analítica.

## La parte que no se obtiene solo escribiendo código
Google no garantiza rastreo, indexación ni posiciones. El SEO necesita un dominio accesible, contenido original con evidencia, enlaces legítimos y revisión de lo que realmente encuentran los usuarios. La guía oficial de Google para sus experiencias generativas mantiene esa base: contenido útil y estructura técnica clara; no recomienda atajos como archivos llms.txt innecesarios o menciones artificiales.

El siguiente paso editorial más valioso es sustituir las pantallas ilustrativas por capturas o grabaciones autorizadas de sistemas reales y documentar resultados verificables. Hasta entonces las visualizaciones permanecen identificadas como demostraciones; no se presentan métricas ficticias como prueba.

## Antes de publicar
1. Guardar una copia del repositorio actual y comprobar la revisión base. El paquete incluye un publicador que se detiene si `main` cambió desde la revisión examinada.
2. Publicar primero una vista de prueba, verificar enlaces, diseño, videos, 404 y datos de contacto.
3. Mantener `CNAME` y el dominio `nichoagenciadigital.com`. Esta entrega conserva las 24 rutas del sitio existente. Si quedan URLs anteriores de Hostinger, inventariarlas y definir una redirección real a su equivalente. No sustituirlas por redirecciones masivas a inicio.
4. Comprobar HTTPS y la opción Enforce HTTPS en GitHub Pages. No cambiar DNS de nuevo solo por esta actualización de diseño.
5. Confirmar que la página principal responde 200; una ruta inexistente debe responder 404, no 200.
6. Verificar que producción no tiene `noindex` y que `robots.txt` y `sitemap.xml` se sirven correctamente. La lógica de noindex solo se aplica a hosts temporales github.io/pages.dev.
7. Validar Organization, Article y BreadcrumbList con las herramientas de Google. `Service` no implica un resultado enriquecido especial.

## Search Console
Verificar la propiedad del dominio por DNS usando el valor que Google genere. No borrar TXT de otros servicios. Enviar `https://nichoagenciadigital.com/sitemap.xml`, inspeccionar inicio, un servicio y un caso. Revisar páginas excluidas, consultas, impresiones, clics y conversiones de negocio. No usar el API de indexación de Google para URLs comerciales genéricas.

## Analítica y conversiones
`assets/js/config.js` contiene `ga4MeasurementId: ''`. La analítica está apagada hasta que se introduzca un ID real y el visitante autorice su uso. No hay un ID ficticio ni se instaló una herramienta sin autorización.

Eventos disponibles: clic en WhatsApp, correo y agenda, filtro de proyectos, etapa de la demostración y preparación de un brief. **Preparar un mensaje o abrir una agenda no equivale a generar un lead ni a reservar una cita.** Una conversión de venta o reserva requiere medición del sistema que realmente completa esa acción. Los eventos no incorporan nombres, correos ni el texto del brief.

## Rendimiento
El objetivo a validar en producción es LCP ≤ 2,5 s, INP < 200 ms y CLS < 0,1, interpretando datos de campo cuando haya volumen suficiente. No se presentan como resultados obtenidos. La entrega reduce hojas de estilos, evita fuentes de red, limita GSAP a la portada, carga medios cerca del viewport y pausa animación fuera de pantalla o con movimiento reducido.

## Primeras cuatro semanas
- Semana 1: accesibilidad del dominio, indexación, respuestas HTTP, consola del navegador y conversión real.
- Semana 2: consultas y páginas encontradas; mejorar títulos según intención real, no por repetir palabras.
- Semana 3: publicar una demostración autorizada y un caso con contexto y evidencia.
- Semana 4: priorizar el siguiente contenido según consultas comerciales y reuniones útiles; revisar rendimiento móvil.

## Fuentes oficiales consultadas
- Google SEO Starter Guide: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
- Google Search y experiencias generativas: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Core Web Vitals: https://developers.google.com/search/docs/appearance/core-web-vitals
- Sitemap: https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap
- Organization: https://developers.google.com/search/docs/appearance/structured-data/organization
- Breadcrumb: https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- GSAP ScrollTrigger: https://gsap.com/docs/v3/Plugins/ScrollTrigger/

La conexión de Search Console, el identificador de analítica, los certificados y la medición de producción no se configuraron desde este entorno.
