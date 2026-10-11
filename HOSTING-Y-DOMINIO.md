# NICHO Agencia Digital — Conectar Hostinger DNS con GitHub Pages

**Sitio**: https://nichoagenciadigital.com  
**GitHub repo**: https://github.com/Samuelacuna12/nicho-web  
**Publicación**: `main` / `/(root)`  
**GitHub Pages CNAME**: confirmado, contiene `nichoagenciadigital.com`.

## 0 — Seguridad antes de cambiar DNS
1. Haz una captura o exportación de **TODOS los registros actuales** de tu zona DNS en Hostinger.
2. Haz copia de la web antigua y conserva sus URL importantes. Cambiar el A del dominio hace que el sitio anterior deje de servirse por ese nombre.
3. Conserva **MX, TXT (SPF, DKIM, DMARC, verificaciones), NS, SRV, CAA y otros subdominios**. No toques los nameservers.
4. Comprueba si Hostinger es el **proveedor DNS activo**. Si usas nameservers de otro proveedor, el DNS efectivo se cambia allí.
5. No elimines los registros actuales hasta identificar los conflictos: generalmente A/AAAA de `@`, y A/AAAA/CNAME de `www`.

## 1 — Registros para GitHub Pages

| Tipo | Host/Nombre | Apunta a |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | samuelacuna12.github.io |

**TTL**: deja el valor predeterminado o 3600 si es posible. Para `www` la ruta no incluye `/nicho-web`.

### IPv6 (opcional, recomendable si gestionas registros AAAA)
| Tipo | Host/Nombre | Apunta a |
|---|---|---|
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |

**Muy importante**: si existe un AAAA anterior para `@` o `www` que apunta al hosting viejo, corregirlo o quitarlo para que no envíe tráfico a un servidor distinto. GitHub admite solamente A si no quieres habilitar IPv6.

## 2 — Pasos en Hostinger
1. Entra en https://hpanel.hostinger.com/.
2. Selecciona **Domains → DNS**, luego `nichoagenciadigital.com`. En algunas interfaces aparece como **Domains → Domain portfolio → Manage → DNS / Nameservers**. Si tu panel tiene hosting web, también se puede encontrar en **Websites → Advanced → DNS Zone Editor**.
3. Revisa si la zona DNS está administrada por Hostinger y guarda captura de los registros existentes.
4. Edita o elimina **solo** los registros conflictivos del dominio web y añade los A y el CNAME anteriores. Conserva todos los registros de correo y demás servicios.
5. Guarda los cambios. La propagación puede tardar hasta 24 horas.

## 3 — Volver a GitHub
1. Entra en https://github.com/Samuelacuna12/nicho-web/settings/pages.
2. El dominio personalizado ya debe figurar como `nichoagenciadigital.com`. **No hace falta volver a guardarlo**.
3. Comprueba que `DNS Check in Progress` cambia a verificación completada.
4. Activa **Enforce HTTPS** cuando GitHub habilite la casilla; puede tomar hasta 24 horas.
5. Comprueba:
   - https://nichoagenciadigital.com/
   - https://www.nichoagenciadigital.com/ (debe redirigir al dominio sin www)
   - https://nichoagenciadigital.com/robots.txt
   - https://nichoagenciadigital.com/sitemap.xml
   - https://nichoagenciadigital.com/favicon.svg
   - Páginas internas, navegación, imágenes, WhatsApp y agenda.
6. Confirma la recepción y envío de email si hay buzones o servicios conectados a ese dominio.

## 4 — SEO después de publicación
- Dar de alta propiedad del dominio en Google Search Console mediante TXT de verificación, sin borrar TXT previos.
- Enviar `https://nichoagenciadigital.com/sitemap.xml`.
- Auditar páginas del sitio anterior y configurar redirecciones **HTTP 301** donde corresponda. GitHub Pages no provee reglas HTTP 301 arbitrarias en un archivo `_redirects`: se necesita infraestructura externa si hay URLs antiguas no preservadas.
- No verificar ranking ni indexación hasta que Google haya podido rastrear las nuevas páginas.

## 5 — Fuentes oficiales
- GitHub Pages custom domain: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- GitHub Pages limits: https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits
- Hostinger DNS editor: https://www.hostinger.com/support/1583249-how-to-manage-dns-records-at-hostinger/

**Estado:** GitHub Pages y CNAME figuran configurados. Este documento NO cambia los DNS de Hostinger. El acceso a la cuenta Hostinger y su editor DNS no está conectado a este chat.