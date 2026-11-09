# GuíaTrámite

Landing de presentación e identidad visual para el proyecto. Noviembre de 2026.

## Contenido

- `web/`: landing estática lista para desplegar en Vercel.
- `GuiaTramite_Landing.html`: vista autocontenida para abrir directamente en el navegador, con estilos, tipografías, imágenes y demo incluidos.
- `identidad/`: logotipos SVG y PNG, símbolo, tarjeta social, paleta y guía de uso.
- `documentos/`: guion de reunión en PDF y Markdown, discurso en castellano y catalán, propuesta de piloto e identidad corporativa.

## Dirección visual actual

Portada oscura, titulares grandes en Montserrat, acento verde, vistas de producto enmarcadas y secciones claras y oscuras alternadas. Adaptación visual a la referencia facilitada: https://www.edutechcommunity.com/vibliotec/?lang=es. La identidad utiliza una G trazada como recorrido y un punto de orientación. La ilustración de atención municipal presenta tres pasos con etiquetas claras: qué hacer, qué preparar y dónde acudir.

Las tipografías Montserrat se sirven desde el proyecto; su licencia SIL Open Font License se incluye en `web/assets/MONTSERRAT-LICENSE.txt`.

Para regenerar la vista autocontenida y los ZIP tras editar el código, ejecutar `python3 package_project.py` desde la carpeta raíz.

## Qué ofrece esta versión

Landing en español y catalán, navegación móvil, demo de tres recorridos con contenido preparado en español, catalán y árabe, vista municipal con selección de fichas y filtro de pendientes, preguntas frecuentes, propuesta de piloto descargable y ficha de reunión que se genera en el dispositivo.

La demostración no consulta un modelo de IA, no tramita solicitudes, no reserva citas y no guarda expedientes. Los indicadores, la funcionalidad real, los idiomas y el calendario del piloto deberán acordarse con la institución. Los datos de las fichas son ficticios.

## Publicación en Vercel

La web está publicada en https://guiatramite.vercel.app. El código está en https://github.com/victorscodeit/guiatramite.

El proyecto de Vercel `guiatramite` pertenece al equipo `victorsanchocoma-4290s-projects` y se despliega desde la carpeta `web/`. No hay comando de build. Para publicar cambios:

```bash
cd web
npx vercel --prod --scope victorsanchocoma-4290s-projects
```

La cuenta de Vercel todavía no puede conectar el repositorio de GitHub, así que un push a `main` no redespliega solo.

## Vista local

La vista HTML autocontenida permite revisar el diseño sin instalación. Para trabajar con los archivos separados se puede servir `web/` con cualquier servidor estático; por ejemplo:

```bash
cd web
python3 -m http.server 8000
```

Abrir `http://localhost:8000`.

## Personalización pendiente

No se ha publicado un email de contacto ni se ha creado un formulario que envíe solicitudes, porque esos datos no se han facilitado. La llamada a la acción permite preparar y descargar una ficha de reunión sin enviar datos. Para incorporar recepción de consultas hay que definir el correo del proyecto y el tratamiento de ese formulario.

El nombre del ayuntamiento tampoco se ha facilitado. La propuesta municipal es general y no muestra logotipos institucionales, clientes, testimonios ni afiliaciones.

## Edición

- Textos en español: `web/index.html`.
- Traducciones en catalán y contenidos preparados de la demo: `web/app.js`.
- Estilos base: `web/styles.css`. Dirección visual de la versión actual: `web/reference.css`.
- Imágenes y tipografías: `web/assets/`.
- Propuesta pública descargable: `web/downloads/GuiaTramite_Propuesta_Piloto.pdf`.

La ficha descargada no se envía a un servidor. No se incluyen analítica, publicidad, modelos de IA, APIs ni claves. Los textos sobre privacidad y accesibilidad describen esta web de presentación; no constituyen una certificación del futuro servicio.

## Verificación realizada

Revisión visual en escritorio y a anchura móvil de 375 px; comprobación de menú móvil, cambio de idioma, lectura RTL del ejemplo árabe, selección de pasos, vista municipal, filtro, selección de ficha y generación de ficha de reunión. Enlaces y archivos locales comprobados, 156 claves de traducción cubiertas, sin IDs duplicados. Se verificó la sintaxis de JavaScript y se revisaron visualmente las 12 páginas de los PDF.

Los requisitos de producción de una plataforma de IA con datos reales se deberán definir y verificar por separado. El código de esta entrega corresponde a la landing y a su demostración.
