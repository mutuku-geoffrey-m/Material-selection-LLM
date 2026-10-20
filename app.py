from dotenv import load_dotenv
load_dotenv()
"""
Engineering Material Selection & Optimization System (EMS-OS) - Advanced Interface.
Grounded in Michael F. Ashby's optimization mechanics, 1,490+ standard materials database,
local Ollama base LLM, automatic Cloud Gemini internet arbitration, and supply chain techno-economics.
"""

import streamlit as st
import uuid
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import os
import sys

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

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
    page_title="EMS-OS | Engineering Material Selection",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for rigorous engineering interface
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
        letter-spacing: -0.5px;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.4rem;
        font-weight: 500;
    }
    .metric-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #312E81;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
        border: 1px solid #C7D2FE;
    }
    .arbitration-badge {
        display: inline-block;
        background-color: #ECFDF5;
        color: #065F46;
        padding: 5px 12px;
        border-radius: 6px;
        font-size: 0.88rem;
        font-weight: 600;
        margin-right: 8px;
        margin-bottom: 6px;
        border: 1px solid #A7F3D0;
    }
    .stDataFrame {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


rag_engine = get_rag_engine()

# Sidebar: System Settings & Sourcing Controls
st.sidebar.title("⚙️ Engineering Configuration")

# Application Theme
theme_choice = st.sidebar.radio("Theme Mode", ["Auto (System Default)", "Light Mode", "Dark Mode"])
if theme_choice != "Auto (System Default)":
    os.makedirs(".streamlit", exist_ok=True)
    theme_name = "dark" if theme_choice == "Dark Mode" else "light"
    with open(".streamlit/config.toml", "w", encoding="utf-8") as f:
        f.write(f"[theme]\nbase='{theme_name}'\n")
else:
    if os.path.exists(".streamlit/config.toml"):
        os.remove(".streamlit/config.toml")

st.sidebar.markdown("---")
st.sidebar.markdown("### 🧠 Foundation Inference Engine")

mode_selection = st.sidebar.selectbox(
    "Active Model Pipeline:",
    [
        "Local Standalone LLM (llama3.2 via Ollama) [Primary Base]",
        "Cloud API (Google Gemini / OpenAI)"
    ],
    index=0
)

mode_map = {
    "Local Standalone LLM (llama3.2 via Ollama) [Primary Base]": LLMOrchestrator.MODE_LOCAL,
    "Cloud API (Google Gemini / OpenAI)": LLMOrchestrator.MODE_CLOUD
}

orchestrator = LLMOrchestrator(mode=mode_map[mode_selection])

# Real-Time Engine Health Status Check
ollama_health = orchestrator.check_ollama_status()
if ollama_health["online"]:
    st.sidebar.success(f"● **Ollama Daemon:** Online (`{ollama_health['endpoint']}`)\nModel: `{orchestrator.local_model}`")
else:
    st.sidebar.error("● **Ollama Daemon:** Offline\nRun `ollama serve` in terminal.")

# Cloud Gemini API Key Input (for live internet tie-break arbitration)
with st.sidebar.expander("🌐 Cloud AI Arbitration (Gemini Key)", expanded=False):
    st.markdown("Automatic cloud arbitration activates when candidate materials have close performance scores ($\le 8\%$).")
    gemini_key_input = st.text_input(
        "Gemini API Key:",
        value=os.getenv("GEMINI_API_KEY", ""),
        type="password",
        help="Optional. If omitted, tie-break arbitration runs via local high-temperature LLM."
    )
    if gemini_key_input:
        orchestrator.cloud_api_key = gemini_key_input
        st.caption("✅ Live Google Gemini API connected for cloud tie-breaking arbitration.")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📦 Supply Chain & Sourcing Controls")

annual_demand_kg = st.sidebar.number_input(
    "Annual Project Demand (kg):",
    min_value=50.0,
    max_value=1000000.0,
    value=1500.0,
    step=250.0,
    help="Annual production quantity used to evaluate Economic Order Quantity (EOQ) and Minimum Order Quantity (MOQ)."
)

# Manufacturing Scope Filter
mfg_scope = st.sidebar.radio(
    "Manufacturing Scope Filter:",
    [
        "Universal (Metals, Alloys, Composites, Ceramics & Polymers)",
        "FDM Additive Manufacturing Only"
    ],
    index=0
)
force_fdm = (mfg_scope == "FDM Additive Manufacturing Only")

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Ad-Hoc Ashby Explorer")
with st.sidebar.expander("Property Coordinate Inspector"):
    plot_x = st.selectbox("X-Axis Coordinate:", ["density", "cost_per_kg_usd", "yield_strength"], index=0)
    plot_y = st.selectbox("Y-Axis Coordinate:", ["youngs_modulus_print_xy", "yield_strength", "thermal_conductivity"], index=0)
    adhoc_fig = create_interactive_ashby_chart(x_prop=plot_x, y_prop=plot_y, title_suffix="Ad-Hoc Inspection")
    st.plotly_chart(adhoc_fig, use_container_width=True, key="sidebar_adhoc_ashby_chart")

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Indexed Standard Materials:** {len(MATERIALS_DATABASE):,} grades & alloys")
st.sidebar.markdown("**Standards Covered:** ISO, ASTM, ASME, DIN, JIS, BS")

# Chat Sessions Manager
st.sidebar.markdown("### 💬 Project Sessions")
if st.sidebar.button("➕ New Engineering Session", use_container_width=True):
    new_id = str(uuid.uuid4())
    st.session_state.chat_sessions[new_id] = {
        "title": f"Session {len(st.session_state.chat_sessions)+1}",
        "messages": [
            {
                "role": "assistant",
                "content": (
                    "**Engineering Material Selection & Optimization System (EMS-OS)** initialized.\n\n"
                    "Provide your technical design specifications, functional objectives, service environment, "
                    "or governing standards (e.g. ISO 527, ASTM D638, ASME Section VIII, DIN 17100)."
                ),
                "payload": None
            }
        ]
    }
    st.session_state.current_chat_id = new_id
    st.rerun()

if "chat_sessions" in st.session_state:
    for chat_id, chat_data in reversed(list(st.session_state.chat_sessions.items())):
        btn_style = "primary" if chat_id == st.session_state.current_chat_id else "secondary"
        if st.sidebar.button(chat_data["title"], key=f"chat_btn_{chat_id}", type=btn_style, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

if st.sidebar.button("🗑️ Clear All Sessions", use_container_width=True):
    del st.session_state.chat_sessions
    st.rerun()


# Main Application Interface
st.markdown('<div class="main-title">Engineering Material Selection & Optimization System (EMS-OS)</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Objective Ashby Mechanics | Local Ollama Foundation | Cloud Gemini Arbitration | Supply Chain Sourcing Optimization</div>', unsafe_allow_html=True)

# Initialize Session State
if "chat_sessions" not in st.session_state:
    initial_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {
        initial_id: {
            "title": "New Engineering Design",
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                        "**Engineering Material Selection & Optimization System (EMS-OS)** initialized.\n\n"
                        "This computational platform evaluates structured mechanical engineering specifications against a database of **1,490+ standardized materials** (ANSI, ISO, DIN, JIS, ASTM), computing analytical **Michael F. Ashby performance indices**, environmental degradation kinetics, and multi-objective supply chain logistics (EOQ, MOQ, Lead Times).\n\n"
                        "Enter your engineering specifications below or select a standard benchmark design brief."
                    ),
                    "payload": None
                }
            ]
        }
    }
    st.session_state.current_chat_id = initial_id

