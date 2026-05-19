"""
API de Atractividad Industrial del Corredor del Bajio
Equipo 11 - Taller de Fundamentos para el Analisis de Datos
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).parent

# ── Inicializar app ───────────────────────────────────────────────────
app = FastAPI(
    title="API - Indice de Atractividad Industrial del Bajio",
    description="""
    API que expone los datos del Indice Compuesto de Atractividad Industrial (ICAI)
    para los cinco estados del corredor del Bajio: San Luis Potosi, Aguascalientes,
    Guanajuato, Jalisco y Queretaro. Periodo 2018-2025.

    **Fuentes de datos:**
    - Inversion Extranjera Directa: Secretaria de Economia
    - Exportaciones: INEGI (ETEF)
    - Actividad Manufacturera: INEGI (EMIM)
    - Credito Comercial: CNBV
    - INPC: Banco de Mexico / INEGI
    """,
    version="1.0.0",
)

# ── CORS (permite acceso desde dashboard y navegador) ─────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Cargar y preparar datos ───────────────────────────────────────────
def cargar_datos():
    df = pd.read_csv(BASE_DIR / "panel_bajio.csv")

    # Normalizacion Min-Max
    def minmax(s):
        return (s - s.min()) / (s.max() - s.min())

    def minmax_inv(s):
        return 1 - minmax(s)

    df["norm_ied"]           = minmax(df["ied_usd"])
    df["norm_exportaciones"] = minmax(df["exportaciones_usd"])
    df["norm_manufactura"]   = minmax(df["personal_ocupado"])
    df["norm_credito"]       = minmax(df["credito_pesos"])
    df["norm_inpc"]          = minmax_inv(df["inpc_general"])

    # Ponderaciones
    df["ICAI"] = (
        df["norm_ied"]           * 0.25 +
        df["norm_exportaciones"] * 0.25 +
        df["norm_manufactura"]   * 0.25 +
        df["norm_credito"]       * 0.15 +
        df["norm_inpc"]          * 0.10
    ) * 100

    df["ICAI"] = df["ICAI"].round(2)
    return df

# Cargar datos al iniciar
panel = cargar_datos()
ESTADOS = sorted(panel["entidad"].unique().tolist())
ANIOS   = sorted(panel["anio"].unique().tolist())


# ══════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ══════════════════════════════════════════════════════════════════════

@app.get("/", tags=["General"])
def bienvenida():
    """Bienvenida y descripcion general de la API."""
    return {
        "mensaje": "API del Indice de Atractividad Industrial del Bajio",
        "version": "1.0.0",
        "estados_disponibles": ESTADOS,
        "periodo": f"{min(ANIOS)}-{max(ANIOS)}",
        "endpoints": [
            "/estados",
            "/datos",
            "/ied",
            "/exportaciones",
            "/manufactura",
            "/credito",
            "/inpc",
            "/icai",
            "/icai/ranking",
            "/icai/perfil/{estado}",
        ]
    }


@app.get("/estados", tags=["General"])
def obtener_estados():
    """Lista los cinco estados del corredor del Bajio."""
    return {
        "estados": ESTADOS,
        "total": len(ESTADOS)
    }


# ── DATOS COMPLETOS ───────────────────────────────────────────────────

@app.get("/datos", tags=["Datos"])
def obtener_datos(
    estado: str | None = Query(None, description="Filtrar por estado"),
    anio:   int | None = Query(None, description="Filtrar por año (2018-2025)")
):
    """
    Devuelve el panel completo de datos con todas las variables.
    Se puede filtrar por estado y/o año.
    """
    df = panel.copy()

    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404,
                detail=f"Estado '{estado}' no encontrado. Estados validos: {ESTADOS}")
        df = df[df["entidad"] == estado]

    if anio:
        if anio not in ANIOS:
            raise HTTPException(status_code=404,
                detail=f"Anio '{anio}' no disponible. Rango: {min(ANIOS)}-{max(ANIOS)}")
        df = df[df["anio"] == anio]

    return {
        "total_registros": len(df),
        "filtros": {"estado": estado, "anio": anio},
        "datos": df[["entidad","anio","ied_usd","exportaciones_usd",
                     "credito_pesos","personal_ocupado","valor_produccion",
                     "inpc_general","inpc_energia"]].to_dict(orient="records")
    }


# ── IED ───────────────────────────────────────────────────────────────

@app.get("/ied", tags=["Dimensiones"])
def obtener_ied(
    estado: str | None = Query(None, description="Filtrar por estado")
):
    """
    Inversion Extranjera Directa por estado y año (millones de USD).
    Fuente: Secretaria de Economia.
    """
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]

    resumen = df.groupby("entidad")["ied_usd"].agg(
        total="sum", promedio="mean", maximo="max", minimo="min"
    ).round(2).reset_index()

    return {
        "descripcion": "Inversion Extranjera Directa acumulada y promedio por estado (2018-2025)",
        "unidad": "Millones de USD",
        "fuente": "Secretaria de Economia",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","ied_usd"]].to_dict(orient="records")
    }


# ── EXPORTACIONES ─────────────────────────────────────────────────────

@app.get("/exportaciones", tags=["Dimensiones"])
def obtener_exportaciones(
    estado: str | None = Query(None, description="Filtrar por estado")
):
    """
    Exportaciones por estado y año (miles de USD).
    Fuente: INEGI - Exportaciones Trimestrales por Entidad Federativa (ETEF).
    """
    df = panel.copy()
    if estado:
        if estado not in ESTADOS:
            raise HTTPException(status_code=404, detail=f"Estado '{estado}' no encontrado.")
        df = df[df["entidad"] == estado]

    resumen = df.groupby("entidad")["exportaciones_usd"].agg(
        total="sum", promedio="mean", maximo="max", minimo="min"
    ).round(0).reset_index()

    return {
        "descripcion": "Exportaciones anuales por estado (2018-2025)",
        "unidad": "Miles de USD",
        "fuente": "INEGI - ETEF",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","exportaciones_usd"]].to_dict(orient="records")
    }


# ── MANUFACTURA ───────────────────────────────────────────────────────

@app.get("/manufactura", tags=["Dimensiones"])
def obtener_manufactura(
    estado: str | None = Query(None, description="Filtrar por estado")
):
    """
    Personal ocupado y valor de produccion manufacturera por estado.
    Fuente: INEGI - Encuesta Mensual de la Industria Manufacturera (EMIM).
    """
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
        "descripcion": "Actividad manufacturera por estado (2018-2025)",
        "unidades": {
            "personal_ocupado": "Numero de personas",
            "valor_produccion": "Miles de pesos corrientes"
        },
        "fuente": "INEGI - EMIM",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df[["entidad","anio","personal_ocupado","valor_produccion"]].to_dict(orient="records")
    }


# ── CREDITO ───────────────────────────────────────────────────────────

@app.get("/credito", tags=["Dimensiones"])
def obtener_credito(
    estado: str | None = Query(None, description="Filtrar por estado")
):
    """
    Credito comercial empresarial por estado (millones de pesos).
    Fuente: CNBV - Portafolio de Informacion, Banca Multiple.
    Nota: ruptura metodologica en 2022 por adopcion de IFRS9.
    """
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
        "descripcion": "Credito comercial empresarial por estado (2018-2025)",
        "unidad": "Millones de pesos corrientes",
        "fuente": "CNBV - Portafolio de Informacion",
        "nota_metodologica": "Ruptura en 2022 por adopcion de IFRS9",
        "resumen_por_estado": resumen.to_dict(orient="records"),
        "serie_anual": df2[["entidad","anio","credito_pesos","participacion_pct"]].to_dict(orient="records")
    }


# ── INPC ──────────────────────────────────────────────────────────────

@app.get("/inpc", tags=["Dimensiones"])
def obtener_inpc():
    """
    Indice Nacional de Precios al Consumidor general y subindice de energeticos.
    Fuente: Banco de Mexico - SIE / INEGI. Base 2Q Jul 2018 = 100.
    Variable de cobertura nacional (no diferencia entre estados).
    """
    df = panel[["anio","inpc_general","inpc_energia"]].drop_duplicates().sort_values("anio")

    return {
        "descripcion": "INPC general y subindice de energeticos (2018-2025)",
        "unidad": "Indice base 2Q Jul 2018 = 100",
        "fuente": "Banco de Mexico - SIE / INEGI",
        "nota": "Variable nacional - no diferencia entre estados",
        "serie_anual": df.to_dict(orient="records")
    }


# ── ICAI ──────────────────────────────────────────────────────────────

@app.get("/icai", tags=["ICAI"])
def obtener_icai(
    estado: str | None = Query(None, description="Filtrar por estado"),
    anio:   int | None = Query(None, description="Filtrar por año")
):
    """
    Indice Compuesto de Atractividad Industrial (ICAI) por estado y año.
    Metodologia: normalizacion Min-Max + ponderacion economica.
    Escala: 0 a 100 puntos.
    """
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
        "descripcion": "ICAI - Indice Compuesto de Atractividad Industrial",
        "metodologia": "Normalizacion Min-Max + ponderacion economica",
        "ponderaciones": {
            "IED": "25%",
            "Exportaciones": "25%",
            "Manufactura": "25%",
            "Credito_comercial": "15%",
            "INPC": "10%"
        },
        "escala": "0 a 100 puntos",
        "datos": df[["entidad","anio","ICAI"]].to_dict(orient="records")
    }


@app.get("/icai/ranking", tags=["ICAI"])
def obtener_ranking():
    """
    Ranking del ICAI promedio 2018-2025 por estado.
    Ordenado de mayor a menor atractividad.
    """
    ranking = panel.groupby("entidad")["ICAI"].mean().round(2).sort_values(
        ascending=False
    ).reset_index()
    ranking.columns = ["estado", "ICAI_promedio"]
    ranking["posicion"] = range(1, len(ranking) + 1)

    return {
        "descripcion": "Ranking de atractividad industrial promedio 2018-2025",
        "metodologia": "ICAI promedio del periodo",
        "ranking": ranking[["posicion","estado","ICAI_promedio"]].to_dict(orient="records")
    }


@app.get("/icai/perfil/{estado}", tags=["ICAI"])
def obtener_perfil(estado: str):
    """
    Perfil dimensional del ICAI para un estado especifico.
    Muestra la contribucion ponderada de cada dimension al indice total.
    """
    if estado not in ESTADOS:
        raise HTTPException(status_code=404,
            detail=f"Estado '{estado}' no encontrado. Estados validos: {ESTADOS}")

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

    # Posicion en el ranking
    ranking = panel.groupby("entidad")["ICAI"].mean().sort_values(ascending=False)
    posicion = list(ranking.index).index(estado) + 1

    return {
        "estado": estado,
        "ICAI_promedio": icai_total,
        "posicion_ranking": posicion,
        "contribucion_por_dimension": perfil,
        "interpretacion": f"{estado} obtiene {icai_total} puntos en el ICAI, "
                          f"ocupando la posicion {posicion} de 5 en el corredor del Bajio."
    }
