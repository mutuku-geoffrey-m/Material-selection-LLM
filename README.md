# Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection

**Course:** FMM3 561 Engineering Project  
**Project Code:** EKM/1/2026  
**Department:** Department of Mechanical and Manufacturing Engineering  
**Faculty:** Faculty of Engineering, University of Nairobi  
**Academic Year:** 2025/2026  

---

## Authors & Supervision

- **Enock Mamai** — Registration No.: `F18/2117/2020`
- **Mutuku Geoffrey Mulu** — Registration No.: `F18/144332/2022`
- **Project Supervisor:** **Mr. Enoch K. Musyoka**, Lecturer, Department of Mechanical and Manufacturing Engineering, University of Nairobi

---

## 1. Project Overview

In mechanical engineering design, material selection is a foundational step that governs product reliability, weight, manufacturing complexity, and total cost. With thousands of commercially standardized engineering materials cataloged under ANSI, ISO, DIN, JIS, and ASTM standards, identifying the single best material for a given load case requires simultaneous optimization across multiple conflicting criteria.

While classical selection methods rely on manual two-dimensional Ashby charts, this manual approach becomes difficult when scaling to multi-variable constraints (such as combined plate bending, high-temperature service limits, chemical exposure, and regional import logistics). Conversely, general-purpose Large Language Models (LLMs) cannot be relied upon for direct engineering calculations because they sample words probabilistically, leading to made-up material properties and incorrect physical scaling relationships.

This software system, developed as our final year engineering project, addresses this problem through a decoupled architecture:
1. **Natural Language Translation:** A parser extracts mechanical requirements (load type, geometry, temperature limits, chemical exposures, and industry standards) from technical prompts.
2. **Boolean Physical Gating:** Filters out materials that fail hard physical constraints (e.g., optical transparency, cryogenic ductile-to-brittle limits, or non-magnetic requirements).
3. **Deterministic Ashby Calculation Engine:** Calculates analytical Michael F. Ashby performance indices across an expanded, unit-normalized database of 1,490 standardized engineering materials using pure numerical formulas in Python.
4. **Techno-Economic Sourcing & Logistics Module:** Calculates the realistic Delivered Duty Paid (DDP) cost to Nairobi via Kilindini Port (Mombasa), accounting for maritime freight, East African Community Common External Tariffs (EAC CET), Import Declaration Fees, Railway Development Levies, VAT, Mombasa port handling, and Standard Gauge Railway (SGR) rail haulage. It also models stochastic safety stock and Wilson-Harris Economic Order Quantities.
5. **TOPSIS Multi-Criteria Decision Analysis:** Ranks candidate materials by balancing mechanical performance, landed cost, lead time, and supply availability using vector-normalized TOPSIS.
6. **Local LLM Synthesis:** Uses a local offline language model (`llama3.2` running via Ollama) to synthesize practical machining, heat-treatment, and failure-prevention notes based on verified data sheets retrieved from a local ChromaDB store.

---

## 2. Methodology & Governing Formulations

### 2.1 Continuum Mechanics Ashby Indices

The calculation engine implements analytical Ashby indices for primary mechanical loading modes:

| Index | Loading Mode | Design Objective | Governing Formula ($M$) |
| :--- | :--- | :--- | :--- |
| $M_1$ | Tie in Tension | Minimum mass under elastic extension constraint | $E / \rho$ |
| $M_2$ | Tie in Tension / Pressure Vessel | Minimum mass under plastic yield load constraint | $\sigma_y / \rho$ |
| $M_3$ | Beam in Bending | Minimum mass under flexural stiffness constraint | $E^{1/2} / \rho$ |
| $M_4$ | Beam in Bending | Minimum mass under flexural plastic collapse | $\sigma_y^{2/3} / \rho$ |
| $M_5$ | Plate in Bending | Minimum mass under plate flexural stiffness | $E^{1/3} / \rho$ |
| $M_6$ | Plate in Bending | Minimum mass under plate yield/puncture load | $\sigma_y^{1/2} / \rho$ |
| $M_7$ | Shaft in Torsion | Minimum mass under torsional twist constraint | $G^{1/2} / \rho$ |
| $M_8$ | Elastic Spring | Maximum elastic strain energy storage per unit mass | $\sigma_y^2 / (E \rho)$ |
| $M_9$ | Thermal Conductor | Steady-state heat conduction per unit mass | $\lambda / \rho$ |
| $M_{10}$ | Cost-Normalized Tie | Minimum material cost under tensile load | $\sigma_y / (\rho C_m)$ |

