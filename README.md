# Reglamento del Consejo de Estudiantes de la Universidad de Zaragoza

Buscador, comparador, PDF y programa del reparto del borrador del Reglamento del CEUZ, servidos con GitHub Pages
e incrustados con un iframe en la página de Drupal [ceuz.unizar.es/reglamento/borrador](https://ceuz.unizar.es/reglamento/borrador)
(de momento sin enlazar desde ningún sitio: es para la revisión de la Comisión Permanente).
Sigue el esquema de [cienzdel/reglamento](https://github.com/cienzdel/reglamento), del Consejo de Estudiantes de Ciencias.

- `buscar/`: buscador; los resultados abren el apartado en ceuz.unizar.es.
- `comparador/`: comparativa del borrador con el Reglamento de 2017, artículo por artículo, con el motivo de cada cambio.
- `pdf/`: el borrador en PDF.
- `reparto/`: programa del anexo que calcula el reparto de puestos entre centros (Sainte-Laguë con un puesto mínimo).

## Cómo se actualiza

El texto se escribe en un único fichero, `contenido.py`, en la carpeta de trabajo del borrador. Allí, `python generar.py`
produce el LaTeX, la comparativa y `reglamento-estructura.json`. Después:

1. `python herramientas/construir.py CARPETA_DEL_BORRADOR` copia esos ficheros a `fuentes/` y regenera `datos/`,
   `comparador/`, `pdf/`, `reparto/` y `drupal/reglamento-borrador.html`.
2. El contenido de `drupal/reglamento-borrador.html` se pega como cuerpo (HTML filtrado) de la página de Drupal.
3. La cuenta de GitHub Pages y el enlace al documento de comentarios se configuran al principio de `construir.py`.

No hay dependencias ni paso de compilación: HTML, CSS y JS estáticos y Python estándar.
