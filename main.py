"""
API del Indice Compuesto de Atractividad Industrial (ICAI)
Corredor del Bajio: SLP, Aguascalientes, Guanajuato, Jalisco, Queretaro
Equipo 11 - Taller de Fundamentos para el Analisis de Datos
"""

from fastapi import FastAPI, HTTPException, Query, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
import pandas as pd
import numpy as np
import os

# ── Autenticacion ─────────────────────────────────────────────────────
API_KEY = os.getenv("API_KEY", "icai-bajio-equipo11-2025")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verificar_api_key(key: str = Security(api_key_header)):
    if key == API_KEY:
        return key
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="API Key invalida o ausente. Incluye el header X-API-Key."
    )

# ── App ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="API - Indice de Atractividad Industrial del Bajio",
    description="""
API que expone los datos del Indice Compuesto de Atractividad Industrial (ICAI)
para los cinco estados del corredor del Bajio durante 2018-2025.

## Autenticacion
Todos los endpoints requieren el header **X-API-Key: icai-bajio-equipo11-2025**

## Fuentes de datos
- IED: Secretaria de Economia
- Exportaciones: INEGI (ETEF)
- Manufactura: INEGI (EMIM)
- Credito Comercial: CNBV
- INPC: Banco de Mexico / INEGI

## Metodologia ICAI
Normalizacion Min-Max + ponderacion economica:
IED (25%) + Exportaciones (25%) + Manufactura (25%) + Credito (15%) + INPC (10%)
    """,
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Datos ─────────────────────────────────────────────────────────────
def cargar_panel():
    df = pd.read_csv("panel_bajio.csv")
    def minmax(s):     return (s - s.min()) / (s.max() - s.min())
    def minmax_inv(s): return 1 - minmax(s)
    df["norm_ied"]           = minmax(df["ied_usd"])
    df["norm_exportaciones"] = minmax(df["exportaciones_usd"])
    df["norm_manufactura"]   = minmax(df["personal_ocupado"])
    df["norm_credito"]       = minmax(df["credito_pesos"])
    df["norm_inpc"]          = minmax_inv(df["inpc_general"])
    df["ICAI"] = (
        df["norm_ied"]           * 0.25 +
        df["norm_exportaciones"] * 0.25 +
        df["norm_manufactura"]   * 0.25 +
        df["norm_credito"]       * 0.15 +
        df["norm_inpc"]          * 0.10
    ) * 100
    df["ICAI"] = df["ICAI"].round(2)
    return df

panel = cargar_panel()
ESTADOS = sorted(panel["entidad"].unique().tolist())
ANIOS   = sorted(panel["anio"].unique().tolist())


# ── Endpoints ─────────────────────────────────────────────────────────

@app.get("/", tags=["General"])
def bienvenida():
    """Bienvenida y descripcion de la API. No requiere autenticacion."""
    return {
        "nombre": "API - ICAI Corredor del Bajio",
        "version": "1.0.0",
        "descripcion": "Indice Compuesto de Atractividad Industrial 2018-2025",
        "autenticacion": "Header X-API-Key requerido en todos los endpoints protegidos",
        "estados": ESTADOS,
        "periodo": f"{min(ANIOS)}-{max(ANIOS)}",
        "endpoints_disponibles": [
            "GET /estados",
            "GET /datos",
            "GET /ied",
            "GET /exportaciones",
            "GET /manufactura",
            "GET /credito",
            "GET /inpc",
            "GET /icai",
            "GET /icai/ranking",
            "GET /icai/perfil/{estado}",
        ]
    }


@app.get("/estados", tags=["General"])
def obtener_estados(api_key: str = Depends(verificar_api_key)):
    """Lista los cinco estados del corredor del Bajio."""
    return {"estados": ESTADOS, "total": len(ESTADOS)}