# Scientific Starter Prompts for Qualified Mechanical Engineers
st.markdown("**Benchmark Engineering Specifications & Standards:**")
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)

starter_prompt = None
if c1.button("❄️ Cryogenic Strut (ASTM E466)", help="Dewar strut under axial fatigue at -196C"):
    starter_prompt = "Design a cryogenic dewar suspension strut operating at -196 C subject to cyclic axial tension fatigue under ASTM E466. Maximize stiffness-to-weight and fatigue endurance limit while minimizing solid thermal conductivity."
if c2.button("⚙️ Machine Spindle (AISI 4340)", help="High torsional rigidity spindle shaft"):
    starter_prompt = "High-speed CNC milling machine spindle shaft subjected to dynamic alternating torsional and bending shear stress at 12,000 RPM. Requires high shear modulus G > 75 GPa, high fatigue limit, and dimensional stability."
if c3.button("🌊 Hydro Turbine (Tana River)", help="Submerged micro-hydro blade"):
    starter_prompt = "Submerged micro-hydro turbine blade operating in Kenyan river sediment flow at flow velocity u = 2.4 m/s. Must resist cantilever hydrodynamic bending stress, cavitation erosion, and freshwater saturation hydrolysis degradation."
if c4.button("🏎️ Downforce Spar (CFRP)", help="Aerodynamic racing wing spar"):
    starter_prompt = "Automotive racing aerodynamic wing spar subjected to extreme negative aerodynamic downforce bending. Requires maximum flexural rigidity per unit weight to prevent wing stall, conforming to composite structural safety margins."
