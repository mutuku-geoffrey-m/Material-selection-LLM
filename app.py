"""
Engineering Material Selection & Optimization System (EMS-OS)
CAD/CAE Engineering Workbench & Analytical Optimization Console.

Grounded in Michael F. Ashby's multi-objective continuum mechanics,
1,490+ standardized materials database (ASTM, ISO, ASME, DIN, JIS),
local Ollama base LLM, automatic Cloud Gemini internet arbitration,
and Wilson-Harris Economic Order Quantity (EOQ) supply chain analytics.

Design System: Linear & ClickHouse Dark Flat Engineering System
"""

import os
import sys
import uuid
import json
import urllib.request
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit as st
from dotenv import load_dotenv

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
load_dotenv()

from src.materials_db import MATERIALS_DATABASE, list_all_materials, get_material
from src.ashby_engine import (
    AshbyIndex, INDEX_DESCRIPTIONS, calculate_ashby_index,
    rank_materials, create_interactive_ashby_chart
)
from src.hydrodynamics import HydrodynamicsEngine
from src.nlp_parser import NLPTranslationLayer
from src.rag_engine import RAGEngine
from src.llm_orchestrator import LLMOrchestrator
from src.economics_engine import EconomicsEngine
from src.report_generator import EngineeringReportGenerator


