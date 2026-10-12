# Verificación de la entrega — Nicho Agencia Digital

Fecha: 11 de octubre de 2026. Versión de origen del repositorio: `7719cde2d4c4452dccac9d32ba0d8072d51ca78b`.

## Estado de publicación
**Nueva versión construida y probada localmente. No se ha guardado ni desplegado en GitHub durante esta entrega.** La conexión disponible solo expone acciones de lectura. No se modificaron DNS, certificados, Hostinger ni Search Console.

## Pruebas realizadas

| Verificación | Resultado |
|---|---|
| Documentos HTML | 25: 24 páginas indexables + 404 |
| Resoluciones de prueba | 390 × 844, 768 × 900 y 1440 × 900 |
| Combinaciones página/resolución | 72 |
| Desbordamientos horizontales detectados | 0 |
| Errores JavaScript detectados | 0 |
| Páginas con más o menos de un H1 | 0 |
| Rutas locales o anclas faltantes | 0 en validación estática |
| Bloques JSON-LD inválidos | 0 |
| Canonicals/sitemap | 24 rutas coincidentes |
| Recursos de imagen sin alt o dimensiones | 0 |
| Fuentes distribuidas en la entrega | 0 |
| Video alternativo de la marca | Reproduce, avanza y se pausa/reanuda |

## Interacciones verificadas
El menú móvil abre, recibe foco, se cierra con Escape y devuelve el foco al botón. La demostración IA–CRM–automatización responde a clics y flechas del teclado. Los filtros muestran cuatro sistemas, un caso de IA, un caso financiero y seis casos al seleccionar todos.

El formulario valida los campos y prepara una URL de WhatsApp para `573028289997`. Una entrada con etiquetas de script se mostró como texto; no se ejecutó. Tras preparar el mensaje se observaron **cero solicitudes HTTP externas**. Abrir el enlace y enviarlo en WhatsApp sigue siendo una acción separada del visitante.

Con JavaScript desactivado, el H1, los textos y los cuatro proyectos destacados continúan visibles. Con movimiento reducido, los videos no se cargan y se conserva un póster legible. La prueba visual estática deja todas las secciones visibles y pausa animaciones para obtener capturas comparables.

## Antes y después en el mismo renderizador

| Medida local | Versión anterior | Nueva versión |
|---|---:|---:|
| Altura de inicio en 1440 px de ancho | 15.153 px | 7.884 px |
| Altura de inicio en 390 px de ancho | 16.101 px | 9.465 px |
| Hojas de estilos enlazadas desde inicio | 6 | 1 |

La reducción de altura no elimina las páginas de servicios ni los estudios de caso. El inicio concentra el mensaje y deriva a la información detallada en páginas independientes.

## Qué NO certifican estas pruebas
No son una puntuación Lighthouse, una auditoría WCAG completa ni mediciones de LCP/INP/CLS de usuarios reales. No se midió el comportamiento de la red pública, el dominio, el certificado ni Safari/iPhone físico. Chromium se utilizó con renderizado local en memoria porque las navegaciones de red están bloqueadas en este entorno.

El WebGL nativo está deshabilitado en el navegador de pruebas. Se validó la alternativa de video/póster generada a partir de la misma geometría, pero no se afirma que el camino GPU haya superado pruebas en dispositivos reales. El código incluye degradación progresiva si WebGL no está disponible.

## Evidencia
`qa/browser-qa.json` contiene cada página, ancho, título, altura, H1 y errores observados. `qa/static-qa.json` contiene el inventario estático. `qa/motion-qa.json` contiene el resultado de reproducción. `vistas-previas/` contiene capturas reales de la entrega y una grabación local de 10 segundos.
