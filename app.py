import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import random
import math
import requests
import google.generativeai as genai

# Creiamo un box sicuro nella barra laterale per la tua API Key
st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Configurazione AI")
user_api_key = st.sidebar.text_input("Inserisci API Key Gemini", type="password")
from datetime import date, timedelta, datetime
from sklearn.linear_model import LinearRegression

try:
    from streamlit_lottie import st_lottie
    LOTTIE_OK = True
except ImportError:
    LOTTIE_OK = False

st.set_page_config(
    page_title="LogiSense — Supply Chain Platform",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Premium Injection ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Hide default Streamlit chrome ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── Fade-in page ── */
@keyframes fadeIn { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
.main .block-container { animation: fadeIn 0.45s ease-out; padding-top: 1.5rem !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 8px !important;
    background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
    color: white !important; border: none !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.3) !important;
}
.stButton > button:hover {
    transform: scale(1.04) !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.45) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%) !important;
    box-shadow: 0 2px 8px rgba(34,197,94,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 4px 16px rgba(34,197,94,0.5) !important;
}

/* ── Download button ── */
.stDownloadButton > button {
    border-radius: 8px !important;
    background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%) !important;
    color: white !important; border: none !important;
    font-weight: 600 !important;
    transition: transform 0.15s ease !important;
}
.stDownloadButton > button:hover { transform: scale(1.04) !important; }