@app.get("/datos", tags=["Datos"])
def obtener_datos(
    estado: str | None = Query(None, description="Filtrar por estado"),
    anio:   int | None = Query(None, description="Filtrar por anio (2018-2025)"),
    api_key: str = Depends(verificar_api_key)
):
    """Panel completo con todas las variables. Filtrable por estado y anio."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado. Disponibles: {ESTADOS}")
        df = df[df["entidad"] == estado]
    if anio:
        if anio not in ANIOS:
            raise HTTPException(status_code=404, detail=f"Anio '{anio}' no disponible. Rango: {min(ANIOS)}-{max(ANIOS)}")
        df = df[df["anio"] == anio]
    return {
        "total_registros": len(df),
        "filtros": {"estado": estado, "anio": anio},
        "datos": df[["entidad","anio","ied_usd","exportaciones_usd",
                     "credito_pesos","personal_ocupado","valor_produccion",
                     "inpc_general","inpc_energia"]].to_dict(orient="records")
    }


@app.get("/ied", tags=["Dimensiones"])
def obtener_ied(
    estado: str | None = Query(None, description="Filtrar por estado"),
    api_key: str = Depends(verificar_api_key)
):
    """Inversion Extranjera Directa por estado y anio (millones de USD)."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]
    resumen = df.groupby("entidad")["ied_usd"].agg(
        total="sum", promedio="mean", maximo="max", minimo="min"
    ).round(2).reset_index()
    return {
        "descripcion": "Inversion Extranjera Directa 2018-2025",
        "unidad": "Millones de USD",
        "fuente": "Secretaria de Economia",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","ied_usd"]].to_dict(orient="records")
    }


@app.get("/exportaciones", tags=["Dimensiones"])
def obtener_exportaciones(
    estado: str | None = Query(None, description="Filtrar por estado"),
    api_key: str = Depends(verificar_api_key)
):
    """Exportaciones por estado y anio (miles de USD)."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]
    resumen = df.groupby("entidad")["exportaciones_usd"].agg(
        total="sum", promedio="mean", maximo="max", minimo="min"
    ).round(0).reset_index()
    return {
        "descripcion": "Exportaciones anuales 2018-2025",
        "unidad": "Miles de USD",
        "fuente": "INEGI - ETEF",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","exportaciones_usd"]].to_dict(orient="records")
    }


@app.get("/manufactura", tags=["Dimensiones"])
def obtener_manufactura(
    estado: str | None = Query(None, description="Filtrar por estado"),
    api_key: str = Depends(verificar_api_key)
):
    """Personal ocupado y valor de produccion manufacturera por estado."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]
    resumen = df.groupby("entidad").agg(
        personal_promedio=("personal_ocupado", "mean"),
        personal_maximo=("personal_ocupado", "max"),
        produccion_promedio=("valor_produccion", "mean"),
    ).round(0).reset_index()
    return {
        "descripcion": "Actividad manufacturera 2018-2025",
        "unidades": {"personal_ocupado": "Personas", "valor_produccion": "Miles de pesos"},
        "fuente": "INEGI - EMIM",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","personal_ocupado","valor_produccion"]].to_dict(orient="records")
    }


