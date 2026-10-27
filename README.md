# EMS-OS: Engineering Material Selection & Optimization System
### Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection

[![Project Code](https://img.shields.io/badge/Project%20Code-EKM%2F1%2F2026-blue.svg)](#)
[![Institution](https://img.shields.io/badge/Institution-University%20of%20Nairobi-darkblue.svg)](#)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Local LLM](https://img.shields.io/badge/Local%20LLM-Ollama%20(llama3.2)-black.svg)](https://ollama.com/)
[![License](https://img.shields.io/badge/License-Academic%20Research-green.svg)](#)

---

## Academic Project Information

- **Project Code:** EKM/1/2026
- **Course:** FMM3 561 Engineering Project (Final Year Capstone)
- **Department:** Department of Mechanical and Manufacturing Engineering
- **Faculty:** Faculty of Engineering, University of Nairobi
- **Authors:**
  - **Enock Mamai** (Registration No.: `F18/2117/2020`)
  - **Mutuku Geoffrey Mulu** (Registration No.: `F18/144332/2022`)
- **Project Supervisor:** **Mr. Enoch K. Musyoka** (*Lecturer, Department of Mechanical and Manufacturing Engineering*)

---

## Executive Summary

Selecting optimal engineering materials from a commercial universe exceeding 100,000 distinct alloys, polymers, ceramics, and composites is among the most consequential phases of mechanical product development. Inappropriate material selection precipitates structural fracture, fatigue failure, galvanic corrosion, or unsustainable procurement costs.

Generic Large Language Models (such as GPT-4 or standard LLaMA) deployed for engineering design suffer from severe limitations:
1. **Physical Hallucinations:** Inventing non-existent mechanical property values ($\sigma_y$, $E$, $\rho$) through probabilistic token sampling.
2. **Physical Law Violations:** Confusing linear scaling with non-linear beam/plate bending exponents (e.g., recommending pure stiffness over strength for flexural members).
3. **Supply Chain Blindness:** Disregarding real-world procurement logistics, tariffs, lead-time variance, minimum order quantities (MOQs), and geographic availability.

**EMS-OS** resolves this dilemma through a **decoupled, physics-grounded architecture**. Natural language engineering design intent is translated into continuum mechanics boundary conditions, while all property evaluations and multi-criteria trade-offs are executed by deterministic mathematical solvers. Qualitative microstructural synthesis is handled by a local edge model (**`llama3.2`** via Ollama) protected by an automated circuit breaker and cloud arbitration fallback.

---

## Key System Architecture & Engineering Modules

```
                             [Natural Language Prompt]
                                        │
                                        ▼
                      [Scientific NLP Translation Layer]
                      (Stress States & Boundary Conditions)
                                        │
                                        ▼
                         [Boolean Physical Gating]
                     (Cryogenic DBTT, Magnetics, Optics)
                                        │
                                        ▼
                      [Deterministic Ashby Index Engine]
                      (1,490+ Standard Materials Catalog)
                                        │
                                        ▼
                       [Techno-Economic Sourcing Engine]
                      (Incoterms 2020 DDP, Mombasa Port,
                       EOQ, Safety Stock, Kraljic Matrix)
                                        │
                                        ▼
                    [Vector-Normalized TOPSIS Optimization]
                     (Compensable Multi-Objective Ranking)
                                        │
                                        ▼
                             [Contender Score Delta]
                              ├── Delta > 8.0% ──► [Local Ollama (llama3.2)]
                              └── Delta ≤ 8.0% ──► [Google Gemini Cloud Arbitration]
                                        │
                                        ▼
                      [Verified Engineering Dossier & Leaderboard]
```

### 1. Scientific NLP Translation Layer
Extracts functional classifications, primary stress states, loading geometries, service temperature ranges, chemical/environmental exposures, and target standards (ANSI, ISO, DIN, JIS, ASTM) from unstructured prompts.

### 2. Boolean Physical Gating Filter
Applies strict non-compensable gates before index ranking:
- Optical transmission ($>85\%$ for transparent bulkheads/shields).
- Cryogenic ductile-to-brittle transition temperature bounds ($T_H < 0.55$).
- Non-magnetic susceptibility ($\chi_m \approx 0$ for high-field MRI components).
- Chemical inertness (hydrocarbon and industrial cutting fluid compatibility).

### 3. Deterministic Continuum Mechanics Ashby Engine
Evaluates 1,490 unit-normalized materials against 10 governing Ashby performance index derivations:
- $M_1 = E / \rho$ (Axial tie stiffness)
- $M_2 = \sigma_y / \rho$ (Tensile tie strength & thin-walled pressure vessels)
- $M_3 = E^{1/2} / \rho$ (Beam flexural bending stiffness)
- $M_4 = \sigma_y^{2/3} / \rho$ (Beam flexural bending strength)
- $M_5 = E^{1/3} / \rho$ (Plate out-of-plane bending stiffness)
- $M_6 = \sigma_y^{1/2} / \rho$ (Plate yield & puncture resistance)
- $M_7 = G^{1/2} / \rho$ (Torsional shaft stiffness)
- $M_8 = \sigma_y^2 / E$ (Elastic strain energy storage density)
- $M_9 = \lambda / \rho$ (Thermal conduction efficiency)
- $M_{10} = \sigma_y / (\rho C_m)$ (Cost-normalized strength)

### 4. Incoterms 2020 Techno-Economic Procurement Model
Calculates actual Delivered Duty Paid ($C_{\text{DDP}}$) factory floor costs delivered to Nairobi via Kilindini Harbour, Port of Mombasa:
$$C_{\text{DDP}} = C_{\text{CIF}} + \text{Tariff}_{\text{EAC}} + \text{IDF} + \text{RDL} + \text{VAT} + \text{Port}_{\text{THC}} + \text{Inland}_{\text{SGR}} + \text{Clearance}_{\text{broker}}$$
Incorporates:
- **East African Community Common External Tariff (EAC CET):** 0%–25% based on raw ingot vs. semi-finished stock.
- **Import Declaration Fee (IDF):** 3.5% of CIF.
- **Railway Development Levy (RDL):** 2.0% of CIF.
- **Value Added Tax (VAT):** 16% on taxable import value.
- **Terminal Handling & Rail Haulage:** Mombasa port handling charges and Standard Gauge Railway (SGR) container transit to Nairobi Inland Container Depot (ICD).

### 5. Stochastic Inventory & Strategic Sourcing Risk
- **Silver-Pyke-Peterson Safety Stock ($SS$):** Buffers against maritime transit variance:
  $$SS = z_\alpha \sqrt{\mu_L \sigma_d^2 + d^2 \sigma_L^2}$$
- **Wilson-Harris Economic Order Quantity (EOQ):** Minimizes setup and inventory holding costs:
  $$\text{EOQ} = \sqrt{\frac{2 D S}{H}}$$
- **Kraljic 4-Quadrant Supply Portfolio:** Categorizes candidate materials into *Strategic*, *Bottleneck*, *Leverage*, or *Routine* quadrants.

### 6. Vector-Normalized Hwang-Yoon TOPSIS Ranking
Ranks surviving materials across disparate units using Euclidean column normalization and relative closeness coefficients ($C_i^* \in [0.000, 1.000]$):
- Ashby Mechanical Performance ($w_1 = 0.40$)
- Delivered Landed Cost DDP ($w_2 = 0.30$)
- Effective Lead Time ($w_3 = 0.15$)
- Supply Availability Ratio ($w_4 = 0.15$)

### 7. Dual-Tier Decoupled Intelligence & Circuit Breaker
- **Local Engine:** Executes locally via Ollama with **`llama3.2`**, constrained to a 250-token output limit and a 6.0-second non-blocking circuit breaker.
- **Automated Cloud Arbitration:** If the top two contenders exhibit a relative score difference $\Delta \le 8.0\%$, the system automatically queries the Google Cloud Gemini API (`gemini-1.5-flash`) for deep microstructural and failure-mode tie-breaking.

---

## Empirical Benchmark Results

| Metric | Target | EMS-OS Measured Value | Status |
| :--- | :--- | :--- | :--- |
| **End-to-End Latency** | $< 10.0\text{ s}$ | **$5.8\text{ s}$** (Intel i7 Quad-Core CPU) | Passed |
| **Numerical Hallucination Rate** | $0.00\%$ | **$0.00\%$** (Deterministic Grounding) | Passed |
| **Constraint Satisfaction Rate** | $100\%$ | **$100\%$** (100 Audit Scenarios) | Passed |
| **Ashby Mathematical Provenance** | $\delta_{\text{rel}} \le 10^{-4}$ | **$0.00 \times 10^{-6}$** | Exact |

---

## Directory Structure

```
Material selection LLM/
├── .streamlit/
│   └── config.toml           # UI styling and layout configuration
├── data/
│   ├── materials_catalog.json           # 1,490+ standardized materials database
│   ├── engineering_intent_dataset.json   # Intent training dataset
│   ├── build_dataset.py                 # Dataset assembly pipeline
│   └── generate_instruction_dataset.py  # Synthetic instruction pipeline
├── knowledge_base/                      # Curated technical engineering references
│   ├── ashby_methodology.md
│   ├── metals_and_alloys_selection.md
│   ├── advanced_composites_and_polymers.md
│   ├── hydrodynamic_surface_roughness_and_epoxy.md
│   ├── micro_hydro_kenya_case_study.md
│   └── polymer_degradation_water_uv.md
├── scripts/
│   └── build_materials_catalog.py       # Catalog generator and normalizer
├── src/
│   ├── __init__.py
│   ├── ashby_engine.py       # Deterministic continuum mechanics solver (10 indices)
│   ├── economics_engine.py   # Incoterms 2020 DDP, EOQ, Safety Stock, TOPSIS
│   ├── hydrodynamics.py      # Fluid shear and surface roughness modeling
│   ├── llm_orchestrator.py   # Decoupled Ollama/Gemini dual-tier orchestrator
│   ├── materials_db.py       # Materials database ingestion and querying
│   ├── nlp_parser.py         # Scientific prompt parser and intent extractor
│   ├── rag_engine.py         # ChromaDB semantic retrieval engine
│   ├── report_generator.py   # Markdown engineering dossier generator
│   ├── semantic_router.py    # Query intent classifier
│   └── train_nlp.py          # Intent model training pipeline
├── .env.example              # Environment variables template
├── .gitignore                # Production git exclusions
├── app.py                    # Streamlit interactive engineering workbench
├── cli.py                    # Headless command-line interface
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies
```

---

## Installation & Setup

### 1. Prerequisites
- **Python:** Version 3.10, 3.11, or 3.12 installed.
- **Ollama:** Download and install from [ollama.com](https://ollama.com/).
  Pull the local model:
  ```bash
  ollama pull llama3.2
  ```

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/your-username/Material-selection-LLM.git
cd Material-selection-LLM

# Create and activate virtual environment
# Windows:
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Optional: Provide a `GEMINI_API_KEY` in `.env` if cloud tie-breaking arbitration is desired).*

---

## Usage

### Graphical User Interface (Streamlit)
Launch the interactive workbench:
```bash
streamlit run app.py
```
Access the application in your browser at `http://localhost:8501`.

### Command-Line Interface (CLI)
Run headless evaluations directly from the terminal:
```bash
python cli.py --prompt "Submarine front transparent shield requiring high hydrostatic yield strength, optical transmission >85%, and saline corrosion resistance."
```

---

## Sample Engineering Benchmark Scenarios

1. **Submarine Transparent Bulkhead Shield:**
   - *Requirements:* Extreme hydrostatic pressure, high optical clarity ($>85\%$), flexural plate yield strength ($M = \sigma_y^{1/2}/\rho$), zero saline degradation.
   - *Engine Result:* Monolithic Cast PMMA (Acrylic) selected; structural metals disqualified by optical gating.

2. **High-Velocity MRI Coupling Bracket:**
   - *Requirements:* High-speed rotational fatigue, high stiffness ($M = E^{1/2}/\rho$), zero magnetic susceptibility ($\chi_m \approx 0$).
   - *Engine Result:* Titanium Ti-6Al-4V Grade 5 & PEEK-CF30; ferromagnetic alloy steels disqualified.

3. **Milling Machine Hydrostatic Coolant Tubing:**
   - *Requirements:* Hydrostatic burst pressure ($M = \sigma_y/\rho$), resistance to aggressive water-miscible cutting fluids and synthetic emulsions.
   - *Engine Result:* Polyoxymethylene (POM / Acetal) & 316L Stainless Steel; hydrolytically vulnerable polymers disqualified.

---

## Authors & Citation

```bibtex
@misc{mamai_mulu_2026,
  author       = {Enock Mamai and Mutuku Geoffrey Mulu},
  title        = {{Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection}},
  year         = {2026},
  howpublished = {Final Year Capstone Project, Department of Mechanical and Manufacturing Engineering, University of Nairobi},
  note         = {Supervised by Mr. Enoch K. Musyoka, Project Code: EKM/1/2026}
}
```
