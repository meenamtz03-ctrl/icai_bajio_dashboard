# API - Indice de Atractividad Industrial del Bajio
## Equipo 11 | Taller de Fundamentos para el Analisis de Datos

API construida con FastAPI que expone los datos del ICAI para los cinco estados
del corredor del Bajio: San Luis Potosi, Aguascalientes, Guanajuato, Jalisco y Queretaro.
Periodo 2018-2025.

## URL publica
https://icai-bajio-api.onrender.com

## Autenticacion
Todos los endpoints protegidos requieren el header:
```
X-API-Key: icai-bajio-equipo11-2025
```

## Endpoints disponibles

| Metodo | Endpoint | Descripcion |
|--------|----------|-------------|
| GET | / | Bienvenida (sin autenticacion) |
| GET | /estados | Lista los 5 estados |
| GET | /datos | Panel completo (filtrable) |
| GET | /ied | Inversion Extranjera Directa |
| GET | /exportaciones | Exportaciones por entidad |
| GET | /manufactura | Actividad manufacturera |
| GET | /credito | Credito comercial empresarial |
| GET | /inpc | INPC y subindice energeticos |
| GET | /icai | ICAI por estado y anio |
| GET | /icai/ranking | Ranking ICAI promedio |
| GET | /icai/perfil/{estado} | Perfil dimensional de un estado |

## Documentacion interactiva
Una vez desplegada: https://icai-bajio-api.onrender.com/docs

## Ejemplo de uso
```bash
curl -H "X-API-Key: icai-bajio-equipo11-2025" https://icai-bajio-api.onrender.com/icai/ranking
```

## Instalacion local
```
pip install -r requirements.txt
uvicorn main:app --reload
```
Disponible en: http://127.0.0.1:8000/docs

## Despliegue en Render
- Build Command: pip install -r requirements.txt
- Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

## Fuentes de datos
- IED: Secretaria de Economia
- Exportaciones: INEGI (ETEF)
- Manufactura: INEGI (EMIM)
- Credito Comercial: CNBV
- INPC: Banco de Mexico / INEGI