@app.get("/credito", tags=["Dimensiones"])
def obtener_credito(
    estado: str | None = Query(None, description="Filtrar por estado"),
    api_key: str = Depends(verificar_api_key)
):
    """Credito comercial empresarial por estado (millones de pesos)."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]
    resumen = df.groupby("entidad")["credito_pesos"].agg(
        promedio="mean", maximo="max", minimo="min"
    ).round(2).reset_index()
    total_corredor = df.groupby("anio")["credito_pesos"].sum().reset_index()
    df2 = df.merge(total_corredor, on="anio", suffixes=("","_total"))
    df2["participacion_pct"] = (df2["credito_pesos"] / df2["credito_pesos_total"] * 100).round(2)
    return {
        "descripcion": "Credito comercial empresarial 2018-2025",
        "unidad": "Millones de pesos corrientes",
        "fuente": "CNBV - Portafolio de Informacion",
        "nota": "Ruptura metodologica en 2022 por adopcion de IFRS9",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df2[["entidad","anio","credito_pesos","participacion_pct"]].to_dict(orient="records")
    }


@app.get("/inpc", tags=["Dimensiones"])
def obtener_inpc(api_key: str = Depends(verificar_api_key)):
    """INPC general y subindice de energeticos (cobertura nacional)."""
    df = panel[["anio","inpc_general","inpc_energia"]].drop_duplicates().sort_values("anio")
    return {
        "descripcion": "INPC general y subindice energeticos 2018-2025",
        "unidad": "Indice base 2Q Jul 2018 = 100",
        "fuente": "Banco de Mexico - SIE / INEGI",
        "nota": "Variable nacional - no diferencia entre estados",
        "serie_anual": df.to_dict(orient="records")
    }


@app.get("/icai", tags=["ICAI"])
def obtener_icai(
    estado: str | None = Query(None, description="Filtrar por estado"),
    anio:   int | None = Query(None, description="Filtrar por anio"),
    api_key: str = Depends(verificar_api_key)
):
    """ICAI por estado y anio. Escala 0-100 puntos."""
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]
    if anio:
        if anio not in ANIOS:
            raise HTTPException(status_code=404, detail=f"Anio '{anio}' no disponible.")
        df = df[df["anio"] == anio]
    return {
        "descripcion": "Indice Compuesto de Atractividad Industrial",
        "metodologia": "Normalizacion Min-Max + ponderacion economica",
        "ponderaciones": {"IED": "25%", "Exportaciones": "25%", "Manufactura": "25%", "Credito": "15%", "INPC": "10%"},
        "escala": "0 a 100 puntos",
        "datos": df[["entidad","anio","ICAI"]].to_dict(orient="records")
    }


@app.get("/icai/ranking", tags=["ICAI"])
def obtener_ranking(api_key: str = Depends(verificar_api_key)):
    """Ranking del ICAI promedio 2018-2025 por estado."""
    ranking = panel.groupby("entidad")["ICAI"].mean().round(2).sort_values(
        ascending=False).reset_index()
    ranking.columns = ["estado", "ICAI_promedio"]
    ranking["posicion"] = range(1, len(ranking) + 1)
    ranking["nivel"] = ranking["ICAI_promedio"].apply(
        lambda v: "Medio-Alto" if v >= 40 else "Intermedio" if v >= 20 else "Bajo"
    )
    return {
        "descripcion": "Ranking de atractividad industrial promedio 2018-2025",
        "ranking": ranking[["posicion","estado","ICAI_promedio","nivel"]].to_dict(orient="records")
    }


@app.get("/icai/perfil/{estado}", tags=["ICAI"])
def obtener_perfil(
    estado: str,
    api_key: str = Depends(verificar_api_key)
):
    """Perfil dimensional del ICAI para un estado especifico."""
    if estado not in ESTADOS:
        raise HTTPException(status_code=404,
            detail=f"Estado '{estado}' no encontrado. Disponibles: {ESTADOS}")
    df = panel[panel["entidad"] == estado]
    pesos = {"IED": 0.25, "Exportaciones": 0.25, "Manufactura": 0.25, "Credito": 0.15, "INPC": 0.10}
    perfil = {
        "IED":          round(df["norm_ied"].mean()           * pesos["IED"]           * 100, 2),
        "Exportaciones":round(df["norm_exportaciones"].mean() * pesos["Exportaciones"] * 100, 2),
        "Manufactura":  round(df["norm_manufactura"].mean()   * pesos["Manufactura"]   * 100, 2),
        "Credito":      round(df["norm_credito"].mean()       * pesos["Credito"]       * 100, 2),
        "INPC":         round(df["norm_inpc"].mean()          * pesos["INPC"]          * 100, 2),
    }
    icai_total = round(sum(perfil.values()), 2)
    ranking = panel.groupby("entidad")["ICAI"].mean().sort_values(ascending=False)
    posicion = list(ranking.index).index(estado) + 1
    nivel = "Medio-Alto" if icai_total >= 40 else "Intermedio" if icai_total >= 20 else "Bajo"
    return {
        "estado": estado,
        "ICAI_promedio": icai_total,
        "nivel": nivel,
        "posicion_ranking": posicion,
        "total_estados": len(ESTADOS),
        "contribucion_por_dimension": perfil,
        "formula": "ICAI = (IED*0.25 + Exp*0.25 + Manuf*0.25 + Cred*0.15 + INPC*0.10) x 100",
        "interpretacion": f"{estado} obtiene {icai_total} puntos en el ICAI, "
                          f"posicion {posicion} de {len(ESTADOS)} en el corredor del Bajio. Nivel: {nivel}."
    }
