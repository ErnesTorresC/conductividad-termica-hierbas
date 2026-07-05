# Determinación de la Conductividad Térmica en Hierbas Aromáticas Deshidratadas

Este proyecto implementa un sistema automatizado de instrumentación virtual y análisis de datos para calcular de manera experimental la constante de conductividad térmica ($k$) del perejil deshidratado (*Petroselinum crispum*), fundamentado en la Ley de Fourier para la transferencia de calor unidimensional en estado estacionario.

##  Características del Proyecto
* **Adquisición de Datos:** Instrumentación virtual desarrollada en LabVIEW para el monitoreo en tiempo real de variables térmicas y eléctricas mediante termopares.
* **Procesamiento de Datos (Data Pipeline):** Script en Python utilizando `Pandas` y `NumPy` para la limpieza automatizada de ruido de digitalización y filtrado de valores atípicos (*outliers*).
* **Análisis de Ingeniería:** Visualización de la transición entre el régimen térmico transitorio y el estado estacionario mediante `Matplotlib`.

---

##  Fundamento Teórico

El cálculo se rige bajo la ecuación de Fourier en estado estacionario:

$$q = -k \cdot A \cdot \frac{\Delta T}{\Delta x}$$

Donde el script despeja la constante de conductividad térmica ($k$):

$$k = \frac{q \cdot \Delta x}{A \cdot \Delta T}$$

### Parámetros del Prototipo:
* **Área de contacto ($A$):** $38.704 \text{ cm}^2$ ($0.0038704 \text{ m}^2$)
* **Espesor de la muestra ($\Delta x$):** $0.552 \text{ cm}$ ($0.00552 \text{ m}$)
* **Corriente Máxima ($I_{max}$):** $0.088 \text{ A}$ a $127 \text{ V}$

---
##  Arquitectura y Diseño del Sistema

### 1. Diagrama del Bloque Instrumental
El sistema adquiere las señales analógicas de los termopares mediante un módulo de adquisición de datos compatible con LabVIEW, procesa los parámetros eléctricos de potencia y exporta los arreglos estructurados para su posterior tratamiento digital en Python.

![Diagrama de Bloques del Sistema](docs/Diagrama_Prototipo_Termico.png)

### 2. Pipeline de Análisis de Datos (Data Wrangling)
El procesamiento numérico ejecutado por el script de Python sigue un flujo estructurado para garantizar la fiabilidad del cálculo de la constante $k$:

![Pipeline de Procesamiento de Datos](docs/Pipeline_Datos_Python.png)