### 2.2 Incoterms 2020 Landed Cost Model (Mombasa to Nairobi)

The delivered procurement cost per kilogram ($C_{\text{DDP}}$) delivered to factory stock in Nairobi is calculated as:

$$C_{\text{DDP}} = C_{\text{CIF}} + \text{Tariff}_{\text{EAC}} + \text{IDF} + \text{RDL} + \text{VAT} + \text{Port}_{\text{THC}} + \text{Inland}_{\text{SGR}} + \text{Clearance}_{\text{broker}}$$

Where:
- $C_{\text{CIF}} = C_{\text{EXW}} \cdot \gamma_{\text{form}} + C_{\text{freight}} + C_{\text{insurance}}$
- $\text{IDF} = 0.035 \times C_{\text{CIF}}$ (Import Declaration Fee)
- $\text{RDL} = 0.020 \times C_{\text{CIF}}$ (Railway Development Levy)
- $\text{VAT} = 0.160 \times (C_{\text{CIF}} + \text{Tariff} + \text{IDF} + \text{RDL})$
- Fixed port handling, documentation, and rail haulage from Mombasa to Nairobi Inland Container Depot (ICD) are set at \$0.42/kg.

### 2.3 Safety Stock and Order Quantity Formulations

- **Silver-Pyke-Peterson Stochastic Safety Stock ($SS$):**
  $$SS = z_\alpha \sqrt{\mu_L \sigma_d^2 + d^2 \sigma_L^2}$$
  Where $\mu_L$ and $\sigma_L$ represent sourcing lead-time mean and standard deviation, $d$ and $\sigma_d$ represent daily consumption parameters, and $z_\alpha$ is the normal safety factor for service level $\alpha$.

- **Wilson-Harris Economic Order Quantity (EOQ):**
  $$\text{EOQ} = \sqrt{\frac{2 D S}{H}}$$
  Where $D$ is annual material demand, $S$ is setup/ordering cost, and $H = i \cdot C_{\text{DDP}}$ is the annual inventory carrying cost.

---

## 3. Repository Structure

```
.
├── app.py                     # Streamlit user interface (Engineering Workbench)
├── cli.py                     # Headless command-line interface
├── requirements.txt           # Python package dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Version control exclusions
├── data/
│   ├── materials_catalog.json           # Curated database of 1,490+ materials
│   ├── engineering_intent_dataset.json   # Intent classification dataset
│   ├── build_dataset.py                 # Dataset assembly script
│   └── generate_instruction_dataset.py  # Data formatting utilities
├── knowledge_base/                      # Technical documentation and standards
│   ├── ashby_methodology.md
│   ├── metals_and_alloys_selection.md
│   ├── advanced_composites_and_polymers.md
│   ├── hydrodynamic_surface_roughness_and_epoxy.md
│   ├── micro_hydro_kenya_case_study.md
│   └── polymer_degradation_water_uv.md
├── scripts/
│   └── build_materials_catalog.py       # Catalog generator and normalizer
└── src/
    ├── __init__.py
    ├── ashby_engine.py       # Deterministic continuum mechanics equations
    ├── economics_engine.py   # Incoterms 2020 DDP, EOQ, Safety Stock, TOPSIS
    ├── hydrodynamics.py      # Fluid shear and surface roughness calculations
    ├── llm_orchestrator.py   # Decoupled inference and external API orchestrator
    ├── materials_db.py       # Database loading, filtering, and property lookup
    ├── nlp_parser.py         # Engineering requirement extraction from text
    ├── rag_engine.py         # ChromaDB semantic retrieval engine
    ├── report_generator.py   # Markdown technical report generation
    ├── semantic_router.py    # Query intent routing
    └── train_nlp.py          # Intent classification training
```

---

## 4. System Requirements & Installation

