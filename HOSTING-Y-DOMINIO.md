# Nicho Agencia Digital — Publicar en GitHub Pages con dominio de Hostinger

**Decisión del proyecto:** probar **GitHub Pages** para la web informativa, el portafolio y captación por enlaces a WhatsApp, email y agendamiento. No habrá cobros ni funcionalidades de backend alojadas en Pages.

> Nota de uso: GitHub declara que Pages no está pensado para alojar gratuitamente negocios online, sitios que facilitan principalmente transacciones comerciales o SaaS. Una web informativa sin pagos tiene un uso técnicamente distinto, pero no garantiza aprobación respecto a todas las restricciones de GitHub. Revisar la política y, si resulta necesario, mantener GitHub como repositorio y migrar solo el hosting.

## 1. Publicar primero una vista de prueba
1. Abre: https://github.com/Samuelacuna12/nicho-web/settings/pages.
2. En Build and deployment: **Source: Deploy from a branch**.
3. Selecciona rama `main` y carpeta `/(root)`. Guarda.
4. Verifica el dominio temporal previsto `https://samuelacuna12.github.io/nicho-web/`. No asumir que ya está activo.

## 2. Antes de conectar el dominio
- Realiza copia del sitio antiguo en Hostinger.
- Exporta o documenta todos los DNS actuales. Asegura MX, TXT, SPF, DKIM, DMARC y otros subdominios para no afectar el correo y servicios.
- Recopila URLs indexadas del sitio antiguo y define redirecciones 301. **GitHub Pages por sí solo no facilita reglas de redirección HTTP 301 personalizadas**: habrá que mantener un mecanismo de redirects en Hostinger o usar un proxy externo si existen URL antiguas.
- Si corresponde, verifica propiedad del dominio en GitHub para evitar riesgos de asignación.

## 3. Configurar dominio personalizado en GitHub primero
1. En Settings → Pages → Custom domain, ingresa `nichoagenciadigital.com` y pulsa Save.
2. GitHub agregará/actualizará el archivo `CNAME` cuando se use publicación desde la rama.
3. Solo después prepara registros DNS en Hostinger.

## 4. DNS Hostinger para dominio raíz
Crea o actualiza **cuatro registros A** para el host `@`, con los siguientes valores:

| Tipo | Host | Apunta a |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | samuelacuna12.github.io |

Eliminar solo los registros A/AAAA/CNAME antiguos que entren en conflicto para `@` y `www`, después de respaldarlos. **No borrar MX ni TXT**, y conservar el resto de registros válidos para servicios y correos. Los records A son publicados por GitHub en su documentación oficial.

## 5. Verificar la puesta en producción
- Enforce HTTPS en GitHub Pages cuando esté disponible.
- Comprobar `https://nichoagenciadigital.com` y `https://www.nichoagenciadigital.com`.
- Comprobar menú, favicons, CSS, recursos Envato y enlace de contacto.
- Revisar `https://nichoagenciadigital.com/robots.txt` y `/sitemap.xml`.
- Validar indexación en Google Search Console y enviar sitemap.
- Probar que correos y subdominios antiguos siguen funcionando.
- Auditar cobertura de URLs antiguas y redirects. Evitar perder posicionamiento por un corte abrupto.

## Fuentes oficiales
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/troubleshooting-custom-domains-and-github-pages

**Estado:** documentación y favicon publicados en GitHub; **no** se han cambiado el DNS, el hosting real, Pages ni Search Console desde estas herramientas.
