# Nicho Agencia Digital — Studio / edición 04

Web estática multipágina con dirección editorial, marca tridimensional, casos de estudio y captación por WhatsApp.

## Sitio
- Marca: Nicho Agencia Digital.
- Dominio: `https://nichoagenciadigital.com`.
- Contacto: `nicho.agenciadigital@gmail.com` · `+57 302 828 9997`.
- Dirección: Carrera 29 #39-39, barrio La Aurora, oficina 01, Bucaramanga, Santander, Colombia.
- 24 rutas indexables y una página 404. No se publican precios.

## Arquitectura
HTML estático generado con contenido visible sin JavaScript. Una hoja de estilos compartida. GSAP/ScrollTrigger solo en la portada. La marca tiene una malla de geometría fija, render WebGL progresivo, video alternativo y póster estático. No se distribuyen tipografías.

Los casos del portafolio usan interfaces ilustrativas y datos de demostración identificados; no representan capturas ni resultados reales de clientes.

## Desarrollo
Los archivos ya están listos para GitHub Pages desde `main` y `/(root)`. No requieren compilación.
Para una prueba local: `python3 -m http.server 8000`, y abrir `http://localhost:8000`.
Si se incluye la carpeta `source` en el repositorio, se pueden regenerar los HTML mediante:

```sh
python3 -m pip install -r source/requirements.txt
python3 source/build.py
python3 tools/check_site.py .
```

El generador no vuelve a procesar videos ni tipografías: los recursos visuales finales están incluidos.

## Analítica y formularios
`assets/js/config.js` no tiene un identificador de Google Analytics configurado. No hay seguimiento externo por defecto. Al configurar un ID real, la interfaz solicita autorización antes de cargar la analítica.
El formulario prepara un mensaje de WhatsApp en el navegador. No lo envía ni crea un registro en un servidor.

## Verificaciones
Se ejecutaron pruebas estáticas y 72 combinaciones de página y ancho en Chromium local. Esta evidencia no sustituye pruebas de DNS/TLS, Core Web Vitals, WebGL nativo ni Search Console en producción. La creación de esta entrega no significa que se haya publicado en GitHub.

El flujo `.github/workflows/quality.yml` propone repetir la validación estática en GitHub Actions al guardar cambios; su ejecución en GitHub debe comprobarse tras publicar.
