# Reparto de puestos entre centros

Programa del anexo del Reglamento. El Consejo calcula el reparto con el censo del curso anterior que le comunica el
vicerrectorado: un puesto por centro y el resto por el método de Sainte-Laguë (cociente `estudiantes / (2s + 1)`,
siendo `s` los puestos que ya tiene el centro). Los empates van al centro con más estudiantes y, si persisten, a sorteo.

    python reparto.py censo.csv 53

`censo.csv` tiene una línea por centro (`centro;estudiantes`); `53` son los puestos de los centros (60 menos los siete
representantes del Consejo de Gobierno). Con `ejemplo.csv` y 6 puestos sale 3, 2 y 1, como el ejemplo del anexo.
Si el programa y el texto del anexo discrepan, prevalece el texto.
