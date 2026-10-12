# Revisión pública de indexabilidad de NICHO

Prueba: 2026-10-12 02:22:25 UTC (11 de octubre, 21:22 en Colombia).
Ejecución: https://github.com/Samuelacuna12/nicho-web/actions/runs/38195520773
Trabajo: 114637168834. Artefacto JSON: 11722923343.

## Resultados observados
La portada https://nichoagenciadigital.com/ respondió HTTP 200 por HTTPS con validación TLS habilitada. Su URL final fue la misma.
La portada tiene robots="index,follow,max-image-preview:large", no presenta X-Robots-Tag restrictivo y declara https://nichoagenciadigital.com/ como canónica. Se detectó un H1 y 47 enlaces HTML.
El sitemap respondió HTTP 200, Content-Type application/xml, XML válido, 24 URL y 24 URL únicas del dominio.
robots.txt respondió HTTP 200. Sus reglas permiten rastrear la portada, las 24 páginas examinadas y el sitemap.
Las 24 URL del sitemap respondieron HTTP 200 por HTTPS, sin meta noindex ni X-Robots-Tag noindex detectado, y con canonical correspondiente a cada URL.
La variante https://www.nichoagenciadigital.com/ terminó en https://nichoagenciadigital.com/ con HTTP 200.
La comprobación no detectó problemas en esos controles. No se modificó la web publicada ni el DNS.

## Límites
La prueba se ejecutó desde un servidor de GitHub Actions, no desde el rastreador de Google. No es una auditoría visual, de rendimiento, ni una verificación del índice de Google.
No se consultó una propiedad conectada de Google Search Console: no se puede afirmar que la portada esté indexada ni determinar la causa exacta del aviso del sitemap.
La captura aportada anteriormente por el usuario correspondía a una prueba en vivo del sitemap, no al estado de indexación de la portada.
Para confirmar indexación, inspeccionar https://nichoagenciadigital.com/ en Search Console y revisar GOOGLE INDEX, no LIVE TEST.
