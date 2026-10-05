from dotenv import load_dotenv
load_dotenv()
"""
Autonomous Computational Material Selection System - Advanced Chat-Based Interface.
Grounded in Michael F. Ashby's optimization methodology, persistent ChromaDB RAG,
multi-material physics, and interactive Plotly visualization.
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
from src.report_generator import EngineeringReportGenerator

# Page Configuration
st.set_page_config(
    page_title="Material Selection System | Advanced Chat",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling for modern conversational interface
st.markdown("""
<style>
    .main-title {
        font-size: 2.0rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.1rem;
    }
    .subtitle {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 1.2rem;
    }
    .chip-btn {
        margin: 2px 4px 6px 0px;
    }
    .metric-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #3730A3;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_rag_engine():
    return RAGEngine()


rag_engine = get_rag_engine()

# Sidebar: System Settings & Ad-Hoc Ashby Explorer
st.sidebar.title(" Engineering Settings")
st.sidebar.markdown("**Autonomous Materials Selection System**")

# Dual-Mode Operational Setting
mode_selection = st.sidebar.selectbox(
    "Inference Engine:",
    [
        "Local Standalone LLM (llama.cpp / Ollama)",
        "Cloud API (OpenSystem GPT-4 / Gemini)",
        "Autonomous Offline Expert Reasoner"
    ],
    index=2
)

mode_map = {
    "Local Standalone LLM (llama.cpp / Ollama)": LLMOrchestrator.MODE_LOCAL,
    "Cloud API (OpenSystem GPT-4 / Gemini)": LLMOrchestrator.MODE_CLOUD,
    "Autonomous Offline Expert Reasoner": LLMOrchestrator.MODE_AUTONOMOUS_EXPERT
}

# Manufacturing Filter Scope
mfg_scope = st.sidebar.radio(
    "Manufacturing Scope Filter:",
    [
        "Universal (All Metals, Composites, Polymers, Ceramics)",
        "FDM 3D Printing Only"
    ],
    index=0
)
force_fdm = (mfg_scope == "FDM 3D Printing Only")

orchestrator = LLMOrchestrator(mode=mode_map[mode_selection])

st.sidebar.markdown("---")
st.sidebar.markdown("###  Ad-Hoc Ashby Plotter")
with st.sidebar.expander("Explore Property Axes & Slopes"):
    plot_x = st.selectbox("X-Axis Property:", ["density", "cost_per_kg_usd", "yield_strength"], index=0)
    plot_y = st.selectbox("Y-Axis Property:", ["youngs_modulus_print_xy", "yield_strength", "thermal_conductivity"], index=0)
    adhoc_fig = create_interactive_ashby_chart(x_prop=plot_x, y_prop=plot_y, title_suffix="Ad-Hoc Inspection")
    st.plotly_chart(adhoc_fig, use_container_width=True, key="sidebar_adhoc_ashby_chart")

st.sidebar.markdown("---")
st.sidebar.markdown("###  Chat History")
if st.sidebar.button(" New Chat", use_container_width=True):
    new_id = str(uuid.uuid4())
    st.session_state.chat_sessions[new_id] = {
        "title": f"Chat {len(st.session_state.chat_sessions)+1}",
        "messages": [
            {
                "role": "assistant",
                "content": (
                    " Hello! I am your **Autonomous Material Selection & Mechanical Engineering Consultant**.\n\n"
                    "Type your query below or click one of the quick starter chips!"
                ),
                "payload": None
            }
        ]
    }
    st.session_state.current_chat_id = new_id
    st.rerun()