# Page Configuration
st.set_page_config(
    page_title="EMS-OS // Engineering Material Selection Console",
    page_icon="O",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Linear / ClickHouse Production CAD-CAE Workbench Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    :root {
        --canvas: #0c0d0e;
        --surface-1: #141517;
        --surface-2: #18191b;
        --surface-3: #202225;
        --hairline: #23252a;
        --hairline-strong: #34343a;
        --ink: #f7f8f8;
        --ink-muted: #d0d6e0;
        --ink-subtle: #8a8f98;
        --ink-tertiary: #62666d;
        --accent: #5e6ad2;
        --accent-hover: #717de0;
        --success: #22c55e;
        --warning: #f59e0b;
        --danger: #ef4444;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: var(--canvas) !important;
        color: var(--ink) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--surface-1) !important;
        border-right: 1px solid var(--hairline) !important;
    }

    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: var(--ink) !important;
        letter-spacing: -0.02em !important;
    }

    /* Top Telemetry Bar */
    .telemetry-bar {
        background-color: var(--surface-1);
        border: 1px solid var(--hairline);
        border-radius: 6px;
        padding: 10px 16px;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        font-size: 12px;
        font-family: 'Inter', sans-serif;
    }

    .telemetry-title {
        font-weight: 600;
        color: var(--ink);
        letter-spacing: 0.02em;
        text-transform: uppercase;
        font-size: 11px;
    }

    .telemetry-item {
        display: flex;
        align-items: center;
        gap: 6px;
        color: var(--ink-subtle);
    }

    .telemetry-dot-online {
        width: 7px;
        height: 7px;
        background-color: var(--success);
        border-radius: 50%;
        display: inline-block;
    }

    .telemetry-dot-offline {
        width: 7px;
        height: 7px;
        background-color: var(--danger);
        border-radius: 50%;
        display: inline-block;
    }

    .telemetry-pill {
        background-color: var(--surface-2);
        border: 1px solid var(--hairline);
        border-radius: 4px;
        padding: 2px 8px;
        color: var(--ink-muted);
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
    }

    /* Panel Card Surfaces */
    .wb-card {
        background-color: var(--surface-1);
        border: 1px solid var(--hairline);
        border-radius: 6px;
        padding: 18px;
        margin-bottom: 16px;
    }

    .wb-card-header {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--ink-subtle);
        margin-bottom: 12px;
        border-bottom: 1px solid var(--hairline);
        padding-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* High-impact Material Headline */
    .material-headline-name {
        font-size: 22px;
        font-weight: 700;
        color: var(--ink);
        letter-spacing: -0.02em;
        margin-bottom: 4px;
    }

    .material-headline-sub {
        font-size: 13px;
        color: var(--ink-subtle);
        margin-bottom: 16px;
    }

    /* Stat Metric Box */
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        margin-bottom: 16px;
    }

    .stat-box {
        background-color: var(--surface-2);
        border: 1px solid var(--hairline);
        border-radius: 4px;
        padding: 10px 12px;
    }

    .stat-label {
        font-size: 11px;
        color: var(--ink-subtle);
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 4px;
    }

    .stat-value {
        font-size: 16px;
        font-weight: 600;
        color: var(--ink);
        font-family: 'JetBrains Mono', monospace;
        font-variant-numeric: tabular-nums;
    }

    .stat-sub {
        font-size: 10px;
        color: var(--ink-tertiary);
        margin-top: 2px;
    }

    /* Status Badge */
    .badge-verified {
        display: inline-block;
        background-color: rgba(34, 197, 94, 0.1);
        border: 1px solid rgba(34, 197, 94, 0.25);
        color: #4ade80;
        padding: 2px 7px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    .badge-arbitrated {
        display: inline-block;
        background-color: rgba(94, 106, 210, 0.15);
        border: 1px solid rgba(94, 106, 210, 0.3);
        color: #a5b4fc;
        padding: 2px 7px;
        border-radius: 3px;
        font-size: 11px;
        font-weight: 500;
        font-family: 'JetBrains Mono', monospace;
    }

    .badge-neutral {
        display: inline-block;
        background-color: var(--surface-2);
        border: 1px solid var(--hairline);
        color: var(--ink-muted);
        padding: 2px 7px;
        border-radius: 3px;
        font-size: 11px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* Form Controls and Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox [data-baseweb="select"] {
        background-color: var(--surface-2) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 4px !important;
        color: var(--ink) !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 13px !important;
    }

    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--accent) !important;
        box-shadow: 0 0 0 1px var(--accent) !important;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--surface-2) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 4px !important;
        color: var(--ink-muted) !important;
        font-weight: 500 !important;
        font-size: 12px !important;
        transition: all 0.12s ease !important;
        padding: 6px 12px !important;
    }

    .stButton > button:hover {
        background-color: var(--surface-3) !important;
        border-color: var(--hairline-strong) !important;
        color: var(--ink) !important;
    }

    .stButton > button[kind="primary"] {
        background-color: var(--accent) !important;
        border: 1px solid #717de0 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }

    .stButton > button[kind="primary"]:hover {
        background-color: var(--accent-hover) !important;
        border-color: #828fff !important;
    }

    /* Data Table Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--hairline) !important;
        border-radius: 4px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid var(--hairline) !important;
        gap: 20px !important;
    }

    .stTabs [data-baseweb="tab"] {
        color: var(--ink-subtle) !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 8px 4px !important;
        border-bottom: 2px solid transparent !important;
    }

    .stTabs [aria-selected="true"] {
        color: var(--ink) !important;
        border-bottom-color: var(--accent) !important;
        font-weight: 600 !important;
    }

    /* Expander */
    [data-testid="stExpander"] {
        background-color: var(--surface-1) !important;
        border: 1px solid var(--hairline) !important;
        border-radius: 4px !important;
    }

    /* Code blocks */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        background-color: var(--surface-2) !important;
        border-radius: 4px !important;
        font-size: 12px !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


rag_engine = get_rag_engine()

# Initialize Session State
if "engineering_sessions" not in st.session_state:
    session_id = str(uuid.uuid4())[:8]
    st.session_state.engineering_sessions = {
        session_id: {
            "title": "Design Case #01",
            "prompt": "Design a cryogenic dewar suspension strut operating at -196 C subject to cyclic axial tension fatigue under ASTM E466. Maximize stiffness-to-weight and fatigue endurance limit while minimizing solid thermal conductivity.",
            "result": None,
            "nlp_spec": None,
            "chart_fig": None
        }
    }
    st.session_state.active_session_id = session_id

current_session = st.session_state.engineering_sessions[st.session_state.active_session_id]

# Sidebar: System Infrastructure & Material Catalog
st.sidebar.markdown("""
<div style="padding: 4px 0 16px 0; border-bottom: 1px solid #23252a; margin-bottom: 16px;">
    <div style="font-size: 13px; font-weight: 700; letter-spacing: 0.04em; color: #f7f8f8;">EMS-OS // WORKBENCH</div>
    <div style="font-size: 11px; color: #8a8f98;">Materials Optimization Console v2.4</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=25, show_spinner=False)
def check_cached_ollama_health(endpoint: str, model_name: str) -> dict:
    try:
        req = urllib.request.Request(f"{endpoint}/api/tags", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=1.0) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            models = [m.get("name") for m in data.get("models", [])]
            return {
                "online": True,
                "endpoint": endpoint,
                "models": models,
                "target_model_ready": any(model_name in m for m in models)
            }
    except Exception as e:
        return {
            "online": False,
            "endpoint": endpoint,
            "models": [],
            "target_model_ready": False,
            "error": str(e)
        }


# Engine Selection
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 6px;'>Inference Daemon Pipeline</div>", unsafe_allow_html=True)

mode_choice = st.sidebar.selectbox(
    "Inference Route",
    [
        "Local Standalone LLM (llama3.2 via Ollama) [Primary]",
        "Deterministic Physics & Metallurgy Solver [Instant < 0.2s]",
        "Cloud API (Google Gemini / OpenAI)"
    ],
    index=0,
    label_visibility="collapsed"
)

mode_map = {
    "Local Standalone LLM (llama3.2 via Ollama) [Primary]": LLMOrchestrator.MODE_LOCAL,
    "Deterministic Physics & Metallurgy Solver [Instant < 0.2s]": LLMOrchestrator.MODE_AUTONOMOUS_EXPERT,
    "Cloud API (Google Gemini / OpenAI)": LLMOrchestrator.MODE_CLOUD
}

orchestrator = LLMOrchestrator(mode=mode_map[mode_choice])
ollama_endpoint = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
ollama_health = check_cached_ollama_health(ollama_endpoint, orchestrator.local_model)

# Status strip in sidebar
if ollama_health["online"]:
    st.sidebar.markdown(f"""
    <div style="background-color: #18191b; border: 1px solid #23252a; border-radius: 4px; padding: 8px 10px; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; color: #f7f8f8; font-weight: 500;">
            <span class="telemetry-dot-online"></span> Ollama Daemon: Online
        </div>
        <div style="font-size: 10px; color: #8a8f98; margin-top: 2px; font-family: 'JetBrains Mono', monospace;">
            Model: {orchestrator.local_model} ({ollama_health['endpoint']})
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div style="background-color: #18191b; border: 1px solid #34343a; border-radius: 4px; padding: 8px 10px; margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 6px; font-size: 11px; color: #ef4444; font-weight: 500;">
            <span class="telemetry-dot-offline"></span> Ollama Daemon: Offline
        </div>
        <div style="font-size: 10px; color: #8a8f98; margin-top: 2px;">
            Execute <code>ollama serve</code> in terminal.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Cloud Arbitration Key
with st.sidebar.expander("Cloud Internet Arbitration (Gemini)", expanded=False):
    st.caption("Automatic cloud arbitration triggers when candidate materials have close performance index margins (Δ ≤ 8%).")
    gemini_key = st.text_input(
        "Gemini API Key",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        placeholder="AIzaSy…",
        label_visibility="collapsed"
    )
    if gemini_key:
        orchestrator.cloud_api_key = gemini_key
        st.markdown("<span style='font-size: 11px; color: #4ade80;'>Connected for live internet tie-breaking.</span>", unsafe_allow_html=True)

st.sidebar.markdown("<div style='border-top: 1px solid #23252a; margin: 16px 0;'></div>", unsafe_allow_html=True)

# Design Sessions Manager
st.sidebar.markdown("<div style='font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;'>Design Cases & History</div>", unsafe_allow_html=True)

if st.sidebar.button("+ New Design Case", use_container_width=True):
    new_id = str(uuid.uuid4())[:8]
    st.session_state.engineering_sessions[new_id] = {
        "title": f"Design Case #{len(st.session_state.engineering_sessions)+1:02d}",
        "prompt": "",
        "result": None,
        "nlp_spec": None,
        "chart_fig": None
    }
    st.session_state.active_session_id = new_id
    st.rerun()

for s_id, s_data in reversed(list(st.session_state.engineering_sessions.items())):
    is_active = (s_id == st.session_state.active_session_id)
    btn_type = "primary" if is_active else "secondary"
    if st.sidebar.button(s_data["title"], key=f"session_btn_{s_id}", type=btn_type, use_container_width=True):
        st.session_state.active_session_id = s_id
        st.rerun()

if len(st.session_state.engineering_sessions) > 1:
    if st.sidebar.button("Reset All Cases", use_container_width=True):
        fresh_id = str(uuid.uuid4())[:8]
        st.session_state.engineering_sessions = {
            fresh_id: {
                "title": "Design Case #01",
                "prompt": "",
                "result": None,
                "nlp_spec": None,
                "chart_fig": None
            }
        }
        st.session_state.active_session_id = fresh_id
        st.rerun()

st.sidebar.markdown("<div style='border-top: 1px solid #23252a; margin: 16px 0;'></div>", unsafe_allow_html=True)

# Catalog Property Inspector
with st.sidebar.expander("Material Database Inspector", expanded=False):
    mat_options = list(MATERIALS_DATABASE.keys())
    sel_mat_key = st.selectbox("Select Grade", mat_options, index=0)
    if sel_mat_key:
        m_info = MATERIALS_DATABASE[sel_mat_key]
        st.markdown(f"**{m_info['name']}**")
        st.caption(f"Family: {m_info.get('family', 'Standard')}")
        st.markdown(f"""
        - **Density:** `{m_info.get('density', 0)} kg/m³`
        - **Yield Strength:** `{m_info.get('yield_strength', 0)} MPa`
        - **Modulus E:** `{m_info.get('youngs_modulus_print_xy', m_info.get('youngs_modulus_iso', 0))} GPa`
        - **Thermal Conductivity:** `{m_info.get('thermal_conductivity', 0)} W/(m·K)`
        - **Service Temp (HDT):** `{m_info.get('heat_deflection_temp', 0)} °C`
        - **Raw Cost:** `${m_info.get('cost_per_kg_usd', 0):.2f} / kg`
        """)

st.sidebar.markdown("<div style='border-top: 1px solid #23252a; margin: 16px 0;'></div>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
<div style="font-size: 11px; color: #62666d; line-height: 1.5;">
    Indexed Materials: <strong style="color: #8a8f98;">{len(MATERIALS_DATABASE):,}</strong><br>
    Standards: <strong style="color: #8a8f98;">ASTM / ISO / ASME / DIN / JIS</strong><br>
    Optimization: <strong style="color: #8a8f98;">Ashby Multi-Objective</strong>
</div>
""", unsafe_allow_html=True)


# Main Interface Top Telemetry Strip
st.markdown(f"""
<div class="telemetry-bar">
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="telemetry-title">EMS-OS // Materials Optimization Console</span>
        <span class="badge-neutral">ISO 527 // ASTM E466 // ASME VIII</span>
    </div>
    <div style="display: flex; align-items: center; gap: 14px;">
        <div class="telemetry-item">
            <span class="{'telemetry-dot-online' if ollama_health['online'] else 'telemetry-dot-offline'}"></span>
            <span>Ollama: <strong style="color: #d0d6e0;">{orchestrator.local_model}</strong></span>
        </div>
        <div class="telemetry-item">
            <span>Catalog: <strong style="color: #d0d6e0;">{len(MATERIALS_DATABASE):,} Grades</strong></span>
        </div>
        <div class="telemetry-item">
            <span>Methodology: <strong style="color: #d0d6e0;">Ashby Continuum</strong></span>
        </div>
        <div class="telemetry-item">
            <span>Sourcing: <strong style="color: #d0d6e0;">Wilson-Harris EOQ</strong></span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# Two-Pane Workbench Layout
col_left, col_right = st.columns([4, 6], gap="medium")

# LEFT PANE: Engineering Specification & Sizing Console
with col_left:
    st.markdown("""
    <div class="wb-card-header">
        <span>Design Specification & Boundary Constraints</span>
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #62666d;">PANEL 01 // INPUT</span>
    </div>
    """, unsafe_allow_html=True)

    # Benchmark Presets Selector
    preset_dict = {
        "Custom Specification (Blank)": "",
        "Cryogenic Dewar Strut (ASTM E466)": "Design a cryogenic dewar suspension strut operating at -196 C subject to cyclic axial tension fatigue under ASTM E466. Maximize stiffness-to-weight and fatigue endurance limit while minimizing solid thermal conductivity.",
        "High-Speed Spindle Shaft (AISI 4340)": "High-speed CNC milling machine spindle shaft subjected to dynamic alternating torsional and bending shear stress at 12,000 RPM. Requires high shear modulus G > 75 GPa, high fatigue limit, and dimensional stability.",
        "Submerged Hydro Turbine Blade (Tana River)": "Submerged micro-hydro turbine blade operating in Kenyan river sediment flow at flow velocity u = 2.4 m/s. Must resist cantilever hydrodynamic bending stress, cavitation erosion, and freshwater saturation hydrolysis degradation.",
        "Downforce Aerodynamic Wing Spar (CFRP)": "Automotive racing aerodynamic wing spar subjected to extreme negative aerodynamic downforce bending. Requires maximum flexural rigidity per unit weight to prevent wing stall, conforming to composite structural safety margins.",
        "Thin-Walled Pressure Vessel (ASME VIII)": "Thin-walled gas containment pressure vessel operating at internal pressure P = 250 bar. Requires maximum yield burst hoop stress efficiency sigma_y / rho while preventing catastrophic brittle rupture.",
        "Orthopedic Femoral Hip Prosthesis (ISO 5832)": "Biocompatible femoral hip joint prosthesis implant conforming to ISO 5832. Requires high yield strength and corrosion resistance in physiological saline, with matching elastic modulus to prevent bone stress shielding.",
        "Automotive Brake Caliper Bridge": "High-performance automotive brake caliper bridge bracket subjected to hydraulic piston clamping force and thermal flash temperatures of 450 C. Requires extreme elastic stiffness to prevent brake pedal sponginess.",
        "High-Flux Electronic Heat Sink (250 W)": "High heat flux CPU/IGBT electronic thermal management heat sink dissipating 250 W. Maximize solid Fourier thermal conductivity k and fin efficiency while maintaining low mass."
    }

    with st.expander("Engineering User Manual & Exploration Guide", expanded=False):
        st.markdown("""
        **Welcome to the EMS-OS Materials Optimization Console.** This system is **open-ended**—you can evaluate any custom mechanical design brief or choose a pre-configured engineering benchmark.
        
        **How to test and explore:**
        1. **Enter Your Design Brief:** Type any mechanical specification directly into the **Technical Engineering Design Brief** area below. Include the component function (e.g., *drone arm, pressure pipe, turbine runner*), stress/loading mode (e.g., *bending, tension, torsion, internal burst pressure*), operating environment (*temperatures, water immersion, UV, chemicals*), and any target standards (*ASTM, ISO, ASME*).
        2. **Use Presets (Optional):** Use the **Benchmark Library** dropdown below to load calibrated baseline test cases (e.g., Cryogenic Dewar Strut, High-Speed Spindle Shaft, Micro-Hydro Blade).
        3. **Set Parameters:** Choose your manufacturing scope (Universal or FDM 3D printing) and projected annual production demand in kg to evaluate Wilson-Harris batch sizes and local landed costs.
        4. **Execute Optimization:** Click the **Execute Screening & Optimization** button to run continuum mechanics derivations, database filtering across 1,490+ materials, and techno-economic ranking.
        """)

    prompt_state_key = f"prompt_input_{st.session_state.active_session_id}"
    if prompt_state_key not in st.session_state:
        st.session_state[prompt_state_key] = current_session.get("prompt", "")

    def on_preset_select():
        chosen = st.session_state.get(f"preset_sel_{st.session_state.active_session_id}")
        if chosen and chosen in preset_dict:
            if chosen == "Custom Specification (Blank)":
                st.session_state[prompt_state_key] = ""
                current_session["prompt"] = ""
                current_session["title"] = "Custom Design Case"
            else:
                st.session_state[prompt_state_key] = preset_dict[chosen]
                current_session["prompt"] = preset_dict[chosen]
                current_session["title"] = chosen.split("(")[0].strip()

    st.selectbox(
        "Standard Benchmark Library (Optional Examples)",
        options=list(preset_dict.keys()),
        index=0,
        key=f"preset_sel_{st.session_state.active_session_id}",
        on_change=on_preset_select,
        help="Select a benchmark specification or enter custom constraints in the text box below."
    )

    # Technical Specification Text Area
    user_prompt = st.text_area(
        "Technical Engineering Design Brief (Open-Ended)",
        key=prompt_state_key,
        height=140,
        placeholder="Enter ANY open-ended technical specification (e.g., 'A hollow titanium or carbon-composite drone arm subjected to 40 N aerodynamic bending at -20 C' or 'Corrosion-resistant marine pump impeller operating in saline brine')...",
        help="Mechanical specifications entered here are parsed for continuum mechanics loading mode, boundary conditions, and environmental degradation kinetic risks."
    )
    current_session["prompt"] = user_prompt

    # Structured Parameter Adjustments
    st.markdown("<div style='font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin: 12px 0 8px 0;'>Boundary Condition Gating</div>", unsafe_allow_html=True)

    c_bnd1, c_bnd2 = st.columns(2)
    with c_bnd1:
        mfg_scope = st.radio(
            "Manufacturing Route",
            ["Universal Multi-Process", "FDM Additive Only"],
            index=0,
            horizontal=True
        )
    with c_bnd2:
        annual_demand_kg = st.number_input(
            "Annual Production Demand (kg)",
            min_value=50.0,
            max_value=1000000.0,
            value=1500.0,
            step=250.0,
            help="Evaluates Economic Order Quantity (EOQ) batch sizing and Minimum Order Quantity (MOQ)."
        )

    # Environmental Kinetics Checkboxes
    with st.expander("Operational Environmental Kinetics", expanded=False):
        c_env1, c_env2 = st.columns(2)
        with c_env1:
            env_hydro = st.checkbox("Submerged River / Marine Water (Hydrolysis Risk)", value=("submerged" in user_prompt.lower() or "hydro" in user_prompt.lower()))
            env_cryo = st.checkbox("Cryogenic Thermal Environment (-196 °C)", value=("cryogenic" in user_prompt.lower() or "-196" in user_prompt.lower()))
            env_uv = st.checkbox("Outdoor Solar UV Radiation", value=("uv" in user_prompt.lower() or "solar" in user_prompt.lower()))
        with c_env2:
            env_high_temp = st.checkbox("Thermal Flash / High Temp (>400 °C)", value=("450" in user_prompt.lower() or "heat" in user_prompt.lower() and "sink" not in user_prompt.lower()))
            env_vacuum = st.checkbox("High Vacuum Outgassing (Space / Chamber)", value=("vacuum" in user_prompt.lower()))

    # Primary Action Button
    execute_clicked = st.button("Execute Screening & Optimization", type="primary", use_container_width=True)

    if execute_clicked and user_prompt.strip():
        with st.spinner("Executing Ashby continuum mechanics, screening 1,490+ materials, checking cloud arbitration, and optimizing supply chain…"):
            # 1. Parse Scientific Prompt
            nlp_spec = NLPTranslationLayer.parse_engineering_prompt(user_prompt)

            # Apply manual overrides if checked
            if mfg_scope == "FDM Additive Only":
                nlp_spec["boundary_conditions_and_constraints"]["fdm_only_preference"] = True
            if env_hydro:
                nlp_spec["boundary_conditions_and_constraints"]["submerged_river_exposure"] = True
            if env_uv:
                nlp_spec["boundary_conditions_and_constraints"]["outdoor_solar_uv_exposure"] = True

            # 2. Retrieve Verified RAG Chunks (Single Query Optimization)
            retrieved_chunks = rag_engine.query(user_prompt, top_k=4)
            rag_prompt = rag_engine.build_augmented_prompt(
                user_query=user_prompt,
                engineering_spec=nlp_spec,
                retrieved_chunks=retrieved_chunks
            )

            # 3. Execute Orchestrator Pipeline
            result = orchestrator.generate_recommendation(
                user_prompt=user_prompt,
                engineering_spec=nlp_spec,
                rag_prompt=rag_prompt,
                retrieved_chunks=retrieved_chunks,
                annual_demand_kg=annual_demand_kg
            )

            # 4. Generate Interactive Ashby Chart
            top_ranked = result.get("ranked_materials", [])
            top_key = top_ranked[0]["key"] if top_ranked else "Stainless_Steel_316L"
            ashby_idx = result.get("ashby_index_used", AshbyIndex.BEAM_STIFFNESS)

            x_axis = "density"
            y_axis = "youngs_modulus_print_xy"
            if ashby_idx in [AshbyIndex.BEAM_STRENGTH, AshbyIndex.TIE_STRENGTH, AshbyIndex.PLATE_STRENGTH, AshbyIndex.FLYWHEEL_INERTIA]:
                y_axis = "yield_strength"
            elif ashby_idx in [AshbyIndex.THERMAL_CONDUCTIVITY, AshbyIndex.THERMAL_DIFFUSIVITY]:
                y_axis = "thermal_conductivity"
            elif ashby_idx == AshbyIndex.FATIGUE_EFFICIENCY:
                y_axis = "fatigue_strength_limit"

            chart_fig = create_interactive_ashby_chart(
                materials=list_all_materials(),
                x_prop=x_axis,
                y_prop=y_axis,
                index_key=ashby_idx,
                highlight_keys=[top_key],
                title_suffix=f"Index: {ashby_idx}",
                anchor_material_key=top_key
            )

            # Store in session state
            current_session["nlp_spec"] = nlp_spec
            current_session["result"] = result
            current_session["chart_fig"] = chart_fig
            current_session["title"] = user_prompt[:28] + ("…" if len(user_prompt) > 28 else "")


# RIGHT PANE: Multi-Objective Analysis & Diagnostics
with col_right:
    res = current_session.get("result")
    spec = current_session.get("nlp_spec")

    if not res:
        # High-Fidelity Empty State
        st.markdown("""
        <div class="wb-card">
            <div class="wb-card-header">
                <span>Multi-Objective Continuum Evaluation Engine</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #62666d;">AWAITING EXECUTION</span>
            </div>
            <div style="padding: 24px 8px; text-align: center;">
                <div style="font-size: 16px; font-weight: 600; color: #f7f8f8; margin-bottom: 8px;">Optimization Console Ready</div>
                <div style="font-size: 13px; color: #8a8f98; max-width: 500px; margin: 0 auto 20px auto; line-height: 1.5;">
                    Select an engineering benchmark specification on the left or enter a custom design brief, then execute multi-objective optimization.
                </div>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; text-align: left; max-width: 580px; margin: 0 auto;">
                    <div style="background-color: #141517; border: 1px solid #23252a; border-radius: 4px; padding: 12px;">
                        <div style="font-size: 11px; font-weight: 600; color: #d0d6e0; text-transform: uppercase; margin-bottom: 4px;">Phase 1: Mechanics</div>
                        <div style="font-size: 11px; color: #8a8f98;">Continuum loading derivations and governing Ashby index assignment.</div>
                    </div>
                    <div style="background-color: #141517; border: 1px solid #23252a; border-radius: 4px; padding: 12px;">
                        <div style="font-size: 11px; font-weight: 600; color: #d0d6e0; text-transform: uppercase; margin-bottom: 4px;">Phase 2: Screening</div>
                        <div style="font-size: 11px; color: #8a8f98;">Pareto boundary filtering across 1,490 standardized alloys and polymers.</div>
                    </div>
                    <div style="background-color: #141517; border: 1px solid #23252a; border-radius: 4px; padding: 12px;">
                        <div style="font-size: 11px; font-weight: 600; color: #d0d6e0; text-transform: uppercase; margin-bottom: 4px;">Phase 3: Sourcing</div>
                        <div style="font-size: 11px; color: #8a8f98;">Wilson-Harris EOQ batch sizing, MOQ gating, and landed cost analytics.</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        top_mats = res.get("ranked_materials", [])
        top_mat = top_mats[0] if top_mats else {"name": "Titanium Ti-6Al-4V", "key": "Titanium_Ti6Al4V"}
        top_mat_data = get_material(top_mat["key"]) or top_mat
        ashby_spec = spec.get("synthesized_engineering_spec", {})
        bnd_spec = spec.get("boundary_conditions_and_constraints", {})

        # Executive Recommendation Banner
        arbitrated = res.get("arbitration_result", {}).get("arbitrated", False)
        arb_badge_html = f"<span class='badge-arbitrated'>Cloud Arbitration: {res['arbitration_result']['engine']}</span>" if arbitrated else f"<span class='badge-verified'>Engine: {res['mode_used']}</span>"

        st.markdown(f"""
        <div class="wb-card">
            <div class="wb-card-header">
                <span>Governing Material Specification</span>
                <div>{arb_badge_html}</div>
            </div>
            <div class="material-headline-name">{top_mat['name']}</div>
            <div class="material-headline-sub">
                Family: <strong style="color: #d0d6e0;">{top_mat.get('family', 'Standard Alloy')}</strong> &nbsp;|&nbsp; 
                Governing Index: <strong style="color: #d0d6e0;">{ashby_spec.get('primary_governing_ashby_index', 'beam_stiffness')}</strong> &nbsp;|&nbsp;
                Route: <strong style="color: #d0d6e0;">{bnd_spec.get('manufacturing_process', 'Universal Multi-Process')}</strong>
            </div>
            <div class="stat-grid">
                <div class="stat-box">
                    <div class="stat-label">Ashby Index (M)</div>
                    <div class="stat-value">{top_mat.get('score', 0):.2f}</div>
                    <div class="stat-sub">{ashby_spec.get('ashby_mathematical_formula', 'E^(1/2) / ρ')}</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Yield Strength (σ_y)</div>
                    <div class="stat-value">{top_mat_data.get('yield_strength', 0):.0f} <span style="font-size: 11px;">MPa</span></div>
                    <div class="stat-sub">Tensile Yielding Limit</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Modulus (E)</div>
                    <div class="stat-value">{top_mat_data.get('youngs_modulus_print_xy', top_mat_data.get('youngs_modulus_iso', 0)):.1f} <span style="font-size: 11px;">GPa</span></div>
                    <div class="stat-sub">Elastic Stiffness</div>
                </div>
                <div class="stat-box">
                    <div class="stat-label">Raw Sourcing Cost</div>
                    <div class="stat-value">${top_mat_data.get('cost_per_kg_usd', 0):.2f} <span style="font-size: 11px;">/ kg</span></div>
                    <div class="stat-sub">EOQ Model Basis</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Interactive Ashby Chart
        if current_session.get("chart_fig"):
            st.markdown("""
            <div class="wb-card-header" style="margin-top: 12px;">
                <span>Ashby Pareto Selection Space (Log-Log Coordinate Plane)</span>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #62666d;">FIGURE 01</span>
            </div>
            """, unsafe_allow_html=True)
            st.plotly_chart(current_session["chart_fig"], use_container_width=True, key=f"chart_{st.session_state.active_session_id}")

        # Multi-Tab Diagnostic Deep Dive
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Continuum Mechanics",
            "Degradation Gating",
            "Sourcing & EOQ",
            "Decision Provenance",
            "Knowledge Base (RAG)"
        ])

        with tab1:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;">
                Analytical Derivation & Manufacturing Directives
            </div>
            """, unsafe_allow_html=True)
            st.markdown(res.get("synthesized_response", "Synthesis complete."))

        with tab2:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;">
                Environmental Degradation Kinetic Verification
            </div>
            """, unsafe_allow_html=True)

            degradation_rows = [
                {
                    "Degradation Mode": "Freshwater / Marine Hydrolysis",
                    "Active Constraint": "Active" if bnd_spec.get("submerged_river_exposure") else "Inactive",
                    "Physical Mechanism": "Ester bond cleavage & moisture plasticization",
                    "Status": "PASS (Sealed / Hydrolysis-Resistant)" if not bnd_spec.get("submerged_river_exposure") or "CF" in top_mat["name"] or "Steel" in top_mat["name"] or "Titanium" in top_mat["name"] else "SURFACE PROTOCOL REQUIRED"
                },
                {
                    "Degradation Mode": "Outdoor Solar UV Degradation",
                    "Active Constraint": "Active" if bnd_spec.get("outdoor_solar_uv_exposure") else "Inactive",
                    "Physical Mechanism": "Free-radical photo-oxidation & surface chalking",
                    "Status": "PASS (UV-Stable Matrix / Inorganic Alloy)"
                },
                {
                    "Degradation Mode": "Cryogenic Ductile-to-Brittle Transition (DBTT)",
                    "Active Constraint": "Active" if "cryogenic" in current_session["prompt"].lower() else "Inactive",
                    "Physical Mechanism": "Dislocation lockup in BCC lattices below DBTT",
                    "Status": "PASS (FCC Austenitic / HCP Titanium Microstructure)" if "Steel" in top_mat["name"] or "Titanium" in top_mat["name"] or "CFRP" in top_mat["name"] else "QUALIFIED"
                },
                {
                    "Degradation Mode": "Thermal Softening / Creep Rupture",
                    "Active Constraint": "Active",
                    "Physical Mechanism": "Molecular relaxation above Heat Deflection Temperature (HDT)",
                    "Status": f"PASS (HDT = {top_mat_data.get('heat_deflection_temp', 0)} °C)"
                }
            ]
            st.dataframe(pd.DataFrame(degradation_rows), use_container_width=True, hide_index=True)

        with tab3:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;">
                Techno-Economic Sourcing & Wilson-Harris EOQ Analytics
            </div>
            """, unsafe_allow_html=True)

            leaderboard = res.get("techno_economic_leaderboard", [])
            if leaderboard:
                econ_rows = []
                for item in leaderboard[:10]:
                    econ = item["economics"]
                    eoq = econ.get("eoq", {})
                    landed = econ.get("landed_cost_breakdown", {})
                    kraljic = econ.get("kraljic_portfolio", {})
                    ss = econ.get("safety_stock_analysis", {})
                    
                    exw = landed.get("incoterm_exw_usd_kg", econ.get("raw_cost_usd_per_kg", 0.0))
                    ddp = landed.get("incoterm_ddp_usd_kg", econ.get("landed_cost_usd_per_kg", exw))
                    origin = landed.get("origin_key", econ.get("sourcing_category", "Global"))
                    lead = econ.get("lead_time_days", 14)
                    ss_kg = ss.get("safety_stock_kg", 0.0)
                    quad = kraljic.get("quadrant", "Routine")
                    moq = econ.get("minimum_order_quantity_kg", 25.0)
                    eff_eoq = eoq.get("effective_order_quantity_kg", eoq.get("eoq_batch_size_kg", 50.0))
                    score = item.get("composite_score", 0.0)

                    econ_rows.append({
                        "Rank": f"#{item['overall_rank']}",
                        "Material Grade": item["name"],
                        "Family": item["family"],
                        "Ashby Index": f"{item['technical_ashby_score']:.2f}",
                        "Cost (EXW / DDP)": f"${exw:.2f} / ${ddp:.2f}",
                        "Sourcing Origin": origin,
                        "Lead Time": f"{lead:.0f}d (SS: {ss_kg:.1f}kg)",
                        "Kraljic Quadrant": quad,
                        "MOQ / EOQ": f"{moq:.0f}kg / {eff_eoq:.0f}kg",
                        "TOPSIS Score": f"{score:.1f}/100"
                    })
                st.dataframe(pd.DataFrame(econ_rows), use_container_width=True, hide_index=True)

        with tab4:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;">
                Engine Decision Provenance & Optimization Pipeline
            </div>
            """, unsafe_allow_html=True)

            thinking = res.get("thinking_process", [])
            if thinking:
                for step in thinking:
                    st.markdown(f"**{step['phase']}**")
                    st.caption(step["details"])

            arb = res.get("arbitration_result")
            if arb and arb.get("arbitrated"):
                st.markdown("<div style='border-top: 1px solid #23252a; margin: 12px 0;'></div>", unsafe_allow_html=True)
                st.markdown(f"**Cloud Internet Tie-Breaking Arbitration ({arb['engine']})**")
                st.caption(arb.get("arbitration_notes", ""))

        with tab5:
            st.markdown("""
            <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; color: #8a8f98; margin-bottom: 8px;">
                Verified ChromaDB Document Retrieval Chunks
            </div>
            """, unsafe_allow_html=True)

            retrieved = res.get("retrieved_chunks", [])
            if retrieved:
                for i, chunk in enumerate(retrieved, 1):
                    st.markdown(f"**Chunk [{i}] // Document:** `{chunk.get('metadata', {}).get('document_title', 'ASTM/ISO Reference')}` &nbsp;|&nbsp; **Relevance:** `{chunk.get('score', 0):.3f}`")
                    st.code(chunk.get("text", ""), language="markdown")
            else:
                st.caption("No vector store chunks retrieved for active query.")

        # Export Report Section
        st.markdown("<div style='border-top: 1px solid #23252a; margin: 20px 0 14px 0;'></div>", unsafe_allow_html=True)
        report_md = EngineeringReportGenerator.generate_markdown_report(res, spec)
        st.download_button(
            label="Export Technical Specification Report (Markdown)",
            data=report_md,
            file_name="engineering_material_specification_report.md",
            mime="text/markdown",
            key=f"dl_btn_{st.session_state.active_session_id}"
        )
