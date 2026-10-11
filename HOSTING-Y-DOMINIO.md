# Publicación de Nicho Agencia Digital: Hostinger + GitHub + Cloudflare Pages

## Recomendación de infraestructura
- **GitHub**: repositorio de código (Samuelacuna12/nicho-web). 
- **Cloudflare Pages**: hosting estático para web comercial, despliegue automático desde GitHub y HTTPS.
- **Hostinger**: mantener propiedad y renovación del dominio `nichoagenciadigital.com`.
- **DNS**: para enlazar el dominio raíz con Cloudflare Pages, usar zona DNS de Cloudflare, conservando el registro en Hostinger.

GitHub Pages no es la opción recomendada para una web empresarial de captación: las políticas de GitHub Pages limitan su uso como hosting gratuito para negocios comerciales.

## Procedimiento con riesgo mínimo
1. Accede a https://dash.cloudflare.com/ > Workers & Pages > Create > Pages > Connect to Git.
2. Autoriza el repositorio `Samuelacuna12/nicho-web`, rama de producción `main`.
3. Configuración: sitio HTML estático sin framework, Build command `exit 0` o vacío, directorio de salida `.` (raíz del repositorio, con index.html).
4. Publica primero en URL temporal `*.pages.dev`. Prueba inicio, páginas internas, imágenes, menú, WhatsApp, email y agenda.
5. Antes de cambiar DNS, **obtén un inventario de registros DNS y una copia del sitio anterior** en Hostinger: A, AAAA, CNAME, MX, TXT, SPF, DKIM, DMARC, registros de verificación y subdominios.
6. Dentro de Cloudflare Pages añade `nichoagenciadigital.com` en Custom Domains. Para el dominio raíz Cloudflare exige configurar el dominio como zona y usar sus nameservers.
7. Copia y verifica los registros de correo y otros servicios en Cloudflare. Después cambia nameservers en Hostinger por los exactos que Cloudflare indique.
8. Activa HTTPS y redirige `www` a sin `www`. Prueba recepción y envío de correo si existen cuentas bajo ese dominio.
9. Audita las URL indexadas de la web anterior; crea reglas 301 permanentes URL-a-URL mediante Cloudflare Redirects. No envíes todas las URLs antiguas a la portada. Si faltan URLs actuales, **no cortes la web anterior**.
10. Verifica `robots.txt`, `sitemap.xml`, HTTP 200/404, canonical y Google Search Console. Envía sitemap https://nichoagenciadigital.com/sitemap.xml.
11. Configura analítica y conversiones (clic WhatsApp, correo, agenda), con consentimiento apropiado y sin prometer resultados SEO.

## Datos de negocio
- Marca: **Nicho Agencia Digital**
- Teléfono/WhatsApp: +57 302 828 9997
- Email: nicho.agenciadigital@gmail.com
- Dirección: Carrera 29 #39-39, barrio La Aurora, oficina 01, Bucaramanga, Santander, Colombia.
- Prioridad geográfica: Bucaramanga, Colombia y Latinoamérica. Atención internacional.
- Sin tarifas en público.

## Enlaces oficiales
- https://developers.cloudflare.com/pages/get-started/git-integration/
- https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
- https://developers.cloudflare.com/pages/configuration/custom-domains/
- https://developers.cloudflare.com/pages/configuration/redirects/
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits

**Estado:** se preparó la web y documentación; no se modificaron Hostinger, DNS, correo, hosting real ni Search Console.