if c5.button("🛢️ Pressure Vessel (ASME VIII)", help="Thin-walled gas containment shell"):
    starter_prompt = "Thin-walled gas containment pressure vessel operating at internal pressure P = 250 bar. Requires maximum yield burst hoop stress efficiency sigma_y / rho while preventing catastrophic brittle rupture."
if c6.button("🦴 Orthopedic Stem (ISO 5832)", help="Biocompatible femoral prosthesis"):
    starter_prompt = "Biocompatible femoral hip joint prosthesis implant conforming to ISO 5832. Requires high yield strength and corrosion resistance in physiological saline, with matching elastic modulus to prevent bone stress shielding."
if c7.button("🛑 Brake Caliper Bridge", help="Stiff bracket resisting clamping deflection"):
    starter_prompt = "High-performance automotive brake caliper bridge bracket subjected to hydraulic piston clamping force and thermal flash temperatures of 450 C. Requires extreme elastic stiffness to prevent brake pedal sponginess."
if c8.button("🔥 Heat Sink (Fourier k)", help="Electronic thermal management 250W"):
    starter_prompt = "High heat flux CPU/IGBT electronic thermal management heat sink dissipating 250 W. Maximize solid Fourier thermal conductivity k and fin efficiency while maintaining low mass."

# Render Chat History
for msg_idx, msg in enumerate(st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        payload = msg.get("payload")
        if payload:
            spec = payload.get("spec", {})
            ashby = spec.get("synthesized_engineering_spec", {})
            bnd = spec.get("boundary_conditions_and_constraints", {})

            # Metric Badges
            badge_html = (
                f"<span class='metric-badge'>📌 Component: {ashby.get('component_classification', 'Mechanical')}</span>"
                f"<span class='metric-badge'>📐 Index: {ashby.get('primary_governing_ashby_index')} ({ashby.get('ashby_mathematical_formula')})</span>"
                f"<span class='metric-badge'>🏭 Route: {bnd.get('manufacturing_process')}</span>"
                f"<span class='metric-badge'>💻 Base Engine: {payload.get('mode_used')}</span>"
            )
            if payload.get("arbitration_result") and payload.get("arbitration_result").get("arbitrated"):
                badge_html += f"<span class='arbitration-badge'>🌐 Cloud Arbitration: {payload['arbitration_result']['engine']}</span>"
            st.markdown(badge_html, unsafe_allow_html=True)

            # Engine Thinking Process Expander
            thinking = payload.get("thinking_process", [])
            if thinking:
                with st.expander("🧠 Engine Thinking Process & Optimization Pipeline", expanded=False):
                    for step in thinking:
                        st.markdown(f"**{step['phase']}**")
                        st.caption(step["details"])

            # Interactive Plotly Chart
            fig = payload.get("chart_figure")
            if fig:
                st.markdown("#### 📈 Interactive Ashby Selection Chart")
                st.plotly_chart(fig, use_container_width=True, key=f"hist_fig_{msg_idx}")

            # Techno-Economic Leaderboard Table
            leaderboard = payload.get("techno_economic_leaderboard")
            if leaderboard:
                with st.expander("📦 Techno-Economic, Availability & Sourcing Leaderboard (EOQ & MOQ)", expanded=True):
                    df_econ = pd.DataFrame([
                        {
                            "Rank": item["overall_rank"],
                            "Material": item["name"],
                            "Family": item["family"],
                            "Ashby Score": f"{item['technical_ashby_score']:.2f}",
                            "Cost ($/kg)": f"${item['economics']['raw_cost_usd_per_kg']:.2f}",
                            "Sourcing": item['economics']['sourcing_category'],
                            "Lead Time": f"{item['economics']['lead_time_days']} days",
                            "MOQ (kg)": f"{item['economics']['minimum_order_quantity_kg']:.0f}",
                            "EOQ Batch (kg)": f"{item['economics']['eoq']['eoq_batch_size_kg']:.0f}",
                            "Composite Score": f"{item['composite_score']:.1f}/100"
                        }
                        for item in leaderboard[:6]
                    ])
                    st.dataframe(df_econ, use_container_width=True, hide_index=True)

            # Verified RAG Context Expander
            retrieved = payload.get("retrieved_chunks", [])
            if retrieved:
                with st.expander("📚 Verified ChromaDB Knowledge Retrieval Chunks"):
                    for i, chunk in enumerate(retrieved, 1):
                        st.markdown(f"**Chunk [{i}] - Document:** `{chunk.get('metadata', {}).get('document_title')}` | **Similarity:** `{chunk.get('score'):.3f}`")
                        st.code(chunk.get("text", ""), language="markdown")

            # Download Report Button
            report_md = payload.get("report_markdown")
            if report_md:
                st.download_button(
                    label="📥 Download Engineering Specification Report (Markdown)",
                    data=report_md,
                    file_name="engineering_material_specification_report.md",
                    mime="text/markdown",
                    key=f"dl_{msg_idx}"
                )

# User Chat Input
user_input = st.chat_input("Enter technical specifications, loading constraints, operating environment, or governing standards...")
active_prompt = starter_prompt or user_input

if active_prompt:
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    if current_chat["title"].startswith("New Engineering") or current_chat["title"].startswith("Session "):
        current_chat["title"] = (active_prompt[:30] + "...") if len(active_prompt) > 30 else active_prompt
    current_chat["messages"].append({"role": "user", "content": active_prompt, "payload": None})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Executing Ashby mechanics, screening 1,490+ materials, checking cloud arbitration, and optimizing supply chain..."):
            # 1. Parse Scientific Engineering Prompt
            nlp_spec = NLPTranslationLayer.parse_engineering_prompt(active_prompt)
            if force_fdm:
                nlp_spec["boundary_conditions_and_constraints"]["fdm_only_preference"] = True

            # 2. Build RAG Augmented Prompt
            rag_prompt = rag_engine.build_augmented_prompt(
                user_query=active_prompt,
                engineering_spec=nlp_spec,
                top_k=4
            )
            retrieved_chunks = rag_engine.query(active_prompt, top_k=4)

            # 3. Execute Orchestration Pipeline
            result = orchestrator.generate_recommendation(
                user_prompt=active_prompt,
                engineering_spec=nlp_spec,
                rag_prompt=rag_prompt,
                retrieved_chunks=retrieved_chunks,
                annual_demand_kg=annual_demand_kg
            )

            top_ranked = result.get("ranked_materials", [])
            top_key = top_ranked[0]["key"] if top_ranked else "Stainless_Steel_316L"

            # 4. Generate Interactive Ashby Plotly Chart
            ashby_idx = result.get("ashby_index_used", AshbyIndex.BEAM_STIFFNESS)
            x_axis = "density"
            y_axis = "youngs_modulus_print_xy"

            if ashby_idx in [AshbyIndex.BEAM_STRENGTH, AshbyIndex.TIE_STRENGTH, AshbyIndex.PLATE_STRENGTH, AshbyIndex.FLYWHEEL_INERTIA]:
                y_axis = "yield_strength"
            elif ashby_idx in [AshbyIndex.THERMAL_CONDUCTIVITY, AshbyIndex.THERMAL_DIFFUSIVITY]:
                y_axis = "thermal_conductivity"
            elif ashby_idx == AshbyIndex.FATIGUE_EFFICIENCY:
                y_axis = "fatigue_strength_limit"

            interactive_chart = create_interactive_ashby_chart(
                materials=list_all_materials(),
                x_prop=x_axis,
                y_prop=y_axis,
                index_key=ashby_idx,
                highlight_keys=[top_key],
                title_suffix=f"Governing: {ashby_idx}",
                anchor_material_key=top_key
            )

            report_text = EngineeringReportGenerator.generate_markdown_report(result, nlp_spec)

            # Render Synthesized Output
            st.markdown(result["synthesized_response"])

            # Metric Badges
            badge_html = (
                f"<span class='metric-badge'>📌 Component: {nlp_spec['synthesized_engineering_spec']['component_classification']}</span>"
                f"<span class='metric-badge'>📐 Index: {ashby_idx} ({nlp_spec['synthesized_engineering_spec']['ashby_mathematical_formula']})</span>"
                f"<span class='metric-badge'>🏭 Route: {nlp_spec['boundary_conditions_and_constraints']['manufacturing_process']}</span>"
                f"<span class='metric-badge'>💻 Base Engine: {result['mode_used']}</span>"
            )
            if result.get("arbitration_result") and result.get("arbitration_result").get("arbitrated"):
                badge_html += f"<span class='arbitration-badge'>🌐 Cloud Arbitration: {result['arbitration_result']['engine']}</span>"
            st.markdown(badge_html, unsafe_allow_html=True)

            # Engine Thinking Process Expander
            thinking = result.get("thinking_process", [])
            if thinking:
                with st.expander("🧠 Engine Thinking Process & Optimization Pipeline", expanded=True):
                    for step in thinking:
                        st.markdown(f"**{step['phase']}**")
                        st.caption(step["details"])

            # Interactive Plotly Chart
            st.markdown("#### 📈 Interactive Ashby Selection Chart")
            st.plotly_chart(interactive_chart, use_container_width=True, key=f"active_fig_{len(st.session_state.chat_sessions[st.session_state.current_chat_id]['messages'])}")

            # Techno-Economic Leaderboard Table
            leaderboard = result.get("techno_economic_leaderboard")
            if leaderboard:
                with st.expander("📦 Techno-Economic, Availability & Sourcing Leaderboard (EOQ & MOQ)", expanded=True):
                    df_econ = pd.DataFrame([
                        {
                            "Rank": item["overall_rank"],
                            "Material": item["name"],
                            "Family": item["family"],
                            "Ashby Score": f"{item['technical_ashby_score']:.2f}",
                            "Cost ($/kg)": f"${item['economics']['raw_cost_usd_per_kg']:.2f}",
                            "Sourcing": item['economics']['sourcing_category'],
                            "Lead Time": f"{item['economics']['lead_time_days']} days",
                            "MOQ (kg)": f"{item['economics']['minimum_order_quantity_kg']:.0f}",
                            "EOQ Batch (kg)": f"{item['economics']['eoq']['eoq_batch_size_kg']:.0f}",
                            "Composite Score": f"{item['composite_score']:.1f}/100"
                        }
                        for item in leaderboard[:6]
                    ])
                    st.dataframe(df_econ, use_container_width=True, hide_index=True)

            # Verified RAG Context
            if retrieved_chunks:
                with st.expander("📚 Verified ChromaDB Knowledge Retrieval Chunks"):
                    for i, chunk in enumerate(retrieved_chunks, 1):
                        st.markdown(f"**Chunk [{i}] - Document:** `{chunk.get('metadata', {}).get('document_title')}` | **Similarity:** `{chunk.get('score'):.3f}`")
                        st.code(chunk.get("text", ""), language="markdown")

            # Download Report Button
            st.download_button(
                label="📥 Download Engineering Specification Report (Markdown)",
                data=report_text,
                file_name="engineering_material_specification_report.md",
                mime="text/markdown"
            )

            # Save to Session State
            st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"].append({
                "role": "assistant",
                "content": result["synthesized_response"],
                "payload": {
                    "spec": nlp_spec,
                    "mode_used": result["mode_used"],
                    "chart_figure": interactive_chart,
                    "thinking_process": thinking,
                    "arbitration_result": result.get("arbitration_result"),
                    "techno_economic_leaderboard": leaderboard,
                    "retrieved_chunks": retrieved_chunks,
                    "report_markdown": report_text
                }
            })
