# Corrección de navegación y fidelidad visual

- Se preservan las 24 URL canónicas existentes; no se cambian DNS, correo ni el alojamiento.
- Navegación principal y móvil con enlaces reales a páginas completas. Se conservan la extensión `.html` y el historial de enlaces para no iniciar otra migración.
- El marcador de vista previa `?v=kinetic` se elimina del navegador; los enlaces heredados de portada `#proyectos`, `#servicios` y `#como` llevan a sus páginas mediante compatibilidad JavaScript. No es una redirección HTTP 301 ni una prueba de lo que Google ha indexado.
- Se elimina de la portada la escena naranja con pin y opacidad reducida. El texto permanece visible; las animaciones sólo presentan los productos y un indicador decorativo.
- Cinco capturas de los códigos originales: Invicto OPS, Luminari, RestoOps, SeguroOS y Cuentas Carlos. Revisiones fijadas en `original-interface-provenance.json`.
- Los sistemas se abren en copias aisladas: se bloquean llamadas externas, el estado operativo queda vacío y se usa el modo de demostración original cuando existe. No se inicia sesión ni se consulta ni modifica una base de datos real.
- Los diseños conservan sus colores, proporciones y componentes. Las imágenes de los productos no reciben filtros ni rediseños.
- El caso de agentes no presenta una interfaz falsa. Sus conversaciones requieren una demostración autorizada.
- La base técnica SEO no equivale a indexación confirmada, posiciones ni resultados de Core Web Vitals. Esas mediciones se deben comprobar por separado.
