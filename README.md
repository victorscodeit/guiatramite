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

El intento de creación y despliegue desde la conexión disponible fue rechazado con un error 403 de permisos para crear proyectos. No hay un despliegue de producción confirmado.

Con una cuenta autorizada en el equipo `victorsanchocoma-4290s-projects`:

1. Utilizar la carpeta `web/` como raíz del proyecto nuevo `guiatramite`.
2. Elegir el preset **Other**. Esta web no necesita instalación de dependencias ni comando de build. Dejar el directorio de salida sin configurar.
3. Desplegar esa carpeta. Incluye `vercel.json` con cabeceras y configuración de URLs.
4. Verificar navegación, selección de idiomas, demo, ficha y descarga de propuesta.

Alternativamente, desde una terminal con Node y una sesión propia de Vercel:

```bash
cd web
npx vercel login
npx vercel --scope victorsanchocoma-4290s-projects --prod
```

Revisar el equipo y seleccionar **crear un proyecto nuevo** con el nombre `guiatramite`. No vincular a otro proyecto existente. Si la cuenta carece de permisos para crear proyectos, deberá resolverlo una persona administradora del equipo.

Documentación oficial: https://vercel.com/docs/cli/deploy

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
