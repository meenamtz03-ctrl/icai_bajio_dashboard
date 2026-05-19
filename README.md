# API - Indice de Atractividad Industrial del Bajio
## Equipo 11 | Taller de Fundamentos para el Analisis de Datos

---

## Instalacion y ejecucion local

### 1. Instalar dependencias
Abrir una terminal en la carpeta del proyecto y ejecutar:
```
pip install -r requirements.txt
```

### 2. Verificar que el archivo de datos este en la misma carpeta
El archivo `panel_bajio.csv` debe estar en la misma carpeta que `main.py`.

### 3. Correr la API
```
uvicorn main:app --reload
```

La API estara disponible en: http://127.0.0.1:8000

### 4. Ver documentacion interactiva
Abrir en el navegador: http://127.0.0.1:8000/docs

---

## Endpoints disponibles

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | / | Bienvenida y descripcion general |
| GET | /estados | Lista los 5 estados del corredor |
| GET | /datos | Panel completo (filtrable por estado y año) |
| GET | /ied | Inversion Extranjera Directa |
| GET | /exportaciones | Exportaciones por entidad |
| GET | /manufactura | Personal ocupado y valor de produccion |
| GET | /credito | Credito comercial empresarial |
| GET | /inpc | INPC general y subindice energeticos |
| GET | /icai | ICAI por estado y año |
| GET | /icai/ranking | Ranking ICAI promedio 2018-2025 |
| GET | /icai/perfil/{estado} | Perfil dimensional de un estado |

---

## Ejemplos de uso

```
# Todos los datos de San Luis Potosi
GET /datos?estado=San Luis Potosi

# IED de Jalisco
GET /ied?estado=Jalisco

# ICAI de 2023
GET /icai?anio=2023

# Perfil dimensional de SLP
GET /icai/perfil/San Luis Potosi

# Ranking completo
GET /icai/ranking
```

---

## Estructura del proyecto

```
api_bajio/
    main.py           <- Codigo principal de la API
    requirements.txt  <- Dependencias
    panel_bajio.csv   <- Datos del panel consolidado
    README.md         <- Este archivo
```

---

## Despliegue en Render

1. Subir esta carpeta a un repositorio de GitHub
2. Crear cuenta en https://render.com
3. New Web Service -> conectar repositorio
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy -> obtener URL publica
