# Dashboard ICAI - Atractividad Industrial del Bajio
## Equipo 11 | Taller de Fundamentos para el Analisis de Datos

---

## Instalacion y ejecucion local

### 1. Instalar dependencias
```
pip install -r requirements.txt
```

### 2. Verificar que el archivo de datos este en la misma carpeta
El archivo `panel_bajio.csv` debe estar en la misma carpeta que `app.py`.

### 3. Correr el dashboard
```
streamlit run app.py
```

El dashboard se abrira automaticamente en: http://localhost:8501

---

## Publicacion en Render

1. Subir esta carpeta a GitHub (incluyendo panel_bajio.csv)
2. Crear cuenta en https://render.com
3. New Web Service -> conectar repositorio
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`
6. Deploy -> obtener URL publica

---

## Estructura del proyecto

```
dashboard/
    app.py              <- Codigo principal del dashboard
    requirements.txt    <- Dependencias
    panel_bajio.csv     <- Datos del panel consolidado
    README.md           <- Este archivo
```

---

## Contenido del dashboard

- KPIs: ICAI promedio, valor ultimo anio, posicion en ranking, mejor anio, diferencia vs corredor
- Filtros: selector de estado y rango de anios en sidebar
- Evolucion del ICAI por estado (lineas)
- Ranking ICAI promedio (barras horizontales)
- Perfil dimensional SLP vs promedio corredor (barras agrupadas)
- IED por estado (lineas)
- Exportaciones por estado (barras agrupadas)
- Personal ocupado manufactura (areas)
- Credito comercial (lineas)
- INPC general vs energeticos (lineas)
- Tabla de datos del estado seleccionado
