# =============================================================================
# ForecastingVentas – Motor de Predicción de Ventas Noviembre 2025
# App Streamlit con predicciones recursivas (HistGradientBoostingRegressor)
# =============================================================================

import warnings
warnings.filterwarnings("ignore")

import sys
import os

import streamlit as st
import pandas as pd
import numpy as np
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------------
# Configuración de página
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="ForecastingVentas · Motor de Predicción Nov 2025",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CSS personalizado – paleta morada/azul, glassmorphism
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    html, body, .stApp {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
        color: #e8e8f5;
    }

    /* ── Sidebar fondo ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10103a 0%, #1e1b4b 60%, #2d2b55 100%);
        border-right: 2px solid #667eea66;
    }
    section[data-testid="stSidebar"] * { color: #d4d4f5 !important; }

    /* ── Sidebar – títulos y separadores ── */
    section[data-testid="stSidebar"] h2 {
        background: linear-gradient(90deg, #667eea, #c5b4f5);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #667eea44 !important;
        margin: .6rem 0 !important;
    }

    /* ── Sidebar – labels de widgets ── */
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #a0a8e8 !important;
        font-weight: 600 !important;
        font-size: .82rem !important;
        letter-spacing: .04em;
    }

    /* ── Sidebar – Selectbox ── */
    section[data-testid="stSidebar"] .stSelectbox > div > div {
        background: linear-gradient(135deg, #1e1b4b, #2d2b6a) !important;
        border: 1.5px solid #667eea88 !important;
        border-radius: 10px !important;
        color: #c5b4f5 !important;
        box-shadow: 0 2px 12px #667eea22 !important;
        transition: border-color .2s, box-shadow .2s !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: #c5b4f5 !important;
        box-shadow: 0 0 0 2px #667eea44 !important;
    }
    section[data-testid="stSidebar"] .stSelectbox > div > div > div {
        color: #c5b4f5 !important;
    }

    /* ── Sidebar – Slider track & thumb ── */
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
        color: #c5b4f5 !important;
    }
    section[data-testid="stSidebar"] .stSlider [role="slider"] {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        border: 2px solid #c5b4f5 !important;
        box-shadow: 0 0 8px #667eea88 !important;
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div:first-child > div:first-child {
        background: linear-gradient(90deg, #667eea, #764ba2) !important;
    }
    section[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] > div:first-child {
        background: #2d2b55 !important;
    }

    /* ── Sidebar – Radio buttons ── */
    section[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
        color: #b0b8f0 !important;
        font-size: .84rem !important;
    }
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] > div:first-child {
        border-color: #667eea !important;
        background: transparent !important;
        transition: all .15s !important;
    }
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] > div:first-child {
        border-color: #c5b4f5 !important;
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        box-shadow: 0 0 8px #667eea88 !important;
    }

    /* ── Sidebar – info note ── */
    section[data-testid="stSidebar"] small {
        color: #6666a0 !important;
        font-size: .72rem !important;
        line-height: 1.5;
    }

    /* ── KPI cards ── */
    .kpi-card {
        background: linear-gradient(135deg, #667eea22, #764ba244);
        border: 1px solid #667eea55;
        border-radius: 14px;
        padding: 1.2rem 1rem;
        text-align: center;
        box-shadow: 0 4px 24px #667eea22;
        transition: transform .2s;
        height: 100%;
    }
    .kpi-card:hover { transform: translateY(-4px); }
    .kpi-label { font-size: .72rem; color: #a0a0d0; letter-spacing: .08em;
                 text-transform: uppercase; margin-bottom: .35rem; }
    .kpi-value { font-size: 1.8rem; font-weight: 800; color: #c5b4f5; }
    .kpi-delta { font-size: .72rem; color: #8888b8; margin-top: .25rem; }

    /* ── Botón simular ── */
    .stButton > button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        padding: .75rem 1.5rem !important;
        width: 100% !important;
        cursor: pointer !important;
        box-shadow: 0 4px 20px #667eea55 !important;
        transition: opacity .2s, transform .15s !important;
    }
    .stButton > button:hover {
        opacity: .88 !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px #764ba266 !important;
    }

    /* ── Metric nativo ── */
    [data-testid="metric-container"] {
        background: #ffffff08;
        border: 1px solid #667eea33;
        border-radius: 10px;
        padding: .6rem .8rem;
    }
    h1, h2, h3 { color: #c5b4f5 !important; }
    .section-sep { border:none; border-top:1px solid #667eea33; margin: 1.5rem 0; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
BASE_DIR   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "models", "modelo_final.joblib")
DATA_PATH  = os.path.join(BASE_DIR, "data", "processed", "inferencia_df_transformado.csv")

LAG_COLS = [f"lag_{i}" for i in range(1, 8)]
MA_COL   = "rolling_mean_7"
BF_DAY   = 28

# ---------------------------------------------------------------------------
# Carga (cached)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Modelo no encontrado: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"Datos no encontrados: {DATA_PATH}")
    df = pd.read_csv(DATA_PATH, parse_dates=["fecha"])
    return df

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def fmt_int(v):  return f"{int(round(v)):,}".replace(",", ".")
def fmt_eur(v):  return f"{v:,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
def fmt_pct(v):  return f"{v:.1f}%"

# ---------------------------------------------------------------------------
# Predicción recursiva  (versión corregida)
# ---------------------------------------------------------------------------
def predict_recursive(df_product, model, descuento_delta, comp_factor):
    """
    descuento_delta : descuento ABSOLUTO en % sobre precio_base que quiere el usuario
                      (0 = sin descuento, 10 = 10% de descuento, -10 = subida de precio 10%).
                      Se aplica DIRECTAMENTE sobre precio_base, no se acumula con el CSV.
    comp_factor     : factor multiplicativo sobre precio_competencia (1.0 / 0.95 / 1.05).
    """
    feature_cols = model.feature_names_in_.tolist()
    df = df_product.copy().sort_values("fecha").reset_index(drop=True)
    predictions  = []

    # ── Pre-inicializar rolling_mean_7 del día 1 desde los lags disponibles ──
    # El CSV tiene rolling_mean_7 = NaN en todos los días; la inicializamos
    # con el promedio de los lags que sí están disponibles en la fila 0.
    lags_dia1 = []
    for k in range(1, 8):
        v = df.loc[0, f"lag_{k}"]
        if pd.notna(v):
            lags_dia1.append(float(v))
    ma7_inicial = float(np.mean(lags_dia1)) if lags_dia1 else 0.0
    df.loc[0, MA_COL] = ma7_inicial

    # ── Rellenar NaN en lags iniciales: lag_k NaN → usar lag_{k-1} ──────────
    # Solo para el día 0; a partir del día 1 los actualiza el loop recursivo.
    ref = df.loc[0, "lag_1"] if pd.notna(df.loc[0, "lag_1"]) else 0.0
    for k in range(1, 8):
        if pd.isna(df.loc[0, f"lag_{k}"]):
            df.loc[0, f"lag_{k}"] = ref

    for i in range(len(df)):
        row = df.loc[i].copy()

        # ── 1. Precio de venta según descuento del slider ──────────────────
        #    descuento_delta es el % que quiere el usuario aplicar sobre precio_base.
        #    Rango slider: -50 (subida de precio 50%) … +50 (descuento del 50%).
        precio_base      = float(row["precio_base"])
        desc_usuario     = float(np.clip(descuento_delta, -50, 50))   # % solicitado
        precio_venta_sim = precio_base * (1.0 - desc_usuario / 100.0)
        precio_venta_sim = max(precio_venta_sim, 0.01)                 # nunca negativo

        # Guardamos en la columna de features el valor en la escala real del CSV
        # (el modelo fue entrenado con esa columna)
        row["precio_venta"]         = precio_venta_sim
        row["descuento_porcentaje"] = desc_usuario   # usamos la escala del slider

        # ── 2. Precio competencia ajustado ────────────────────────────────
        precio_comp_sim           = float(row["precio_competencia"]) * comp_factor
        row["precio_competencia"] = precio_comp_sim
        row["ratio_precio"]       = (precio_venta_sim / precio_comp_sim) if precio_comp_sim > 0 else 1.0

        # ── 3. Actualizar lags recursivamente (días 2-30) ─────────────────
        if i > 0:
            # Desplazar: lag_7←lag_6, …, lag_2←lag_1, lag_1←predicción anterior
            for k in range(7, 1, -1):
                row[f"lag_{k}"] = df.loc[i - 1, f"lag_{k - 1}"]
            row["lag_1"] = predictions[-1]
            # Actualizar rolling_mean_7 con las últimas 7 predicciones disponibles
            ventana = predictions[-7:]
            row[MA_COL] = float(np.mean(ventana))

        # ── 4. Garantizar que no queden NaN en features ───────────────────
        for col in feature_cols:
            if pd.isna(row[col]):
                row[col] = 0.0

        # ── 5. Predecir ───────────────────────────────────────────────────
        X    = pd.DataFrame([row[feature_cols].values], columns=feature_cols)
        pred = max(float(model.predict(X)[0]), 0.0)
        predictions.append(pred)

        # ── 6. Persistir en df para la siguiente iteración ────────────────
        df.loc[i, "lag_1"]                = row["lag_1"]
        df.loc[i, MA_COL]                 = row[MA_COL]
        df.loc[i, "precio_venta"]         = precio_venta_sim
        df.loc[i, "precio_competencia"]   = precio_comp_sim
        df.loc[i, "descuento_porcentaje"] = desc_usuario
        df.loc[i, "ratio_precio"]         = row["ratio_precio"]

    df["prediccion"]       = [round(p) for p in predictions]
    df["precio_venta_sim"] = df["precio_venta"]
    df["precio_comp_sim"]  = df["precio_competencia"]
    df["descuento_sim"]    = df["descuento_porcentaje"]
    df["ingresos_sim"]     = df["prediccion"] * df["precio_venta_sim"]
    return df

# ---------------------------------------------------------------------------
# Gráfico seaborn
# ---------------------------------------------------------------------------
def plot_prediccion(df_pred, producto):
    sns.set_theme(style="darkgrid")
    fig, ax = plt.subplots(figsize=(10, 3.8))
    fig.patch.set_facecolor("#12122a")
    ax.set_facecolor("#0f0f26")

    dias   = df_pred["dia_mes"].astype(int).tolist()
    ventas = df_pred["prediccion"].tolist()

    ax.plot(dias, ventas, color="#c5b4f5", linewidth=2.5, zorder=3)
    ax.fill_between(dias, ventas, alpha=0.15, color="#667eea")
    ax.scatter(dias, ventas, color="#667eea", s=35, zorder=4, linewidths=0)

    if BF_DAY in dias:
        idx_bf  = dias.index(BF_DAY)
        val_bf  = ventas[idx_bf]
        max_val = max(ventas)
        ax.axvline(x=BF_DAY, color="#ff6b6b", linewidth=1.5, linestyle="--", alpha=.85, zorder=2)
        ax.scatter([BF_DAY], [val_bf], color="#ff6b6b", s=130, zorder=5,
                   edgecolors="white", linewidths=1.5)
        ax.annotate(
            f"🛍 Black Friday\n{fmt_int(val_bf)} uds",
            xy=(BF_DAY, val_bf),
            xytext=(BF_DAY + 1.2, val_bf + max_val * 0.1),
            fontsize=8, color="#ff9999",
            arrowprops=dict(arrowstyle="->", color="#ff6b6b", lw=1.2),
        )

    ax.set_xlabel("Día de noviembre", color="#8888b8", fontsize=8.5)
    ax.set_ylabel("Unidades predichas", color="#8888b8", fontsize=8.5)
    ax.tick_params(colors="#8888b8", labelsize=7.5)
    ax.set_xticks(range(1, 31))
    ax.set_xlim(0.5, 30.5)
    for spine in ax.spines.values():
        spine.set_edgecolor("#667eea33")
    ax.grid(True, color="#667eea1a", linewidth=0.6)
    ax.set_title(f"Predicción diaria · {producto}", color="#c5b4f5", fontsize=10.5, pad=9)
    plt.tight_layout()
    return fig

# ===========================================================================
# CARGA DE RECURSOS
# ===========================================================================
load_error = None
try:
    with st.spinner("⚙️ Cargando modelo y datos…"):
        model  = load_model()
        df_all = load_data()
except Exception as e:
    load_error = str(e)

if load_error:
    st.error(f"❌ **Error al cargar archivos:** {load_error}")
    st.info("Ejecuta la app desde la raíz del proyecto:\n```\nstreamlit run app/app.py\n```")
    st.stop()

productos = sorted(df_all["nombre"].unique().tolist())

# ===========================================================================
# SIDEBAR
# ===========================================================================
with st.sidebar:
    st.markdown("## 🎛 Controles de Simulación")
    st.markdown("---")

    producto_sel = st.selectbox(
        "🏷 Producto",
        options=productos,
        index=0,
        key="producto_sel",
    )

    st.markdown("---")

    descuento_delta = st.slider(
        "📉 Descuento sobre precio base (%)",
        min_value=-50, max_value=50, value=0, step=5,
        format="%d%%",
        key="descuento_delta",
        help="0% = precio base sin cambio | +10% = 10% de descuento | -10% = 10% de incremento de precio",
    )

    st.markdown("---")

    escenario_comp = st.radio(
        "🏪 Escenario de competencia",
        options=["Actual (0%)", "Competencia −5%", "Competencia +5%"],
        index=0,
        key="escenario_comp",
    )

    comp_factor_map = {
        "Actual (0%)":     1.00,
        "Competencia −5%": 0.95,
        "Competencia +5%": 1.05,
    }
    comp_factor = comp_factor_map[escenario_comp]

    st.markdown("---")
    simular = st.button("🚀 Simular Ventas", key="btn_simular", use_container_width=True)
    st.markdown("---")
    st.markdown(
        "<small style='color:#6666a0;'>ℹ️ Las predicciones son recursivas: "
        "cada día usa las unidades predichas del día anterior como lag.</small>",
        unsafe_allow_html=True,
    )

# ===========================================================================
# EJECUCIÓN – siempre antes del st.stop()
# ===========================================================================
if simular:
    df_producto = df_all[df_all["nombre"] == producto_sel].copy()
    if df_producto.empty:
        st.error(f"No hay datos para: {producto_sel}")
    else:
        with st.spinner("🔄 Calculando predicciones recursivas…"):
            try:
                df_pred = predict_recursive(df_producto, model, descuento_delta, comp_factor)
                st.session_state["resultado"]       = df_pred
                st.session_state["producto_activo"] = producto_sel
                st.session_state["desc_activo"]     = descuento_delta
                st.session_state["comp_activo"]     = comp_factor
                st.session_state["esc_activo"]      = escenario_comp
            except Exception as e:
                st.error(f"❌ Error durante la predicción: {e}")

# ===========================================================================
# HEADER PRINCIPAL
# ===========================================================================
st.markdown(
    """
    <div style='text-align:center; padding:1.8rem 0 .6rem 0;'>
        <div style='font-size:2.8rem; margin-bottom:.3rem; line-height:1;'>🔮</div>
        <h1 style='font-size:2.1rem; letter-spacing:-.02em;
                   background:linear-gradient(90deg,#667eea 0%,#c5b4f5 50%,#f5a0e0 100%);
                   -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                   margin:0; font-weight:800;'>
            ForecastingVentas
        </h1>
        <p style='color:#8888b8; font-size:.88rem; margin:.35rem 0 0 0;
                  letter-spacing:.12em; text-transform:uppercase;'>
            Motor de Predicción · Noviembre 2025
        </p>
        <div style='width:80px; height:3px;
                    background:linear-gradient(90deg,#667eea,#764ba2);
                    border-radius:2px; margin:.7rem auto 0 auto;'></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mostrar mensaje inicial si aún no hay resultados
if "resultado" not in st.session_state:
    st.info("👈 Configura los parámetros en el sidebar y pulsa **🚀 Simular Ventas** para generar las predicciones.")
    st.stop()

# ===========================================================================
# DASHBOARD (solo si hay resultados)
# ===========================================================================
df_pred         = st.session_state["resultado"]
producto_activo = st.session_state["producto_activo"]
desc_activo     = st.session_state["desc_activo"]
comp_activo     = st.session_state["comp_activo"]
esc_activo      = st.session_state["esc_activo"]

# ── Sub-header del producto ────────────────────────────────────────────────
signo = "+" if desc_activo >= 0 else ""
st.markdown(
    f"""
    <div style='background:linear-gradient(135deg,#667eea22,#764ba222);
                border:1px solid #667eea44; border-radius:14px;
                padding:.9rem 1.4rem; margin:.4rem 0 1rem 0;'>
        <h2 style='margin:0; color:#c5b4f5; font-size:1.35rem;'>🏷 {producto_activo}</h2>
        <p style='margin:.25rem 0 0 0; color:#8888b8; font-size:.82rem;'>
            Descuento ajustado: <b style='color:#c5b4f5'>{signo}{desc_activo}pp</b>
            &nbsp;|&nbsp;
            Escenario: <b style='color:#c5b4f5'>{esc_activo}</b>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ===========================================================================
# SECCIÓN 1 – KPIs
# ===========================================================================
unidades_total  = df_pred["prediccion"].sum()
ingresos_total  = df_pred["ingresos_sim"].sum()
precio_promedio = df_pred["precio_venta_sim"].mean()
desc_promedio   = df_pred["descuento_sim"].mean()

c1, c2, c3, c4 = st.columns(4)
kpis = [
    (c1, "📦 Unidades Proyectadas", fmt_int(unidades_total),  "Noviembre 2025"),
    (c2, "💰 Ingresos Proyectados",  fmt_eur(ingresos_total),  "Noviembre 2025"),
    (c3, "🏷 Precio Medio Venta",    fmt_eur(precio_promedio), "Media mensual"),
    (c4, "📉 Descuento Medio",       fmt_pct(desc_promedio),   "Media mensual"),
]
for col, label, value, sub in kpis:
    with col:
        st.markdown(
            f"""<div class='kpi-card'>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-value'>{value}</div>
                <div class='kpi-delta'>{sub}</div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

# ===========================================================================
# SECCIÓN 2 – Gráfico seaborn
# ===========================================================================
st.markdown("### 📈 Predicción Diaria de Ventas")
fig = plot_prediccion(df_pred, producto_activo)
st.pyplot(fig, use_container_width=True)
plt.close(fig)

st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

# ===========================================================================
# SECCIÓN 3 – Tabla detallada
# ===========================================================================
st.markdown("### 📋 Detalle Diario · Noviembre 2025")

DIAS_NOMBRE = {0:"Lunes",1:"Martes",2:"Miércoles",3:"Jueves",
               4:"Viernes",5:"Sábado",6:"Domingo"}

tabla = df_pred[["fecha","dia_semana","dia_mes",
                  "precio_venta_sim","precio_comp_sim",
                  "descuento_sim","prediccion","ingresos_sim"]].copy()

tabla["Día"]                 = tabla["fecha"].dt.strftime("%d/%m/%Y")
tabla["Semana"]              = tabla["dia_semana"].map(DIAS_NOMBRE)
tabla["Precio Venta (€)"]   = tabla["precio_venta_sim"].map(lambda x: f"{x:,.2f} €")
tabla["P. Comp. (€)"]       = tabla["precio_comp_sim"].map(lambda x: f"{x:,.2f} €")
tabla["Descuento (%)"]       = tabla["descuento_sim"].map(lambda x: f"{x:.1f}%")
tabla["Unidades"]            = tabla["prediccion"].astype(int)
tabla["Ingresos (€)"]        = tabla["ingresos_sim"].map(lambda x: f"{x:,.2f} €")
tabla["🛍 BF"]               = tabla["dia_mes"].apply(
    lambda d: "🛍 BLACK FRIDAY" if d == BF_DAY else ""
)

display = tabla[["Día","Semana","Precio Venta (€)","P. Comp. (€)",
                  "Descuento (%)","Unidades","Ingresos (€)","🛍 BF"]].reset_index(drop=True)

bf_idx = tabla["dia_mes"].tolist().index(BF_DAY) if BF_DAY in tabla["dia_mes"].tolist() else None

def hl_bf(row):
    color = "background-color:#ff6b6b18; color:#ff9999; font-weight:bold;"
    return [color if row.name == bf_idx else "" for _ in row]

st.dataframe(display.style.apply(hl_bf, axis=1), use_container_width=True, height=440)

st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)

# ===========================================================================
# SECCIÓN 4 – Comparativa de escenarios
# ===========================================================================
st.markdown("### 🔀 Comparativa de Escenarios de Competencia")
st.markdown(
    f"<p style='color:#8888b8;font-size:.82rem;margin-top:-.4rem;'>"
    f"Descuento fijo: <b style='color:#c5b4f5'>{signo}{desc_activo}pp</b> · "
    f"Solo varía el precio de la competencia.</p>",
    unsafe_allow_html=True,
)

df_base = df_all[df_all["nombre"] == producto_activo].copy()

escenarios_def = [
    ("Actual (0%)",     1.00, "⚖️", "#667eea"),
    ("Competencia −5%", 0.95, "📉", "#4ecdc4"),
    ("Competencia +5%", 1.05, "📈", "#ff6b6b"),
]

colA, colB, colC = st.columns(3)
for col, (esc_name, factor, icon, color) in zip([colA, colB, colC], escenarios_def):
    with col:
        with st.spinner(f"Calculando {esc_name}…"):
            df_esc = predict_recursive(df_base, model, desc_activo, factor)
        uds  = df_esc["prediccion"].sum()
        ing  = df_esc["ingresos_sim"].sum()
        st.markdown(
            f"""<div style='background:linear-gradient(135deg,{color}22,{color}11);
                           border:1px solid {color}55; border-radius:14px;
                           padding:1.2rem; text-align:center;'>
                    <div style='font-size:1.7rem; margin-bottom:.35rem;'>{icon}</div>
                    <div style='font-size:.82rem; font-weight:700; color:{color}; margin-bottom:.6rem;'>{esc_name}</div>
                    <div style='font-size:1.35rem; font-weight:800; color:#e8e8f5;'>{fmt_int(uds)} uds</div>
                    <div style='font-size:.82rem; color:#a0a0d0; margin-top:.3rem;'>{fmt_eur(ing)}</div>
                </div>""",
            unsafe_allow_html=True,
        )

# ===========================================================================
# FOOTER
# ===========================================================================
st.markdown("<hr class='section-sep'>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center;color:#444470;font-size:.72rem;'>"
    "TelecomX · Simulador de Ventas Nov 2025 · "
    "Modelo: HistGradientBoostingRegressor · "
    "Predicciones recursivas con lags actualizados día a día"
    "</p>",
    unsafe_allow_html=True,
)