### Prerequisites
- Python 3.10, 3.11, or 3.12
- [Ollama](https://ollama.com/) (for running the local LLM offline)

### Step 1: Install Ollama and Pull the Model
Download and install Ollama from the official website. Then, from your terminal:
```bash
ollama pull llama3.2
```
Keep Ollama running in the background.

### Step 2: Clone the Repository & Set Up Virtual Environment
```bash
git clone https://github.com/mutuku-geoffrey-m/Material-selection-LLM.git
cd Material-selection-LLM

# On Windows:
python -m venv .venv
.venv\Scripts\activate

# On Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
The application runs completely offline using the local Ollama instance (`http://localhost:11434`). If you wish to test cloud model arbitration, you can optionally provide an API key in `.env`.

---

## 5. Running the System

### Web Interface (Streamlit)
To launch the interactive graphical workbench:
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

The workbench provides:
- Engineering scenario selection and custom prompt input.
- Interactive Ashby logarithmic selection charts ($E$ vs. $\rho$, $\sigma_y$ vs. $\rho$).
- Landed cost waterfall breakdown ($C_{\text{EXW}} \to C_{\text{CIF}} \to C_{\text{DDP}}$).
- Kraljic matrix supply risk quadrant visualization.
- Downloadable technical selection dossier in Markdown format.

### Command-Line Interface (CLI)
To run a query directly in headless mode:
```bash
python cli.py --prompt "Submarine front transparent shield requiring high hydrostatic yield strength, optical transmission >85%, and saline corrosion resistance."
```

---

## 6. Workbench User Manual & Exploration Guide

The EMS-OS workbench is designed to be **fully open-ended**. While pre-configured benchmark examples are provided in the drop-down menu for convenience, you are encouraged to enter **any custom mechanical engineering design brief** into the console.

### 6.1 Formulating an Open-Ended Technical Prompt

For the natural language translation layer to extract accurate boundary conditions and continuum mechanics parameters, formulate your brief including one or more of the following aspects:

1. **Component Type & Function:** What part is being engineered?
   - *Examples:* Cantilever beam, pressure vessel, high-speed spindle, drone arm, connecting rod, heat exchanger, turbine blade, gear, spring, or prosthetic implant.
2. **Primary Loading Mode / Stress State:** What physical forces act on the part?
   - *Tension / Tie:* Axial stretching, burst hoop stress in thin cylinders ($M = \sigma_y / \rho$ or $M = E / \rho$).
   - *Bending:* Cantilever or supported beam deflection ($M = E^{1/2} / \rho$) or plastic collapse ($M = \sigma_y^{2/3} / \rho$).
   - *Plate Out-of-Plane Bending:* Panels, bulkheads, car body panels ($M = E^{1/3} / \rho$ or $M = \sigma_y^{1/2} / \rho$).
   - *Torsion:* Shafts, couplings, drill strings ($M = G^{1/2} / \rho$).
   - *Elastic Energy Storage:* Helical or leaf springs ($M = \sigma_y^2 / E$).
   - *Thermal Conduction:* Heat sinks, cooling fins ($M = \lambda / \rho$).
3. **Environmental & Thermal Constraints:** Where does the part operate?
   - Temperature ranges (e.g. *cryogenic -196 °C, ambient, or high temperatures > 400 °C*).
   - Fluid exposure (e.g. *submerged in river sediment, marine saline water, industrial cutting fluids, acids, or vacuum*).
4. **Manufacturing Process:**
   - Universal search across all 1,490+ materials (metals, polymers, composites, ceramics) or restricted to *FDM Additive Manufacturing* filaments or *CNC Machining*.
5. **Governing Standards (Optional):**
   - E.g. *ASTM E466, ASTM A36, ISO 527, ASME Section VIII*.

### 6.2 Navigating the User Interface

The workbench interface is split into two primary panels:

#### Left Panel: Design Specification & Boundary Sizing
- **In-App User Manual (Collapsible):** Click to review operating instructions directly within the UI.
- **Standard Benchmark Library:** An optional drop-down containing calibrated engineering baselines. Selecting any preset automatically loads its brief into the text box. Choosing *Custom Specification (Blank)* clears the input for fresh entries.
- **Technical Engineering Design Brief:** An open-ended multi-line input where you type or edit your mechanical requirements.
- **Manufacturing Route:**
  - *Universal Multi-Process:* Evaluates all material families (structural steels, titanium, aluminum alloys, engineering polymers, continuous and short-fiber composites, and technical ceramics).
  - *FDM Additive Only:* Restricts candidate search to 3D printable filament grades (PETG-CF, PEEK, ASA, PLA, PA12-CF, TPU).
- **Annual Production Demand (kg):** Enter the estimated annual project consumption (e.g., 500 kg, 2,500 kg, 10,000 kg). The engine uses this to calculate Wilson-Harris Economic Order Quantities (EOQ) and evaluate supplier Minimum Order Quantity (MOQ) holding penalties.
- **Operational Environmental Kinetics:** Checkboxes to quickly flag specific service hazards (Submerged Hydrolysis, Cryogenic Thermal, Outdoor UV, High-Temp Flash, Vacuum Outgassing).
- **Inference Route (Sidebar):** Select between:
  - *Local Standalone LLM (llama3.2 via Ollama):* Local generative synthesis with verified ground-truth bounds.
  - *Deterministic Continuum Mechanics Solver [Fast < 0.2s]:* Pure mathematical physics and metallurgical evaluation with zero network latency.
  - *Cloud API (Google Gemini):* Cloud reasoning mode.
- **Execute Button:** Click **"Execute Screening & Optimization"** to launch the analysis.

#### Right Panel: Multi-Objective Analysis & Sizing
Once executed, the right panel populates with comprehensive engineering diagnostics:
- **Governing Material Banner:** Highlights the #1 optimal material, its material family, governing Ashby index, and key mechanical constants (yield strength $\sigma_y$, Young's modulus $E$, density $\rho$).
- **Interactive Log-Log Ashby Chart:** Generates an interactive Plotly property space chart ($E$ vs. $\rho$, $\sigma_y$ vs. $\rho$, or thermal conductivity vs. density) plotting the material universe with the theoretical Ashby selection guide line. Hover over any bubble to inspect mechanical properties.
- **Incoterms 2020 Sourcing & Landed Cost Breakdown:** A multi-column procurement table displaying Ex Works (EXW) price, Delivered Duty Paid (DDP) cost to Nairobi via Kilindini Harbour (Mombasa), customs tariffs (EAC CET), freight lead times, buffer safety stock, and Kraljic risk quadrant (*Strategic, Bottleneck, Leverage, Routine*).
- **Technical Dossier:** Displays detailed metallurgical commentary on microstructural trade-offs, operational failure modes (fatigue, creep, galvanic corrosion), and recommended fabrication directives.
- **Export Report:** Download the verified selection dossier as a clean Markdown report for your design log.

#### Sidebar Utilities
- **Design Cases Manager:** Create new design cases with **"+ New Design Case"** or switch between previous cases. Each case preserves its own independent prompt, inputs, and results.
- **Material Database Inspector:** Select any material from the 1,490-grade database to inspect its standardized mechanical properties, thermal limits, and raw cost.

### 6.3 Sample Open-Ended Prompts to Try

Copy and paste any of the following open-ended technical briefs into the text area to test different physics engines:

```text
1. Drone Arm (Aerospace / Flexural Stiffness):
"Design a lightweight cantilever arm for an autonomous agricultural drone carrying a 5 kg sensor payload under high wind gusts. Must maximize flexural bending stiffness per unit mass while resisting outdoor solar UV radiation."

2. Geothermal Valve Body (High-Temperature & Corrosive Media):
"Valving body for an Olkaria geothermal brine extraction line operating at 320 C and 40 bar pressure. Must resist hot saline sulfide stress corrosion cracking, prevent catastrophic thermal creep rupture, and conform to ASME Section VIII."

3. Marine Propeller Hub (Hydrodynamic Cavitation & Saline Immersion):
"High-speed marine vessel propeller hub operating continuously in coastal seawater under cyclic torsional shear stress at 2,800 RPM. Requires high shear modulus G > 40 GPa, immunity to pitting corrosion, and low galvanic potential."

4. Precision Optical Mirror Bulkhead (Dimensional Stability):
"Support bulkhead for a high-precision satellite optical camera. Requires near-zero thermal expansion coefficient, maximum specific stiffness E/rho to survive launch acoustic vibration, and zero outgassing in vacuum."

5. Heavy-Duty Truck Suspension Leaf Spring (Elastic Strain Energy):
"Heavy commercial transport vehicle suspension spring operating over rough gravel roads. Maximize elastic strain energy storage per unit weight (sigma_y^2 / E) while maintaining high fracture toughness and resistance to cyclic fatigue."
```

---

## 7. Citation

If referencing this project, please cite our technical report using the following IEEE format:

### IEEE Format
> E. Mamai and M. G. Mulu, "Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection," Final Year Engineering Project Report, Project Code: EKM/1/2026, Department of Mechanical and Manufacturing Engineering, University of Nairobi, Nairobi, Kenya, 2026. Supervisor: Mr. Enoch K. Musyoka.

### BibTeX Format
```bibtex
@techreport{mamai_mulu_2026,
  author      = {Mamai, Enock and Mulu, Mutuku Geoffrey},
  title       = {Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection},
  institution = {University of Nairobi, Department of Mechanical and Manufacturing Engineering},
  number      = {EKM/1/2026},
  type        = {Final Year Engineering Project Report},
  year        = {2026},
  address     = {Nairobi, Kenya},
  note        = {Supervised by Mr. Enoch K. Musyoka}
}
```