st.sidebar.markdown("#### Previous Chats")
if "chat_sessions" in st.session_state:
    for chat_id, chat_data in reversed(list(st.session_state.chat_sessions.items())):
        btn_style = "primary" if chat_id == st.session_state.current_chat_id else "secondary"
        if st.sidebar.button(chat_data["title"], key=f"chat_btn_{chat_id}", type=btn_style, use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

if st.sidebar.button(" Clear All History", use_container_width=True):
    del st.session_state.chat_sessions
    st.rerun()

st.sidebar.markdown(f"**Indexed Materials:** {len(MATERIALS_DATABASE)} alloys, composites, polymers & ceramics")
st.sidebar.markdown("**RAG Vector Store:** ChromaDB Persistent Index Active")

# Main Page Header
st.markdown('<div class="main-title">Autonomous Computational Material Selection System</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Universal Mechanical Design & Ashby Optimization Consultant | Advanced Chat Interface</div>', unsafe_allow_html=True)

# Initialize Chat History
if "chat_sessions" not in st.session_state:
    initial_id = str(uuid.uuid4())
    st.session_state.chat_sessions = {
        initial_id: {
            "title": "New Chat",
            "messages": [
                {
                    "role": "assistant",
                    "content": (
                " Hello! I am your **Autonomous Material Selection & Mechanical Engineering Consultant**.\n\n"
                "I analyze non-technical requirements and translate them into rigorous **Michael Ashby performance indices**, "
                "evaluate empirical degradation (freshwater saturation, UV exposure, fatigue limits), and prescribe exact manufacturing "
                "directives across **all engineering domains**:\n"
                "-  **Aerospace & Marine:** Lightweight spars, hydrofoil turbine blades, boat hulls, rocket nozzles\n"
                "-  **Automotive & Sports:** Bicycle frames, racing chassis, crane hooks, suspension arms\n"
                "-  **Thermal Management:** CPU heat sinks, heat exchangers, thermal barriers\n"
                "-  **Biomedical & Consumer:** Orthopedic hip implants, shock-absorbing phone cases, wear-resistant gears\n\n"
                "Type your query below or click one of the quick starter chips!"
            ),
            "payload": None
        }
    ]}}
    st.session_state.current_chat_id = initial_id

# Quick Starter Chips
st.markdown("**Quick Starter Prompts:**")
c1, c2, c3, c4 = st.columns(4)
c5, c6, c7, c8 = st.columns(4)

starter_prompt = None
if c1.button(" Micro-Hydro Turbine", help="Kenyan river hydro turbine blade"):
    starter_prompt = "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight."
if c2.button(" Bicycle Frame", help="Lightweight stiff bicycle frame"):
    starter_prompt = "I want to design a lightweight and stiff bicycle frame that won't flex under heavy rider pedaling."
if c3.button(" CPU Heat Sink", help="Thermal management for high power electronics"):
    starter_prompt = "I need a material for a high-performance CPU heat sink to dissipate 200W of heat as fast as possible."
if c4.button(" Rocket Nozzle", help="Extreme thermal service at 700°C"):
    starter_prompt = "I need a material for an exhaust nozzle operating under continuous 700 C heat and mechanical stress."
if c5.button(" Hip Implant", help="Biocompatible orthopedic device"):
    starter_prompt = "I need a biocompatible material for an orthopedic hip joint implant that won't corrode in body fluids."
if c6.button(" Phone Case", help="Impact shock absorption"):
    starter_prompt = "I want to make a shock-absorbing smartphone case that will survive high drops without cracking."
if c7.button(" Crane Hook", help="Heavy-duty lifting under high load"):
    starter_prompt = "I need a material for a heavy-duty crane lifting hook that must lift 10 tons without brittle fracture."
if c8.button(" Low-Friction Gear", help="Precision wear-resistant sliding gear"):
    starter_prompt = "I need a low-friction, wear-resistant material for high-speed transmission gears with smooth sliding."

# Render Chat History
for msg_idx, msg in enumerate(st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"]):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        payload = msg.get("payload")
        if payload:
            # 1. Metric Badges
            spec = payload.get("spec", {})
            ashby = spec.get("synthesized_engineering_spec", {})
            bnd = spec.get("boundary_conditions_and_constraints", {})

            st.markdown(
                f"<span class='metric-badge'> Component: {ashby.get('component_classification', 'Mechanical')}</span>"
                f"<span class='metric-badge'> Index: {ashby.get('primary_governing_ashby_index')} ({ashby.get('ashby_mathematical_formula')})</span>"
                f"<span class='metric-badge'> Route: {bnd.get('manufacturing_process')}</span>"
                f"<span class='metric-badge'> Engine: {payload.get('mode_used')}</span>",
                unsafe_allow_html=True
            )

            # 2. Interactive Ashby Plotly Chart
            fig = payload.get("chart_figure")
            if fig:
                st.markdown("####  Interactive Ashby Property Chart")
                st.plotly_chart(fig, use_container_width=True, key=f"history_plotly_chart_{msg_idx}")

            # 3. Domain-Specific Deep Dives (Rendered conditionally when relevant!)
            hydro = payload.get("hydro_analysis")
            if hydro:
                with st.expander(" Fluid Dynamics & Hydrodynamic Roughness Deep Dive", expanded=True):
                    hc1, hc2, hc3 = st.columns(3)
                    hc1.metric("Chord Reynolds Number", f"{hydro['chord_reynolds_number']:,.0f}")
                    hc2.metric("As-Printed FDM Drag Penalty", f"-{hydro['drag_penalty_percent']}% L/D")
                    hc3.metric("Post-Coating Recovery", "0.0% Drag Penalty", delta="Full L/D Recovery")
                    st.info(
                        f"**Boundary Layer Physics:** Flow operates in {hydro['reynolds_range_match']}. Raw FDM layer lines "
                        f"(Ra ≈ {hydro['effective_roughness_ra_microns']} μm) induce premature boundary layer tripping near the leading edge. "
                        f"Mandatory UV-curable epoxy sealant (XTC-3D protocol) fills negative skewness valleys, restoring hydraulic smoothness (Ra < 1.2 μm)."
                    )

            if payload.get("is_kenya_case"):
                with st.expander(" Kenya Micro-Hydro Mini-Grid Economics Deep Dive", expanded=False):
                    kc1, kc2, kc3 = st.columns(3)
                    kc1.metric("Imported Marine Bronze Cost", "$850 - $1,200 USD")
                    kc2.metric("Decentralized 3D Print Cost", "$12.16 USD (~1,580 KES)", delta="-98.6% Cost")
                    kc3.metric("Lead Time Reduction", "10 Hours vs 6 Months", delta="-99.8% Downtime")
                    st.success(
                        "**Rural Catchment Resilience:** Micro-hydrokinetic potential across Tana River and Lake Victoria basins "
                        "exceeds 3,000 MW. Decentralized on-site 3D printing enables same-day power restoration for rural community mini-grids."
                    )

            # 4. Anti-Hallucination Verified RAG Context
            retrieved = payload.get("retrieved_chunks", [])
            if retrieved:
                with st.expander(" Verified ChromaDB RAG Knowledge Retrieval Chunks"):
                    for i, chunk in enumerate(retrieved, 1):
                        st.markdown(f"**Chunk [{i}] - Source:** `{chunk.get('metadata', {}).get('source')}` | **Similarity:** `{chunk.get('score')}`")
                        st.code(chunk.get("text", ""), language="markdown")

            # 5. Download Full Report
            report_md = payload.get("report_markdown")
            if report_md:
                st.download_button(
                    label=" Download Engineering Specification Report (Markdown)",
                    data=report_md,
                    file_name="engineering_material_specification_report.md",
                    mime="text/markdown",
                    key=f"dl_{id(msg)}"
                )

# Chat Input Handler
user_input = st.chat_input("Describe your mechanical component, environment, loads, or application...")
active_prompt = starter_prompt or user_input

if active_prompt:
    # Append User Message
    current_chat = st.session_state.chat_sessions[st.session_state.current_chat_id]
    if current_chat["title"].startswith("New Chat") or current_chat["title"].startswith("Chat "):
        current_chat["title"] = (active_prompt[:25] + "...") if len(active_prompt) > 25 else active_prompt
    current_chat["messages"].append({"role": "user", "content": active_prompt, "payload": None})
    with st.chat_message("user"):
        st.markdown(active_prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing intent, computing Ashby indices, querying ChromaDB, and synthesizing engineering decision..."):
            # 1. Parse NLP Intent
            nlp_spec = NLPTranslationLayer.parse_layman_prompt(active_prompt)

            # Override FDM filter if sidebar forced it
            if force_fdm:
                nlp_spec["boundary_conditions_and_constraints"]["fdm_only_preference"] = True

            # 2. Build RAG Augmented Prompt
            rag_prompt = rag_engine.build_augmented_prompt(
                user_query=active_prompt,
                engineering_spec=nlp_spec,
                top_k=4
            )
            retrieved_chunks = rag_engine.query(active_prompt, top_k=4)

            # 3. Orchestrate Recommendation
            result = orchestrator.generate_recommendation(
                user_prompt=active_prompt,
                engineering_spec=nlp_spec,
                rag_prompt=rag_prompt,
                retrieved_chunks=retrieved_chunks
            )

            top_ranked = result.get("ranked_materials", [])
            top_key = top_ranked[0]["key"] if top_ranked else "PETG-CF"

            # 4. Generate Dynamically Tailored Interactive Ashby Chart
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

            # Check domain flags
            is_kenya = "kenya" in active_prompt.lower() or "tana" in active_prompt.lower() or "meru" in active_prompt.lower()
            report_text = EngineeringReportGenerator.generate_markdown_report(result, nlp_spec)

            # Render in current message bubble
            st.markdown(result["synthesized_response"])

            # Metric Badges
            st.markdown(
                f"<span class='metric-badge'> Component: {nlp_spec['synthesized_engineering_spec']['component_classification']}</span>"
                f"<span class='metric-badge'> Index: {ashby_idx} ({nlp_spec['synthesized_engineering_spec']['ashby_mathematical_formula']})</span>"
                f"<span class='metric-badge'> Route: {nlp_spec['boundary_conditions_and_constraints']['manufacturing_process']}</span>"
                f"<span class='metric-badge'> Engine: {result['mode_used']}</span>",
                unsafe_allow_html=True
            )

            # Interactive Plotly Chart
            st.markdown("####  Interactive Ashby Property Chart")
            st.plotly_chart(interactive_chart, use_container_width=True, key=f'active_plotly_chart_{len(st.session_state.chat_sessions[st.session_state.current_chat_id]["messages"])}')

            # Hydrodynamic Callout if applicable
            hydro = result.get("hydrodynamic_analysis")
            if hydro:
                with st.expander(" Fluid Dynamics & Hydrodynamic Roughness Deep Dive", expanded=True):
                    hc1, hc2, hc3 = st.columns(3)
                    hc1.metric("Chord Reynolds Number", f"{hydro['chord_reynolds_number']:,.0f}")
                    hc2.metric("As-Printed FDM Drag Penalty", f"-{hydro['drag_penalty_percent']}% L/D")
                    hc3.metric("Post-Coating Recovery", "0.0% Drag Penalty", delta="Full L/D Recovery")
                    st.info(
                        f"**Boundary Layer Physics:** Flow operates in {hydro['reynolds_range_match']}. Raw FDM layer lines "
                        f"(Ra ≈ {hydro['effective_roughness_ra_microns']} μm) induce premature boundary layer tripping near the leading edge. "
                        f"Mandatory UV-curable epoxy sealant (XTC-3D protocol) fills negative skewness valleys, restoring hydraulic smoothness (Ra < 1.2 μm)."
                    )

            if is_kenya:
                with st.expander(" Kenya Micro-Hydro Mini-Grid Economics Deep Dive", expanded=False):
                    kc1, kc2, kc3 = st.columns(3)
                    kc1.metric("Imported Marine Bronze Cost", "$850 - $1,200 USD")
                    kc2.metric("Decentralized 3D Print Cost", "$12.16 USD (~1,580 KES)", delta="-98.6% Cost")
                    kc3.metric("Lead Time Reduction", "10 Hours vs 6 Months", delta="-99.8% Downtime")

            # Verified RAG Context
            if retrieved_chunks:
                with st.expander(" Verified ChromaDB RAG Knowledge Retrieval Chunks"):
                    for i, chunk in enumerate(retrieved_chunks, 1):
                        st.markdown(f"**Chunk [{i}] - Source:** `{chunk.get('metadata', {}).get('source')}` | **Similarity:** `{chunk.get('score')}`")
                        st.code(chunk.get("text", ""), language="markdown")

            # Download Report
            st.download_button(
                label=" Download Engineering Specification Report (Markdown)",
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
                    "hydro_analysis": hydro,
                    "is_kenya_case": is_kenya,
                    "retrieved_chunks": retrieved_chunks,
                    "report_markdown": report_text
                }
            })
