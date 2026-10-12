# Diagnóstico de disponibilidad del sitemap de NICHO

Prueba realizada el 12 de octubre de 2026 a las 02:09:25 UTC, desde un servidor de GitHub Actions. No es un rastreo de Google Search Console.

Ejecución: https://github.com/Samuelacuna12/nicho-web/actions/runs/38194675879
Trabajo con registros detallados: 114634619337.

## Resultados observados

- https://nichoagenciadigital.com/sitemap.xml: HTTP 200, misma URL final, conexión HTTPS con verificación TLS predeterminada habilitada.
- Tipo de contenido: application/xml. Tamaño: 2678 bytes.
- XML analizado correctamente, con espacio de nombres de sitemaps correcto.
- Contiene 24 URL únicas, todas del dominio https://nichoagenciadigital.com/.
- https://nichoagenciadigital.com/robots.txt: HTTP 200; permite obtener /sitemap.xml para Googlebot y declara la URL del sitemap.
- https://nichoagenciadigital.com/: HTTP 200, contenido HTML.
- La solicitud a https://www.nichoagenciadigital.com/sitemap.xml termina en https://nichoagenciadigital.com/sitemap.xml con HTTP 200.
- Google Public DNS devuelve los cuatro registros A de GitHub Pages; la consulta no devuelve registros AAAA ni CAA para la raíz.

## Alcance

Esta prueba confirma disponibilidad desde el servidor que ejecutó el diagnóstico, no desde los servidores de rastreo de Google. El estado «Couldn't fetch» del informe de Search Console requiere abrir el detalle de la solicitud o probar la URL en tiempo real desde Search Console para conocer su causa exacta.

No se modificaron la web publicada, DNS ni Search Console.