/* ── st.metric cards (secondary use) ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    border: 1px solid #e2e8f0; border-radius: 12px;
    padding: 12px 16px !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

/* ── Custom KPI cards ── */
.kpi-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 18px 20px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.07);
    margin-bottom: 6px;
    height: 100%;
}
.kpi-card .kpi-icon  { font-size: 1.4rem; margin-bottom: 4px; }
.kpi-card .kpi-label { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 4px; }
.kpi-card .kpi-value { font-size: 1.75rem; font-weight: 800; color: #0f172a; line-height: 1.1; }
.kpi-card .kpi-delta { font-size: 0.78rem; margin-top: 6px; font-weight: 600; }
.kpi-delta-up   { color: #16a34a; }
.kpi-delta-down { color: #dc2626; }
.kpi-delta-neutral { color: #64748b; }

/* ── Score badges ── */
.score-badge-great { background: #dcfce7; color: #166534; border-radius: 20px; padding: 3px 10px; font-weight: 700; font-size: 0.82rem; }
.score-badge-ok    { background: #fef9c3; color: #92400e; border-radius: 20px; padding: 3px 10px; font-weight: 700; font-size: 0.82rem; }
.score-badge-bad   { background: #fee2e2; color: #991b1b; border-radius: 20px; padding: 3px 10px; font-weight: 700; font-size: 0.82rem; }

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border-radius: 10px; overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
}

/* ── Expander ── */
[data-testid="stExpander"] {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stSlider > div > div { background: #334155 !important; }
[data-testid="stSidebar"] [data-testid="stSelectbox"] { background: #1e293b !important; }
[data-testid="stSidebar"] [data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.05) !important;
    border-radius: 8px !important; border: 1px dashed #475569 !important;
}

/* ── Tab bar ── */
[data-testid="stTabs"] button {
    border-radius: 6px 6px 0 0 !important;
    font-weight: 600 !important; font-size: 0.88rem !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(135deg, #eff6ff, #eef2ff) !important;
    color: #3b82f6 !important; border-bottom: 2px solid #3b82f6 !important;
}

/* ── Headers ── */
h1, h2, h3 { letter-spacing: -0.02em; }

/* ── Code blocks ── */
[data-testid="stCodeBlock"] {
    border-radius: 8px !important;
    border: 1px solid #e2e8f0 !important;
    font-size: 0.84rem !important;
}

/* ── Divider ── */
hr { border-color: #e2e8f0 !important; margin: 1.2rem 0 !important; }
</style>
""", unsafe_allow_html=True)


# ── KPI Card helper ───────────────────────────────────────────────────────────
def kpi_card(label: str, value: str, icon: str = "📊",
             delta: str = "", delta_type: str = "neutral") -> str:
    """Render a premium HTML/CSS KPI card via st.markdown."""
    delta_class = {"up": "kpi-delta-up", "down": "kpi-delta-down"}.get(delta_type, "kpi-delta-neutral")
    delta_html = f'<div class="kpi-delta {delta_class}">{delta}</div>' if delta else ""
    return f"""
<div class="kpi-card">
  <div class="kpi-icon">{icon}</div>
  <div class="kpi-label">{label}</div>
  <div class="kpi-value">{value}</div>
  {delta_html}
</div>"""


# ── Lottie helper ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_lottie_url(url: str):
    try:
        r = requests.get(url, timeout=6)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None


# ── Mock inventory data ───────────────────────────────────────────────────────
@st.cache_data
def load_mock_inventory() -> pd.DataFrame:
    random.seed(42)
    data = {
        "SKU": [f"SKU-{1000 + i}" for i in range(15)],
        "Prodotto": [
            "Vite M6x20", "Bullone M8", "Guarnizione OR-15", "Cuscinetto 6205",
            "Cinghia B-42", "Filtro Olio FO-3", "Valvola 2-Vie", "Pompa Centrifuga",
            "Encoder Rotativo", "Riduttore G-50", "Sensore Pressione", "Relay 24V",
            "Quadro Elettrico Q1", "Motore EC-75", "Inverter 2.2kW",
        ],
        "Categoria": [
            "Viterie", "Viterie", "Tenute", "Trasmissione",
            "Trasmissione", "Filtrazione", "Fluidica", "Fluidica",
            "Elettronica", "Meccanica", "Elettronica", "Elettronica",
            "Elettrotecnica", "Elettrotecnica", "Elettrotecnica",
        ],
        "Fornitore": [
            "FastenerTech Srl", "FastenerTech Srl", "SealPro Italia Srl",
            "BearingWorld Spa", "BearingWorld Spa", "FilterMaster Srl",
            "FluidTech Srl", "FluidTech Srl", "ElettroComp Spa",
            "MeccaInd Srl", "ElettroComp Spa", "ElettroComp Spa",
            "PowerDrive Italia Spa", "PowerDrive Italia Spa", "PowerDrive Italia Spa",
        ],
        "Email_Fornitore": [
            "info@fastenertech.it", "info@fastenertech.it", "ordini@sealpro.it",
            "acquisti@bearingworld.it", "acquisti@bearingworld.it", "info@filtermaster.it",
            "ordini@fluidtech.it", "ordini@fluidtech.it", "acquisti@elettrocomp.it",
            "info@meccaind.it", "acquisti@elettrocomp.it", "acquisti@elettrocomp.it",
            "ordini@powerdrive.it", "ordini@powerdrive.it", "ordini@powerdrive.it",
        ],
        "Costo Unitario (€)": [
            0.08, 0.15, 1.20, 8.50, 12.00, 4.30, 35.00, 220.00,
            75.00, 340.00, 55.00, 18.00, 1200.00, 890.00, 650.00,
        ],
        "Giacenza": [
            5200, 3100, 480, 45, 30, 120, 18, 6,
            12, 4, 22, 95, 2, 3, 5,
        ],
        "Scorta Sicurezza": [
            1000, 500, 200, 60, 50, 80, 25, 10,
            15, 8, 20, 50, 3, 5, 4,
        ],
        "Lead Time (giorni)": [
            7, 7, 14, 21, 21, 10, 28, 45,
            30, 60, 30, 14, 90, 75, 60,
        ],
        "Costo Ordine S (€)": [
            15, 15, 20, 35, 35, 25, 50, 80,
            60, 100, 60, 30, 150, 120, 100,
        ],
        "Costo Mantenimento H (€/u/anno)": [
            0.02, 0.03, 0.24, 1.70, 2.40, 0.86, 7.00, 44.00,
            15.00, 68.00, 11.00, 3.60, 240.00, 178.00, 130.00,
        ],
    }
    df = pd.DataFrame(data)
    df["Valore Totale (€)"] = df["Costo Unitario (€)"] * df["Giacenza"]
    return df


def load_uploaded_inventory(uploaded_file) -> pd.DataFrame:
    """Parse a user-uploaded CSV or XLSX and map to our schema."""
    fname = uploaded_file.name.lower()
    try:
        if fname.endswith(".xlsx") or fname.endswith(".xls"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        else:
            df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")
        return load_mock_inventory()

    # Normalise column names (strip, title-case comparison)
    df.columns = df.columns.str.strip()

    # Required numeric columns with defaults
    numeric_defaults = {
        "Giacenza": 100, "Scorta Sicurezza": 20,
        "Lead Time (giorni)": 14, "Costo Unitario (€)": 1.0,
        "Costo Ordine S (€)": 30, "Costo Mantenimento H (€/u/anno)": 0.5,
    }
    for col, default in numeric_defaults.items():
        if col not in df.columns:
            df[col] = default
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default)

    if "SKU" not in df.columns:
        df.insert(0, "SKU", [f"SKU-{i}" for i in range(len(df))])
    if "Prodotto" not in df.columns:
        df["Prodotto"] = df.get("Nome", df.get("Product", df["SKU"]))
    if "Categoria" not in df.columns:
        df["Categoria"] = "Altro"
    if "Fornitore" not in df.columns:
        df["Fornitore"] = "Fornitore Generico"
    if "Email_Fornitore" not in df.columns:
        df["Email_Fornitore"] = "acquisti@fornitore.it"

    df["Valore Totale (€)"] = df["Costo Unitario (€)"] * df["Giacenza"]
    return df


# ── Analytic helpers ──────────────────────────────────────────────────────────
@st.cache_data
def generate_historical_sales(df: pd.DataFrame, history_days: int = 90) -> dict:
    rng = np.random.default_rng(seed=7)
    end_date = date.today()
    dates = [end_date - timedelta(days=history_days - 1 - i) for i in range(history_days)]
    base_rates = (df["Giacenza"] / df["Lead Time (giorni)"].replace(0, 1)).values
    sales_dict = {}
    for idx, row in df.reset_index(drop=True).iterrows():
        base = base_rates[idx]
        trend = np.linspace(0, base * 0.15, history_days)
        seasonality = base * 0.10 * np.sin(np.linspace(0, 4 * np.pi, history_days))
        noise = rng.normal(0, base * 0.08, history_days)
        daily = np.clip(base + trend + seasonality + noise, 0.01, None)
        sales_dict[row["SKU"]] = pd.DataFrame({"Data": dates, "Vendite": np.round(daily, 2)})
    return sales_dict


@st.cache_data
def run_forecast(sku: str, _sales_dict: dict, forecast_days: int = 30):
    hist = _sales_dict[sku].copy()
    X = np.arange(len(hist)).reshape(-1, 1)
    y = hist["Vendite"].values
    model = LinearRegression().fit(X, y)
    hist["Fitted"] = model.predict(X)
    future_X = np.arange(len(hist), len(hist) + forecast_days).reshape(-1, 1)
    future_dates = [hist["Data"].iloc[-1] + timedelta(days=i + 1) for i in range(forecast_days)]
    future_sales = np.clip(model.predict(future_X), 0.01, None)
    future_df = pd.DataFrame({"Data": future_dates, "Previsione": np.round(future_sales, 2)})
    return hist, future_df, float(future_sales.mean()), model.coef_[0]


def compute_days_to_stockout(df: pd.DataFrame, sales_dict: dict) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        _, _, avg_daily, _ = run_forecast(row["SKU"], sales_dict)
        usable = max(row["Giacenza"] - row["Scorta Sicurezza"], 0)
        days = usable / avg_daily if avg_daily > 0 else float("inf")
        rows.append({
            "SKU": row["SKU"], "Prodotto": row["Prodotto"],
            "Giacenza": row["Giacenza"], "Scorta Sicurezza": row["Scorta Sicurezza"],
            "Consumo Giorn. Prev. (u/g)": round(avg_daily, 2),
            "Giorni Stimati al Stockout": round(days, 1) if days != float("inf") else 9999,
        })
    return pd.DataFrame(rows).sort_values("Giorni Stimati al Stockout")


def compute_eoq(df: pd.DataFrame, sales_dict: dict) -> pd.DataFrame:
    rows = []
    for _, row in df.iterrows():
        _, _, avg_daily, _ = run_forecast(row["SKU"], sales_dict)
        annual_demand = avg_daily * 365
        S = row["Costo Ordine S (€)"]
        H = row["Costo Mantenimento H (€/u/anno)"]
        eoq = math.sqrt(2 * annual_demand * S / H) if H > 0 else 0
        eoq = max(1, round(eoq))
        usable = max(row["Giacenza"] - row["Scorta Sicurezza"], 0)
        days_left = usable / avg_daily if avg_daily > 0 else float("inf")
        is_below_ss = row["Giacenza"] < row["Scorta Sicurezza"]
        is_at_risk = days_left < 45
        if is_below_ss or is_at_risk:
            order_cost = eoq * row["Costo Unitario (€)"]
            urgency = "🔴 SOTTO SCORTA" if is_below_ss else (
                "🟠 CRITICO" if days_left < 14 else "🟡 A RISCHIO"
            )
            rows.append({
                "SKU": row["SKU"], "Prodotto": row["Prodotto"], "Categoria": row["Categoria"],
                "Domanda AI (u/g)": round(avg_daily, 2),
                "Domanda Annua (u)": round(annual_demand),
                "Costo Ordine S (€)": S, "Costo Mantenimento H (€/u/a)": H,
                "EOQ (unità)": eoq, "Costo Stimato Ordine (€)": round(order_cost, 2),
                "Giorni Rimasti": round(days_left, 1) if days_left < 9999 else 999,
                "Urgenza": urgency,
            })
    return pd.DataFrame(rows).sort_values("Giorni Rimasti")


def generate_supplier_scorecard(df: pd.DataFrame) -> pd.DataFrame:
    """Generate simulated supplier performance scorecard from inventory data."""
    rng = np.random.default_rng(seed=123)
    grp = df.groupby("Fornitore").agg(
        N_SKU=("SKU", "count"),
        Lead_Time_Medio=("Lead Time (giorni)", "mean"),
        Valore_Gestito=("Valore Totale (€)", "sum"),
    ).reset_index()
    n = len(grp)
    # Simulate realistic variation: better suppliers have lower lead times
    base_puntualita = np.clip(95 - grp["Lead_Time_Medio"].values * 0.4 + rng.normal(0, 5, n), 62, 99)
    base_accuratezza = np.clip(88 - grp["Lead_Time_Medio"].values * 0.3 + rng.normal(0, 6, n), 58, 98)
    base_fill = np.clip(94 - grp["Lead_Time_Medio"].values * 0.05 + rng.normal(0, 3, n), 76, 99.5)
    grp["Puntualità Consegna (%)"] = base_puntualita.round(1)
    grp["Accuratezza Lead Time (%)"] = base_accuratezza.round(1)
    grp["Order Fill Rate (%)"] = base_fill.round(1)
    grp["Ordini Storici (sim.)"] = rng.integers(8, 48, n)
    grp["Score Globale"] = (
        grp["Puntualità Consegna (%)"] * 0.40 +
        grp["Accuratezza Lead Time (%)"] * 0.35 +
        grp["Order Fill Rate (%)"] * 0.25
    ).round(1)
    grp = grp.sort_values("Score Globale", ascending=False).reset_index(drop=True)
    medals = {0: "🥇", 1: "🥈", 2: "🥉"}
    grp["Rank"] = [medals.get(i, f"#{i+1}") for i in range(len(grp))]
    grp["Rating"] = grp["Score Globale"].apply(
        lambda s: "⭐ Eccellente" if s >= 87 else ("✅ Buono" if s >= 78 else "⚠️ Da Migliorare")
    )
    grp["Lead_Time_Medio"] = grp["Lead_Time_Medio"].round(1)
    return grp


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    if LOTTIE_OK:
        lottie_data = load_lottie_url(
            "https://lottie.host/8c69d80c-0cf3-406a-a169-2f4cf5a04eb7/pWcE8N5eR4.json"
        )
        if lottie_data:
            st_lottie(lottie_data, height=110, key="sidebar_lottie", speed=0.8)
        else:
            st.image("https://img.icons8.com/fluency/96/warehouse.png", width=64)
    else:
        st.image("https://img.icons8.com/fluency/96/warehouse.png", width=64)

    st.title("LogiSense")
    st.caption("Supply Chain Platform v2.0")
    st.divider()

    # ── File uploader ──────────────────────────────────────────────────────────
    st.subheader("📂 Carica Inventario")
    uploaded_file = st.file_uploader(
        "CSV o Excel (.csv, .xlsx)",
        type=["csv", "xlsx", "xls"],
        help="Se caricato, sostituisce il dataset mock. Le colonne devono includere: SKU, Giacenza, Scorta Sicurezza.",
        label_visibility="collapsed",
    )
    if uploaded_file is not None:
        st.success(f"✅ {uploaded_file.name}")
    else:
        st.caption("🔷 Usando dataset demo (15 SKU)")

    st.divider()
    st.subheader("⚙️ Stress Test")
    demand_shock = st.slider(
        "Aumento Improvviso Domanda (%)",
        min_value=0, max_value=100, value=0, step=5,
        help="Simula un'impennata della domanda in percentuale.",
    )
    supplier_delay = st.slider(
        "Ritardo Fornitori (Giorni)",
        min_value=0, max_value=30, value=0, step=1,
        help="Aggiunge giorni extra al Lead Time originale.",
    )
    st.divider()
    st.subheader("📈 Previsione Domanda")

    # Load data (file or mock) — done here so forecast_sku selectbox has options
    if uploaded_file is not None:
        df_base = load_uploaded_inventory(uploaded_file)
    else:
        df_base = load_mock_inventory()

    forecast_sku = st.selectbox(
        "Articolo da analizzare",
        options=df_base["SKU"].tolist(),
        format_func=lambda s: f"{s} — {df_base.loc[df_base['SKU'] == s, 'Prodotto'].values[0]}",
        help="Seleziona l'articolo per il grafico di previsione.",
    )
    st.divider()
    st.caption("Usa i cursori per simulare scenari di crisi in tempo reale.")


# ── Pre-compute analytics ─────────────────────────────────────────────────────
sales_history = generate_historical_sales(df_base)
days_to_stockout_df = compute_days_to_stockout(df_base, sales_history)
critical_row = days_to_stockout_df.iloc[0]
critical_product = critical_row["Prodotto"]
critical_days = critical_row["Giorni Stimati al Stockout"]


def compute_stress(df: pd.DataFrame, demand_pct: int, extra_days: int) -> pd.DataFrame:
    out = df.copy()
    daily_consumption = out["Giacenza"] / out["Lead Time (giorni)"].replace(0, 1)
    effective_lead_time = out["Lead Time (giorni)"] + extra_days
    demand_multiplier = 1 + demand_pct / 100
    consumed = daily_consumption * demand_multiplier * effective_lead_time
    out["Giacenza Stress"] = (out["Giacenza"] - consumed).clip(lower=0).round(0).astype(int)
    out["Stockout"] = out["Giacenza Stress"] < out["Scorta Sicurezza"]
    out["Delta Giacenza"] = out["Giacenza Stress"] - out["Giacenza"]
    return out


df_stress = compute_stress(df_base, demand_shock, supplier_delay)


# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊  Dashboard & KPI",
    "🔥  Stress Test Simulator",
    "🤖  Copilota AI",
    "🛒  Gestione Ordini (EOQ)",
    "🚀  Smart Execution",
])


# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — Dashboard & KPI
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    source_label = f"📂 File: {uploaded_file.name}" if uploaded_file else "🔷 Dataset Demo"
    st.markdown("### 📊 Dashboard & KPI del Magazzino <small style='font-size:0.55em;color:#64748b;'>🔷 Dataset Demo</small>", unsafe_allow_html=True)

    alerts_normal = int((df_base["Giacenza"] < df_base["Scorta Sicurezza"]).sum())
    alerts_stress = int(df_stress["Stockout"].sum())
    total_value = df_base["Valore Totale (€)"].sum()
    num_skus = len(df_base)

    # ── Premium KPI Cards ──────────────────────────────────────────────────────
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi_card(
            "Valore Totale Magazzino", f"€ {total_value:,.0f}",
            icon="💰", delta=f"{num_skus} SKU attivi", delta_type="neutral",
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            "Articoli Totali (SKU)", str(num_skus),
            icon="📦", delta=df_base["Categoria"].nunique().__str__() + " categorie", delta_type="neutral",
        ), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(
            "Alert Sotto Scorta", str(alerts_normal),
            icon="🔴",
            delta=f"{'↑ ' + str(alerts_normal) + ' critici' if alerts_normal > 0 else '✅ Nessun alert'}",
            delta_type="down" if alerts_normal > 0 else "up",
        ), unsafe_allow_html=True)
    with c4:
        delta_stress = alerts_stress - alerts_normal
        st.markdown(kpi_card(
            "Stockout Scenario Stress", str(alerts_stress),
            icon="⚠️",
            delta=f"{'↑ +' + str(delta_stress) + ' rispetto al normale' if delta_stress > 0 else '= nessun peggioramento'}",
            delta_type="down" if delta_stress > 0 else "neutral",
        ), unsafe_allow_html=True)
    with c5:
        st.markdown(kpi_card(
            "Giorni al Stockout (min)", f"{critical_days:.0f} gg" if critical_days < 9999 else "∞",
            icon="⏱️",
            delta=f"{'↓ ' if critical_days < 30 else ''}{critical_product}",
            delta_type="down" if critical_days < 30 else "neutral",
        ), unsafe_allow_html=True)

    st.divider()

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.subheader("Valore per Categoria")
        cat_val = (
            df_base.groupby("Categoria")["Valore Totale (€)"]
            .sum().sort_values(ascending=False).reset_index()
        )
        fig_pie = go.Figure(go.Pie(
            labels=cat_val["Categoria"], values=cat_val["Valore Totale (€)"],
            hole=0.42, textinfo="label+percent",
        ))
        fig_pie.update_layout(
            margin=dict(t=10, b=10, l=10, r=10), showlegend=False,
            height=320, paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_b:
        st.subheader("Giacenza vs Scorta di Sicurezza")
        colors = ["#ef4444" if g < s else "#22c55e"
                  for g, s in zip(df_base["Giacenza"], df_base["Scorta Sicurezza"])]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            x=df_base["Prodotto"], y=df_base["Giacenza"],
            name="Giacenza Attuale", marker_color=colors,
        ))
        fig_bar.add_trace(go.Scatter(
            x=df_base["Prodotto"], y=df_base["Scorta Sicurezza"],
            mode="lines+markers", name="Scorta di Sicurezza",
            line=dict(color="#f59e0b", dash="dash", width=2), marker=dict(size=6),
        ))
        fig_bar.update_layout(
            xaxis_tickangle=-35, margin=dict(t=10, b=10, l=0, r=0),
            legend=dict(orientation="h", y=1.1), height=320,
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()

    selected_product = df_base.loc[df_base["SKU"] == forecast_sku, "Prodotto"].values[0]
    selected_row = df_base.loc[df_base["SKU"] == forecast_sku].iloc[0]
    st.subheader(f"📈 Previsione Domanda — {selected_product}")
    st.caption("Modello: Regressione Lineare (scikit-learn) · Storico 90 gg · Orizzonte 30 gg")

    hist_df, future_df, avg_daily_forecast, trend_coef = run_forecast(forecast_sku, sales_history)
    usable_stock = max(selected_row["Giacenza"] - selected_row["Scorta Sicurezza"], 0)
    days_until_ss = usable_stock / avg_daily_forecast if avg_daily_forecast > 0 else float("inf")
    stockout_date = date.today() + timedelta(days=int(days_until_ss)) if days_until_ss < 9999 else None

    kf1, kf2, kf3 = st.columns(3)
    with kf1:
        st.markdown(kpi_card(
            "Consumo Medio Previsto", f"{avg_daily_forecast:.1f} u/g",
            icon="📉",
            delta=f"trend {'↑' if trend_coef > 0 else '↓'} {abs(trend_coef):.3f} u/g/giorno",
            delta_type="down" if trend_coef > 0 else "up",
        ), unsafe_allow_html=True)
    with kf2:
        st.markdown(kpi_card(
            "Giorni Stimati al Stockout",
            f"{days_until_ss:.0f} gg" if days_until_ss < 9999 else "∞",
            icon="⏱️",
            delta=f"Stima: {stockout_date}" if stockout_date else "Scorta sufficiente",
            delta_type="down" if days_until_ss < 30 else "neutral",
        ), unsafe_allow_html=True)
    with kf3:
        st.markdown(kpi_card(
            "Scorta Residua Utile", f"{usable_stock:.0f} u",
            icon="📦",
            delta=f"sopra min. di {int(selected_row['Scorta Sicurezza'])} u",
            delta_type="up" if usable_stock > 0 else "down",
        ), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    fig_fc = go.Figure()
    fig_fc.add_trace(go.Scatter(
        x=hist_df["Data"].astype(str), y=hist_df["Vendite"],
        mode="lines", name="Vendite Storiche",
        line=dict(color="#93c5fd", width=1.2), opacity=0.7,
    ))
    fig_fc.add_trace(go.Scatter(
        x=hist_df["Data"].astype(str), y=hist_df["Fitted"],
        mode="lines", name="Trend Storico (LR)",
        line=dict(color="#3b82f6", width=2),
    ))
    fig_fc.add_trace(go.Scatter(
        x=future_df["Data"].astype(str), y=future_df["Previsione"],
        mode="lines+markers", name="Previsione 30 gg",
        line=dict(color="#f97316", width=2.5, dash="dash"),
        marker=dict(size=4, color="#f97316"),
    ))
    today_str = str(date.today())
    fig_fc.add_vline(x=today_str, line_dash="dot", line_color="#6b7280",
                     annotation_text="Oggi", annotation_position="top right")
    if stockout_date and days_until_ss < 120:
        fig_fc.add_vline(x=str(stockout_date), line_dash="dash", line_color="#ef4444",
                         annotation_text=f"⚠️ Stockout ({stockout_date})",
                         annotation_position="top left", annotation_font_color="#ef4444")
    fig_fc.update_layout(
        xaxis_title="Data", yaxis_title="Unità/giorno",
        legend=dict(orientation="h", y=1.08),
        margin=dict(t=20, b=10, l=0, r=0), height=380,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
        yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
    )
    st.plotly_chart(fig_fc, use_container_width=True)

    with st.expander("📋 Giorni Stimati al Stockout — tutti gli articoli", expanded=False):
        dts_display = days_to_stockout_df.copy()
        dts_display["Giorni Stimati al Stockout"] = dts_display["Giorni Stimati al Stockout"].apply(
            lambda x: "∞" if x >= 9999 else f"{x:.0f}"
        )
        dts_display["Urgenza"] = dts_display["Giorni Stimati al Stockout"].apply(
            lambda x: "🔴 CRITICO" if x not in ("∞",) and float(x) < 14
            else ("🟡 ATTENZIONE" if x not in ("∞",) and float(x) < 45 else "✅ OK")
        )
        def highlight_urgency(row):
            if "CRITICO" in str(row["Urgenza"]):
                return ["background-color: #fee2e2; color: #991b1b"] * len(row)
            if "ATTENZIONE" in str(row["Urgenza"]):
                return ["background-color: #fef9c3; color: #92400e"] * len(row)
            return [""] * len(row)
        st.dataframe(dts_display.style.apply(highlight_urgency, axis=1),
                     use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("📦 Inventario Completo")
    display_df = df_base.copy()
    display_df["⚠️ Alert"] = display_df.apply(
        lambda r: "🔴 SOTTO SCORTA" if r["Giacenza"] < r["Scorta Sicurezza"] else "✅ OK", axis=1,
    )
    def highlight_alert(row):
        if row["Giacenza"] < row["Scorta Sicurezza"]:
            return ["background-color: #fee2e2; color: #991b1b"] * len(row)
        return [""] * len(row)

    show_cols = ["SKU", "Prodotto", "Categoria", "Fornitore",
                 "Costo Unitario (€)", "Giacenza", "Scorta Sicurezza",
                 "Lead Time (giorni)", "Valore Totale (€)", "⚠️ Alert"]
    show_cols = [c for c in show_cols if c in display_df.columns]
    fmt = {c: f for c, f in {"Costo Unitario (€)": "€ {:.2f}", "Valore Totale (€)": "€ {:,.2f}"}.items()
           if c in display_df.columns}
    styled = display_df[show_cols].style.apply(highlight_alert, axis=1).format(fmt)
    st.dataframe(styled, use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — Stress Test Simulator
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("🔥 Stress Test Simulator")
    st.markdown(
        f"**Scenario attivo:** domanda +**{demand_shock}%** | ritardo fornitori +**{supplier_delay}** giorni  \n"
        "Regola i cursori nella sidebar per simulare scenari di crisi in tempo reale."
    )

    stockout_items = df_stress[df_stress["Stockout"]]["Prodotto"].tolist()
    if stockout_items:
        st.error(
            f"⚠️  **{len(stockout_items)} articoli in Stockout nello scenario di stress:** "
            + ", ".join(stockout_items)
        )
    else:
        st.success("✅ Nessun articolo va in stockout con i parametri correnti.")

    st.divider()

    # KPI stress cards
    cs1, cs2, cs3, cs4 = st.columns(4)
    with cs1:
        st.markdown(kpi_card("Domanda Simulata", f"+{demand_shock}%", icon="📈",
                              delta="rispetto al normale", delta_type="down" if demand_shock > 0 else "neutral"),
                    unsafe_allow_html=True)
    with cs2:
        st.markdown(kpi_card("Ritardo Fornitori", f"+{supplier_delay} gg", icon="🚚",
                              delta="extra al lead time", delta_type="down" if supplier_delay > 0 else "neutral"),
                    unsafe_allow_html=True)
    with cs3:
        st.markdown(kpi_card("Articoli in Stockout", str(len(stockout_items)), icon="🔴",
                              delta=f"su {len(df_base)} totali",
                              delta_type="down" if stockout_items else "up"),
                    unsafe_allow_html=True)
    with cs4:
        pct = round(len(stockout_items) / len(df_base) * 100, 1)
        st.markdown(kpi_card("% Catalogo a Rischio", f"{pct}%", icon="⚠️",
                              delta="del portafoglio SKU",
                              delta_type="down" if pct > 20 else ("neutral" if pct > 0 else "up")),
                    unsafe_allow_html=True)

    st.divider()
    st.subheader("Confronto Giacenza: Scenario Normale vs Stress")

    bar_colors_stress = ["#ef4444" if s else "#22c55e" for s in df_stress["Stockout"]]
    fig_compare = go.Figure()
    fig_compare.add_trace(go.Bar(
        name="Giacenza Normale", x=df_stress["Prodotto"], y=df_stress["Giacenza"],
        marker_color="#3b82f6", opacity=0.7,
    ))
    fig_compare.add_trace(go.Bar(
        name="Giacenza Post-Stress", x=df_stress["Prodotto"], y=df_stress["Giacenza Stress"],
        marker_color=bar_colors_stress,
    ))
    fig_compare.add_trace(go.Scatter(
        x=df_stress["Prodotto"], y=df_stress["Scorta Sicurezza"],
        mode="lines+markers", name="Scorta di Sicurezza",
        line=dict(color="#f59e0b", dash="dot", width=2), marker=dict(size=5),
    ))
    fig_compare.update_layout(
        barmode="group", xaxis_tickangle=-35,
        legend=dict(orientation="h", y=1.08),
        margin=dict(t=20, b=10, l=0, r=0), height=420,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_compare, use_container_width=True)

    st.subheader("Variazione Giacenza (Δ unità) per articolo")
    fig_delta = go.Figure(go.Bar(
        x=df_stress["Prodotto"], y=df_stress["Delta Giacenza"],
        marker_color=["#ef4444" if v < 0 else "#22c55e" for v in df_stress["Delta Giacenza"]],
        text=df_stress["Delta Giacenza"], textposition="outside",
    ))
    fig_delta.update_layout(
        xaxis_tickangle=-35, yaxis_title="Δ Giacenza (unità)",
        margin=dict(t=20, b=10, l=0, r=0), height=320,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig_delta, use_container_width=True)

    st.subheader("Dettaglio Articoli — Scenario di Stress")
    stress_display = df_stress[[
        "SKU", "Prodotto", "Categoria", "Giacenza",
        "Giacenza Stress", "Scorta Sicurezza", "Delta Giacenza", "Stockout",
    ]].copy()
    stress_display["Stockout"] = stress_display["Stockout"].map({True: "🔴 STOCKOUT", False: "✅ OK"})
    def highlight_stress(row):
        if "STOCKOUT" in str(row["Stockout"]):
            return ["background-color: #fee2e2; color: #991b1b"] * len(row)
        return [""] * len(row)
    st.dataframe(stress_display.style.apply(highlight_stress, axis=1),
                 use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — Copilota AI
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("🤖 Supply Chain Copilot VERO")
    st.caption("L'intelligenza di Gemini applicata ai tuoi dati logistici.")
    
    st.markdown("### 💬 Interroga il tuo Copilot AI")
    user_query = st.text_area("Fai una domanda complessa sui tuoi dati (es. 'Quali articoli hanno il lead time più alto in rapporto al loro costo?'):")
    
    if st.button("Invia al Copilot"):
        # Controlliamo se l'utente ha inserito la password di Gemini
        if not user_api_key:
            st.error("⚠️ Attenzione: Inserisci la tua API Key di Gemini nella barra laterale sinistra per sbloccare l'AI!")
        elif not user_query:
            st.warning("Scrivi una domanda prima di cliccare invio.")
        else:
            # Configura l'AI con la tua chiave segreta
            genai.configure(api_key=user_api_key)
            
            # Usiamo Gemini 1.5 Flash (veloce e gratuito)
            # Cerchiamo in automatico il modello corretto per il tuo account
            modelli_validi = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            modello_scelto = modelli_validi[0] # Prende il primo modello funzionante garantito
            
            # Preferiamo un modello della famiglia Gemini
            for m in modelli_validi:
                if "gemini" in m.lower():
                    modello_scelto = m
                    break
                    
            model = genai.GenerativeModel(modello_scelto)
            
            with st.spinner("🧠 Gemini sta analizzando i dati del tuo magazzino..."):
                try:
                    # Diamo in pasto all'AI il tuo foglio Excel convertito in testo
                    contesto_dati = df_base.to_string(index=False) 
                    
                    # Creiamo il "cervello" dell'AI
                    prompt_avanzato = f"""
                    Sei un Supply Chain Manager esperto di livello direzionale. 
                    Questa è la tabella con i dati reali del mio magazzino attuale:
                    {contesto_dati}
                    
                    Basandoti ESCLUSIVAMENTE sui dati qui sopra, rispondi in modo professionale, 
                    analitico e in lingua italiana alla seguente richiesta dell'utente:
                    "{user_query}"
                    
                    Se ti vengono chiesti calcoli, falli basandoti sui numeri della tabella.
                    Se ti viene chiesta un'email, scrivila pronta per essere copiata.
                    """
                    
                    # Facciamo la vera chiamata ai server di Google
                    risposta = model.generate_content(prompt_avanzato)
                    
                    # Mostriamo il risultato
                    st.success("✅ Analisi completata!")
                    st.markdown("---")
                    st.markdown(risposta.text)
                    st.markdown("---")
                    
                except Exception as e:
                    st.error(f"Si è verificato un errore di connessione con l'AI: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — Gestione Ordini (EOQ)
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    if "order_history" not in st.session_state:
        st.session_state.order_history = []
    if "last_approval_id" not in st.session_state:
        st.session_state.last_approval_id = None

    st.header("🛒 Gestione Ordini Automatici — EOQ")
    st.markdown(
        "Il sistema identifica gli articoli **sotto scorta di sicurezza** o "
        "**a rischio stockout entro 45 giorni** (stima AI) e calcola la quantità "
        "ottimale da ordinare tramite la formula **EOQ** (*Economic Order Quantity*)."
    )

    with st.expander("ℹ️ Come funziona il calcolo EOQ", expanded=False):
        st.markdown(r"""
**Formula:** $EOQ = \sqrt{\dfrac{2 \cdot D \cdot S}{H}}$

| Parametro | Descrizione | Fonte |
|-----------|-------------|-------|
| **D** | Domanda annua prevista (unità/anno) | Modello AI (LR × 365) |
| **S** | Costo fisso per ordine emesso (€) | Dataset per ogni SKU |
| **H** | Costo di mantenimento annuo (€/u/anno) | Dataset (~20% costo unitario) |

L'EOQ minimizza il **costo totale** di emissione + stoccaggio.
""")

    st.divider()
    eoq_df = compute_eoq(df_base, sales_history)

    if eoq_df.empty:
        st.success("✅ Nessun articolo richiede un ordine al momento. Tutte le scorte sono nella norma.")
    else:
        total_order_value = eoq_df["Costo Stimato Ordine (€)"].sum()
        n_orders = len(eoq_df)
        n_critical = int((eoq_df["Urgenza"] == "🔴 SOTTO SCORTA").sum())
        total_eoq_units = int(eoq_df["EOQ (unità)"].sum())

        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.markdown(kpi_card("Ordini da Emettere", str(n_orders), icon="📋",
                                  delta="batch proposti", delta_type="neutral"),
                        unsafe_allow_html=True)
        with k2:
            st.markdown(kpi_card("Articoli Sotto Scorta", str(n_critical), icon="🔴",
                                  delta=f"{n_critical} urgenti" if n_critical > 0 else "nessuno",
                                  delta_type="down" if n_critical > 0 else "up"),
                        unsafe_allow_html=True)
        with k3:
            st.markdown(kpi_card("Unità Totali (EOQ)", f"{total_eoq_units:,}", icon="📦",
                                  delta="da ordinare", delta_type="neutral"),
                        unsafe_allow_html=True)
        with k4:
            st.markdown(kpi_card("Valore Totale Ordini", f"€ {total_order_value:,.0f}", icon="💶",
                                  delta="investimento ottimizzato", delta_type="neutral"),
                        unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📋 Ordini d'Acquisto Proposti")

        def highlight_eoq(row):
            if row["Urgenza"] == "🔴 SOTTO SCORTA":
                return ["background-color: #fee2e2; color: #991b1b"] * len(row)
            if row["Urgenza"] == "🟠 CRITICO":
                return ["background-color: #ffedd5; color: #9a3412"] * len(row)
            if row["Urgenza"] == "🟡 A RISCHIO":
                return ["background-color: #fef9c3; color: #92400e"] * len(row)
            return [""] * len(row)

        display_cols = [
            "Urgenza", "SKU", "Prodotto", "Categoria",
            "Domanda AI (u/g)", "Domanda Annua (u)",
            "EOQ (unità)", "Costo Stimato Ordine (€)", "Giorni Rimasti",
        ]
        styled_eoq = eoq_df[display_cols].style.apply(highlight_eoq, axis=1).format({
            "Costo Stimato Ordine (€)": "€ {:,.2f}",
            "Domanda AI (u/g)": "{:.2f}", "Giorni Rimasti": "{:.0f}",
        })
        st.dataframe(styled_eoq, use_container_width=True, hide_index=True)

        st.subheader("📊 Quantità EOQ per Articolo")
        bar_colors_eoq = [
            "#ef4444" if u == "🔴 SOTTO SCORTA"
            else "#f97316" if u == "🟠 CRITICO" else "#eab308"
            for u in eoq_df["Urgenza"]
        ]
        fig_eoq = go.Figure(go.Bar(
            x=eoq_df["Prodotto"], y=eoq_df["EOQ (unità)"],
            marker_color=bar_colors_eoq,
            text=eoq_df["EOQ (unità)"], textposition="outside",
            customdata=eoq_df[["Costo Stimato Ordine (€)", "Domanda AI (u/g)"]].values,
            hovertemplate=(
                "<b>%{x}</b><br>EOQ: %{y} unità<br>"
                "Costo: € %{customdata[0]:,.2f}<br>"
                "Domanda AI: %{customdata[1]:.2f} u/g<extra></extra>"
            ),
        ))
        fig_eoq.update_layout(
            xaxis_tickangle=-35, yaxis_title="Quantità da Ordinare (EOQ)",
            margin=dict(t=20, b=10, l=0, r=0), height=340,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_eoq, use_container_width=True)

        with st.expander("🔢 Dettaglio Parametri EOQ per ogni articolo", expanded=False):
            params_cols = [
                "SKU", "Prodotto", "Domanda Annua (u)",
                "Costo Ordine S (€)", "Costo Mantenimento H (€/u/a)",
                "EOQ (unità)", "Costo Stimato Ordine (€)",
            ]
            st.dataframe(
                eoq_df[params_cols].style.format({
                    "Costo Stimato Ordine (€)": "€ {:,.2f}",
                    "Costo Ordine S (€)": "€ {:.0f}",
                    "Costo Mantenimento H (€/u/a)": "€ {:.2f}",
                }),
                use_container_width=True, hide_index=True,
            )

        st.divider()
        st.subheader("✅ Approva ed Invia Ordini")

        col_btn, col_info = st.columns([1, 3])
        with col_btn:
            approve = st.button(
                "✅ Approva Ordini Automatici",
                type="primary", use_container_width=True, key="btn_approve",
            )

        if approve:
            new_order_id = f"ORD-{len(st.session_state.order_history) + 1:04d}"
            sku_detail = [
                {"SKU": r["SKU"], "Prodotto": r["Prodotto"],
                 "EOQ (unità)": r["EOQ (unità)"], "Costo (€)": r["Costo Stimato Ordine (€)"],
                 "Urgenza": r["Urgenza"]}
                for _, r in eoq_df.iterrows()
            ]
            st.session_state.order_history.append({
                "ID Ordine": new_order_id,
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "N° SKU": n_orders, "Unità Totali": total_eoq_units,
                "Valore Totale (€)": round(total_order_value, 2),
                "Stato": "✅ Inviato ERP", "_dettaglio": sku_detail,
            })
            st.session_state.last_approval_id = new_order_id

        with col_info:
            if st.session_state.last_approval_id:
                last = next(
                    (o for o in reversed(st.session_state.order_history)
                     if o["ID Ordine"] == st.session_state.last_approval_id), None,
                )
                if last:
                    lines = "\n".join([
                        f"- **{d['Prodotto']}** ({d['SKU']}): {d['EOQ (unità)']} unità — € {d['Costo (€)']:,.2f}"
                        for d in last["_dettaglio"]
                    ])
                    st.success(
                        f"🎉 **Ordine {last['ID Ordine']} approvato e inviato al sistema ERP!**  \n"
                        f"_{last['Timestamp']}_\n\n{lines}\n\n"
                        f"**Valore totale impegnato: € {last['Valore Totale (€)']:,.2f}**  \n"
                        f"I fornitori riceveranno conferma via EDI entro 15 minuti."
                    )
            else:
                st.info(
                    f"Premi **'Approva Ordini Automatici'** per inviare tutti i {n_orders} ordini "
                    f"proposti al sistema ERP.\n\nValore da impegnare: **€ {total_order_value:,.2f}**"
                )

    st.divider()
    st.subheader("📜 Registro Storico Ordini (Audit Log)")

    if not st.session_state.order_history:
        st.info("📭 Nessun ordine approvato finora.")
    else:
        total_sessions = len(st.session_state.order_history)
        cumulative_value = sum(o["Valore Totale (€)"] for o in st.session_state.order_history)
        cumulative_skus = sum(o["N° SKU"] for o in st.session_state.order_history)

        hs1, hs2, hs3 = st.columns(3)
        with hs1:
            st.markdown(kpi_card("Sessioni di Ordine", str(total_sessions), icon="📋"), unsafe_allow_html=True)
        with hs2:
            st.markdown(kpi_card("SKU Totali Ordinati", str(cumulative_skus), icon="📦"), unsafe_allow_html=True)
        with hs3:
            st.markdown(kpi_card("Valore Cumulativo", f"€ {cumulative_value:,.0f}", icon="💶"), unsafe_allow_html=True)

        log_rows = [{k: v for k, v in o.items() if k != "_dettaglio"}
                    for o in reversed(st.session_state.order_history)]
        log_df = pd.DataFrame(log_rows)
        def highlight_log(row):
            return ["background-color: #f0fdf4; color: #166534"] * len(row)
        st.dataframe(
            log_df.style.apply(highlight_log, axis=1).format({"Valore Totale (€)": "€ {:,.2f}"}),
            use_container_width=True, hide_index=True,
        )

        st.caption("💡 Espandi un ordine per vedere il dettaglio SKU:")
        for entry in reversed(st.session_state.order_history):
            with st.expander(
                f"🧾 {entry['ID Ordine']} — {entry['Timestamp']} — "
                f"{entry['N° SKU']} SKU — € {entry['Valore Totale (€)']:,.2f}", expanded=False,
            ):
                detail_df = pd.DataFrame(entry["_dettaglio"])
                def highlight_detail(row):
                    if row["Urgenza"] == "🔴 SOTTO SCORTA":
                        return ["background-color: #fee2e2"] * len(row)
                    if row["Urgenza"] == "🟠 CRITICO":
                        return ["background-color: #ffedd5"] * len(row)
                    return ["background-color: #fef9c3"] * len(row)
                st.dataframe(
                    detail_df.style.apply(highlight_detail, axis=1).format({"Costo (€)": "€ {:,.2f}"}),
                    use_container_width=True, hide_index=True,
                )

        st.divider()
        csv_rows = [
            {"ID Ordine": o["ID Ordine"], "Timestamp": o["Timestamp"],
             "N° SKU": o["N° SKU"], "Unità Totali": o["Unità Totali"],
             "Valore Totale (€)": o["Valore Totale (€)"], "Stato": o["Stato"]}
            for o in st.session_state.order_history
        ]
        csv_bytes = pd.DataFrame(csv_rows).to_csv(index=False).encode("utf-8")
        dl_col, clear_col = st.columns(2)
        with dl_col:
            st.download_button(
                label="⬇️ Esporta Storico in CSV", data=csv_bytes,
                file_name="storico_ordini_logisense.csv",
                mime="text/csv", use_container_width=True,
            )
        with clear_col:
            if st.button("🗑️ Cancella Storico Ordini", key="btn_clear_history", use_container_width=True):
                st.session_state.order_history = []
                st.session_state.last_approval_id = None
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — Smart Execution + Supplier Scorecard
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("🚀 Smart Execution — Automazione & Performance Fornitori")

    subtab_a, subtab_b = st.tabs([
        "🏆  Supplier Performance Scorecard",
        "📬  Automazione Email Ordini",
    ])

    # ──────────────────────────────────────────────────────────────────────────
    # SUBTAB A — Supplier Performance Scorecard
    # ──────────────────────────────────────────────────────────────────────────
    with subtab_a:
        st.subheader("🏆 Supplier Performance Scorecard")
        st.markdown(
            "Valutazione comparativa dei fornitori basata su **puntualità di consegna**, "
            "**accuratezza lead time** e **order fill rate** — con ranking automatico e score globale ponderato."
        )
        st.divider()

        sc_df = generate_supplier_scorecard(df_base)

        # ── KPI cards row ──
        top_supp = sc_df.iloc[0]
        avg_score = sc_df["Score Globale"].mean()
        pct_excellent = round((sc_df["Score Globale"] >= 87).sum() / len(sc_df) * 100)
        worst_supp = sc_df.iloc[-1]

        sp1, sp2, sp3, sp4 = st.columns(4)
        with sp1:
            st.markdown(kpi_card(
                "Fornitore #1", top_supp["Fornitore"],
                icon="🥇",
                delta=f"Score {top_supp['Score Globale']}",
                delta_type="up",
            ), unsafe_allow_html=True)
        with sp2:
            st.markdown(kpi_card(
                "Score Medio Panel", f"{avg_score:.1f}",
                icon="📊",
                delta="su 100 punti",
                delta_type="up" if avg_score >= 80 else "neutral",
            ), unsafe_allow_html=True)
        with sp3:
            st.markdown(kpi_card(
                "Fornitori Eccellenti", f"{pct_excellent}%",
                icon="⭐",
                delta="score ≥ 87",
                delta_type="up" if pct_excellent >= 50 else "neutral",
            ), unsafe_allow_html=True)
        with sp4:
            st.markdown(kpi_card(
                "Da Monitorare", worst_supp["Fornitore"],
                icon="⚠️",
                delta=f"Score {worst_supp['Score Globale']}",
                delta_type="down" if worst_supp["Score Globale"] < 78 else "neutral",
            ), unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── Ranking table ──
        st.subheader("📋 Ranking Fornitori")
        sc_display = sc_df[[
            "Rank", "Fornitore", "N_SKU",
            "Puntualità Consegna (%)", "Accuratezza Lead Time (%)", "Order Fill Rate (%)",
            "Ordini Storici (sim.)", "Score Globale", "Rating",
        ]].rename(columns={
            "N_SKU": "SKU Gestiti",
            "Ordini Storici (sim.)": "Ordini Tot.",
        })

        def highlight_score(row):
            s = row["Score Globale"]
            if s >= 87:
                return ["background-color: #f0fdf4; color: #166534"] * len(row)
            if s >= 78:
                return ["background-color: #fef9c3; color: #92400e"] * len(row)
            return ["background-color: #fee2e2; color: #991b1b"] * len(row)

        st.dataframe(
            sc_display.style.apply(highlight_score, axis=1).format({
                "Puntualità Consegna (%)": "{:.1f}%",
                "Accuratezza Lead Time (%)": "{:.1f}%",
                "Order Fill Rate (%)": "{:.1f}%",
                "Score Globale": "{:.1f}",
            }),
            use_container_width=True, hide_index=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns([3, 2])

        with col_chart1:
            st.subheader("📊 Performance Comparativa per Metrica")
            metrics_cols = ["Puntualità Consegna (%)", "Accuratezza Lead Time (%)", "Order Fill Rate (%)"]
            sc_melt = sc_df.melt(
                id_vars="Fornitore",
                value_vars=metrics_cols,
                var_name="Metrica", value_name="Valore",
            )
            color_map = {
                "Puntualità Consegna (%)": "#3b82f6",
                "Accuratezza Lead Time (%)": "#8b5cf6",
                "Order Fill Rate (%)": "#22c55e",
            }
            fig_bar_sc = px.bar(
                sc_melt, x="Fornitore", y="Valore", color="Metrica",
                barmode="group",
                color_discrete_map=color_map,
                text_auto=".1f",
            )
            fig_bar_sc.update_layout(
                xaxis_tickangle=-30, yaxis_title="% Performance",
                yaxis_range=[50, 105],
                legend=dict(orientation="h", y=1.12),
                margin=dict(t=20, b=10, l=0, r=0), height=380,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            )
            fig_bar_sc.add_hline(y=87, line_dash="dot", line_color="#22c55e",
                                  annotation_text="⭐ Soglia Eccellente (87)",
                                  annotation_position="top right",
                                  annotation_font_color="#166534")
            fig_bar_sc.add_hline(y=78, line_dash="dot", line_color="#f59e0b",
                                  annotation_text="⚠️ Soglia Minima (78)",
                                  annotation_position="top right",
                                  annotation_font_color="#92400e")
            st.plotly_chart(fig_bar_sc, use_container_width=True)

        with col_chart2:
            st.subheader("🎯 Score Globale Ranking")
            sc_sorted = sc_df.sort_values("Score Globale")
            bar_colors_sc = [
                "#22c55e" if s >= 87 else ("#f59e0b" if s >= 78 else "#ef4444")
                for s in sc_sorted["Score Globale"]
            ]
            fig_rank = go.Figure(go.Bar(
                x=sc_sorted["Score Globale"],
                y=sc_sorted["Fornitore"],
                orientation="h",
                marker_color=bar_colors_sc,
                text=[f"{s:.1f}" for s in sc_sorted["Score Globale"]],
                textposition="outside",
            ))
            fig_rank.add_vline(x=87, line_dash="dot", line_color="#22c55e",
                                annotation_text="Eccellente", annotation_position="top right",
                                annotation_font_color="#166534")
            fig_rank.add_vline(x=78, line_dash="dot", line_color="#f59e0b",
                                annotation_text="Min. OK", annotation_position="bottom right",
                                annotation_font_color="#92400e")
            fig_rank.update_layout(
                xaxis_range=[50, 105], xaxis_title="Score Globale",
                margin=dict(t=20, b=10, l=0, r=10), height=380,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_rank, use_container_width=True)

        # ── Radar chart ──
        st.subheader("🕸️ Radar — Profilo Competitivo Fornitori")
        radar_cols = ["Puntualità Consegna (%)", "Accuratezza Lead Time (%)", "Order Fill Rate (%)"]
        theta_labels = ["Puntualità\nConsegna", "Accuratezza\nLead Time", "Order\nFill Rate"]
        palette = ["#3b82f6", "#8b5cf6", "#22c55e", "#f97316", "#ec4899",
                   "#14b8a6", "#eab308", "#ef4444"]
        fig_radar = go.Figure()
        for i, (_, row) in enumerate(sc_df.iterrows()):
            vals = [row[c] for c in radar_cols]
            vals_closed = vals + [vals[0]]
            labels_closed = theta_labels + [theta_labels[0]]
            color = palette[i % len(palette)]
            fig_radar.add_trace(go.Scatterpolar(
                r=vals_closed, theta=labels_closed,
                fill="toself", name=row["Fornitore"],
                line=dict(color=color, width=2),
                fillcolor=color.replace(")", ",0.08)").replace("rgb", "rgba") if "rgb" in color
                else f"rgba({int(color[1:3],16)},{int(color[3:5],16)},{int(color[5:7],16)},0.08)",
                opacity=0.85,
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[50, 100])),
            legend=dict(orientation="h", y=-0.15),
            margin=dict(t=30, b=60, l=40, r=40), height=420,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # ── Delivery trend lines ──
        st.subheader("📈 Trend Puntualità Consegne (Ultimi 12 Mesi Simulati)")
        rng2 = np.random.default_rng(seed=77)
        months = [(date.today().replace(day=1) - timedelta(days=30 * i)).strftime("%b %Y")
                  for i in range(11, -1, -1)]
        fig_trend = go.Figure()
        for i, (_, row) in enumerate(sc_df.iterrows()):
            base_val = row["Puntualità Consegna (%)"]
            trend_vals = np.clip(
                base_val + rng2.normal(0, 3, 12).cumsum() * 0.3 + rng2.normal(0, 2, 12),
                60, 100
            ).round(1)
            fig_trend.add_trace(go.Scatter(
                x=months, y=trend_vals.tolist(),
                mode="lines+markers",
                name=row["Fornitore"],
                line=dict(color=palette[i % len(palette)], width=2),
                marker=dict(size=5),
            ))
        fig_trend.add_hline(y=87, line_dash="dot", line_color="rgba(34,197,94,0.5)",
                             annotation_text="Target Eccellente")
        fig_trend.update_layout(
            xaxis_title="Mese", yaxis_title="Puntualità Consegna (%)",
            yaxis_range=[55, 105],
            legend=dict(orientation="h", y=1.08),
            margin=dict(t=20, b=10, l=0, r=0), height=360,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(200,200,200,0.2)"),
        )
        st.plotly_chart(fig_trend, use_container_width=True)

        # ── SKU concentration ──
        with st.expander("🔎 Concentrazione SKU per Fornitore", expanded=False):
            sku_conc = df_base.groupby("Fornitore").agg(
                SKU_Count=("SKU", "count"),
                Valore_Tot=("Valore Totale (€)", "sum"),
            ).reset_index().sort_values("Valore_Tot", ascending=False)
            fig_conc = px.treemap(
                sku_conc, path=["Fornitore"], values="Valore_Tot",
                color="SKU_Count",
                color_continuous_scale="Blues",
                custom_data=["SKU_Count"],
            )
            fig_conc.update_traces(
                texttemplate="<b>%{label}</b><br>€ %{value:,.0f}<br>%{customdata[0]} SKU",
            )
            fig_conc.update_layout(
                margin=dict(t=10, b=10, l=0, r=0), height=320,
                paper_bgcolor="rgba(0,0,0,0)",
            )
            st.plotly_chart(fig_conc, use_container_width=True)

    # ──────────────────────────────────────────────────────────────────────────
    # SUBTAB B — Automazione Email Ordini
    # ──────────────────────────────────────────────────────────────────────────
    with subtab_b:
        st.subheader("📬 Automazione Email Ordini")
        st.markdown(
            "Genera automaticamente bozze di **email d'ordine professionali in italiano** "
            "per ogni articolo sotto scorta minima, pronte da copiare in Outlook o Gmail."
        )
        st.divider()

        exec_eoq = compute_eoq(df_base, sales_history)

        if exec_eoq.empty:
            st.success(
                "✅ **Nessun articolo richiede un ordine urgente al momento.**\n\n"
                "Tutte le scorte sono sopra la soglia di sicurezza. "
                "Ricontrolla aumentando i parametri di stress nella sidebar."
            )
        else:
            supplier_info = df_base[["SKU", "Fornitore", "Email_Fornitore",
                                      "Lead Time (giorni)", "Costo Unitario (€)",
                                      "Giacenza", "Scorta Sicurezza"]]
            exec_eoq = exec_eoq.merge(supplier_info, on="SKU", how="left")

            n_exec = len(exec_eoq)
            total_exec_cost = exec_eoq["Costo Stimato Ordine (€)"].sum()
            n_exec_critical = int((exec_eoq["Urgenza"] == "🔴 SOTTO SCORTA").sum())
            n_suppliers = exec_eoq["Fornitore"].nunique()

            ec1, ec2, ec3, ec4 = st.columns(4)
            with ec1:
                st.markdown(kpi_card("Email da Generare", str(n_exec), icon="📧",
                                      delta="bozze pronte", delta_type="neutral"), unsafe_allow_html=True)
            with ec2:
                st.markdown(kpi_card("Articoli Sotto Scorta", str(n_exec_critical), icon="🔴",
                                      delta="ordine urgente" if n_exec_critical > 0 else "nessuno",
                                      delta_type="down" if n_exec_critical > 0 else "up"), unsafe_allow_html=True)
            with ec3:
                st.markdown(kpi_card("Fornitori Coinvolti", str(n_suppliers), icon="🏭",
                                      delta="da contattare", delta_type="neutral"), unsafe_allow_html=True)
            with ec4:
                st.markdown(kpi_card("Valore Totale Ordini", f"€ {total_exec_cost:,.0f}", icon="💶",
                                      delta="da impegnare", delta_type="neutral"), unsafe_allow_html=True)

            st.divider()
            st.subheader("📬 Bozze Email per i Fornitori")
            st.caption("Ogni espander contiene una bozza email pronta. Usa l'icona **📋 Copy** in alto a destra per copiarla.")

            today = date.today()

            for _, row in exec_eoq.iterrows():
                prodotto = row["Prodotto"]
                sku = row["SKU"]
                fornitore = row["Fornitore"]
                email_forn = row["Email_Fornitore"]
                eoq_qty = int(row["EOQ (unità)"])
                costo_totale = row["Costo Stimato Ordine (€)"]
                costo_unitario = row["Costo Unitario (€)"]
                lead_time = int(row["Lead Time (giorni)"])
                giacenza = int(row["Giacenza"])
                scorta_min = int(row["Scorta Sicurezza"])
                urgenza = row["Urgenza"]
                delivery_date = today + timedelta(days=lead_time)

                urgenza_label = {
                    "🔴 SOTTO SCORTA": "URGENTE — Sotto Scorta Minima",
                    "🟠 CRITICO": "CRITICO — Meno di 14 giorni",
                    "🟡 A RISCHIO": "A RISCHIO — Meno di 45 giorni",
                }.get(urgenza, urgenza)

                email_text = f"""A: {email_forn}
Oggetto: [ORDINE D'ACQUISTO] {prodotto} ({sku}) — Rif. LogiSense EOQ — {today.strftime('%d/%m/%Y')}

Gentile Team Commerciale di {fornitore},

con la presente, la nostra società desidera formalizzare un ordine d'acquisto per il \
prodotto indicato di seguito, generato automaticamente dal nostro sistema \
di gestione scorte LogiSense (EOQ — Economic Order Quantity).

──────────────────────────────────────────
  DETTAGLI ORDINE
──────────────────────────────────────────
  Prodotto         : {prodotto}
  Codice SKU       : {sku}
  Quantità (EOQ)   : {eoq_qty} unità
  Costo unitario   : € {costo_unitario:.2f}
  Valore totale    : € {costo_totale:,.2f}
  Data ordine      : {today.strftime('%d/%m/%Y')}
  Consegna richiesta: {delivery_date.strftime('%d/%m/%Y')} ({lead_time} giorni)
──────────────────────────────────────────

MOTIVAZIONE: {urgenza_label}.
Giacenza attuale: {giacenza} unità | Scorta minima: {scorta_min} unità.

Vi chiediamo gentilmente di:
  1. Confermare la disponibilità della merce
  2. Indicare la data di spedizione confermata
  3. Allegare il DDT (Documento di Trasporto) alla consegna

Modalità di pagamento: bonifico bancario a 30 giorni dalla data fattura (standard).

In attesa di un Vostro riscontro entro 24 ore lavorative,
porgiamo cordiali saluti.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ufficio Acquisti — LogiSense Supply Chain Platform
Sistema EOQ Automatizzato | {today.strftime('%d/%m/%Y')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""

                urgency_icon = {"🔴 SOTTO SCORTA": "🔴", "🟠 CRITICO": "🟠", "🟡 A RISCHIO": "🟡"}.get(urgenza, "📧")

                with st.expander(
                    f"{urgency_icon} Genera Ordine per: **{fornitore}** — {prodotto} "
                    f"({sku}) · {eoq_qty} u · € {costo_totale:,.2f}",
                    expanded=(urgenza == "🔴 SOTTO SCORTA"),
                ):
                    inf1, inf2, inf3, inf4 = st.columns(4)
                    with inf1:
                        st.markdown(kpi_card("Qtà EOQ", f"{eoq_qty} u", icon="📦"), unsafe_allow_html=True)
                    with inf2:
                        st.markdown(kpi_card("Valore Ordine", f"€ {costo_totale:,.2f}", icon="💶"), unsafe_allow_html=True)
                    with inf3:
                        st.markdown(kpi_card("Consegna Entro", delivery_date.strftime("%d/%m/%Y"), icon="🚚"), unsafe_allow_html=True)
                    with inf4:
                        st.markdown(kpi_card("Stato Scorta", urgenza, icon="📊",
                                              delta_type="down" if "SOTTO" in urgenza else "neutral"), unsafe_allow_html=True)

                    st.markdown(f"**📧 Destinatario:** `{email_forn}`")
                    st.markdown("**✉️ Bozza Email (clicca 📋 in alto a destra per copiare):**")
                    st.code(email_text, language="markdown")
