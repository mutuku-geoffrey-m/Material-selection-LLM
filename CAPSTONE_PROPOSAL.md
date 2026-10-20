# UNIVERSITY OF NAIROBI
## FACULTY OF ENGINEERING
### DEPARTMENT OF MECHANICAL AND MANUFACTURING ENGINEERING

---

# FINAL YEAR CAPSTONE PROJECT PROPOSAL
**Academic Year:** 2026 / 2027  
**Project Title:** Computational Engineering Material Selection & Optimization System (EMS-OS) with Local Foundation LLM, Cloud Gemini Tie-Breaking Arbitration, and Supply Chain Techno-Economics  
**Candidate:** Mutuku Geoffrey Mulu  
**Registration Number:** F18/144332/2022  
**Degree Program:** Bachelor of Science in Mechanical and Manufacturing Engineering  
**Supervisor:** Capstone Evaluation Committee & Project Supervisor  
**Submission Date:** October 2026  

---

## EXECUTIVE SUMMARY

Engineering material selection is a foundational pillar of mechanical design, directly dictating structural integrity, component longevity, manufacturability, and commercial feasibility. In modern industrial and decentralized engineering environments, mechanical engineers face a vast materials universe comprising over 100,000 candidate alloys, polymers, technical ceramics, and composite systems. While Professor Michael F. Ashby’s analytical performance index framework provides the mathematical gold standard for material optimization (maximizing specific stiffness, specific yield strength, or thermal dissipation per unit mass), industrial adoption is severely bottlenecked by manual, static 2D chart cross-referencing and the total absence of real-time supply chain techno-economic intelligence.

Concurrently, the rapid emergence of Large Language Models (LLMs) offers unprecedented potential for natural language engineering synthesis. However, deploying raw, generative foundational models (e.g., standard GPT-4 or ungrounded Llama models) in mechanical design introduces catastrophic failure modes: hallucinations of non-existent material yield limits, omission of empirical environmental degradation (such as hydrolytic cleavage of PLA or stress corrosion cracking of austenitic stainless steels), and an inability to enforce deterministic continuum mechanics constraints. Furthermore, standard LLM tools completely ignore the procurement realities that govern real-world mechanical projects: Minimum Order Quantities (MOQ), Economic Order Quantity (EOQ) batch economics, and international shipping lead-time delays.

This capstone project proposes the formulation, development, and experimental validation of the **Engineering Material Selection & Optimization System (EMS-OS)**. Tailored specifically for qualified mechanical engineers, the platform eliminates colloquial abstractions in favor of structured scientific specifications and international standards (ISO, ASTM, ASME Section VIII, DIN). The system operates on a robust dual-tiered architecture:
1. **Local Foundation Engine:** Employs a local standalone LLM (`llama3.2` executed via Ollama) integrated with a persistent ChromaDB Retrieval-Augmented Generation (RAG) vector store, executing 100% on local engineering hardware with complete data sovereignty and zero mandatory cloud overhead.
2. **High-Throughput Standardized Catalog:** Ingests and standardizes 1,490+ materials across ANSI, ISO, DIN, JIS, and ASTM standards with unified mechanical, thermal, environmental, and techno-economic attributes.
3. **Automated Cloud Internet Arbitration:** When top competing candidate materials exhibit near-identical Ashby performance scores (score delta $\le 8.0\%$) or complex multi-objective trade-offs, the system automatically establishes a secure internet connection to the Google Cloud Gemini API to perform deep metallurgical, microstructural, and failure-mode arbitration, logging its complete chain-of-thought reasoning.
4. **Techno-Economic & Supply Chain Engine:** Integrates a classical Wilson-Harris Economic Order Quantity (EOQ) optimization formulation, evaluates supplier Minimum Order Quantity (MOQ) penalties, quantifies logistics lead-time delays (domestic road transit vs. international ocean freight), and computes a multi-criteria composite score.

This proposal establishes the technical rationale, mathematical formulations, software architecture, verification protocols, and execution milestones for the capstone project.

---

## 1. INTRODUCTION & BACKGROUND

### 1.1 The Challenge of Engineering Material Selection
Material selection represents one of the earliest and most consequential phases in the engineering design life cycle. An optimal choice minimizes component mass, eliminates operational failure modes, and minimizes life-cycle costs. Conversely, a sub-optimal selection leads to premature mechanical failure, uncompetitive manufacturing costs, or severe supply chain delays.

To transform material selection from qualitative guesswork into an exact science, Professor Michael F. Ashby developed the method of **Material Performance Indices**. By isolating:
- The **Function** (e.g., beam in bending, tie in tension, rotating shaft, pressure containment vessel),
- The **Objective** (e.g., minimize mass, maximize energy storage, minimize cost), and
- The **Constraints** (e.g., maximum deflection limit $\delta_{max}$, minimum yield strength $\sigma_y$, maximum service temperature $T_{max}$),

the governing physical equations can be analytically separated into functional, geometric, and material property parameters:
$$p = f(F, G, M)$$
Where $M$ is the characteristic material index to be maximized. For example, for a lightweight cantilever beam requiring high flexural stiffness:
$$M = \frac{E^{1/2}}{\rho}$$
where $E$ is Young's Modulus (GPa) and $\rho$ is material density ($\text{kg/m}^3$).

### 1.2 The Failure of Generic LLMs in Critical Engineering
The advent of Generative AI has prompted attempts to query general-purpose conversational LLMs for material recommendations. However, academic studies and rigorous evaluations reveal severe deficiencies:
1. **Hallucination of Mechanical Constants:** General LLMs frequently invent material properties or state yield strengths that exceed theoretical lattice limits.
2. **Inability to Screen Multi-Variable Databases:** A general LLM cannot deterministically sort and filter thousands of materials against hard environmental thresholds (e.g., disqualifying thermoplastics exceeding their Heat Deflection Temperature).
3. **Ignoring Environmental & Degradation Kinetics:** Generic models fail to account for moisture saturation penalties (e.g., PLA suffering a 28.4% tensile loss and 7.2% modulus reduction when submerged in water) or UV photo-oxidation embrittlement.
4. **Supply Chain Blindness:** Existing AI models treat material availability as an infinite, frictionless assumption, failing to differentiate between locally stocked commercial bar stock and specialty vacuum-induction melted superalloys requiring 6-month import lead times and 500 kg Minimum Order Quantities.

### 1.3 The Need for an Integrated Engineering System
To address these limitations, a production-grade engineering tool must combine:
- **Deterministic Continuum Mechanics & Ashby Formulations:** Absolute mathematical ground truth that cannot be overridden by statistical text probabilities.
- **Qualified Engineering Input Interfaces:** Full recognition of ISO, ASTM, ASME, and DIN standards.
- **Local-First Foundational LLM:** Standalone local deployment via Ollama/llama.cpp for privacy and shop-floor reliability.
- **Dynamic Cloud AI Arbitration:** Utilizing cloud LLMs (Gemini API) selectively for difficult, ambiguous tie-breaking edge cases.
- **Techno-Economic Logistics Sourcing Models:** Real-world inventory optimization (EOQ/MOQ) and freight lead-time modeling.

---

## 2. PROBLEM STATEMENT & JUSTIFICATION

### 2.1 Problem Statement
Mechanical design engineers currently lack an integrated computational platform capable of translating complex, multi-objective design specifications directly into mathematically verified material selections while accounting for empirical environmental degradation and procurement logistics. Existing solutions either rely on static 2D Ashby charts that cannot scale to modern high-throughput databases, or ungrounded conversational AI models prone to hallucination. Furthermore, existing engineering software packages evaluate material performance in complete isolation from supply chain variables, resulting in designs that are technically sound on paper but unprocurable in practice due to prohibitive Minimum Order Quantities, long import lead times, or excessive batch holding costs.

### 2.2 Justification of the Study
1. **Academic Rigor:** This research bridges physical continuum mechanics, high-throughput materials informatics, and neuro-symbolic AI systems.
2. **Industrial Impact:** Accelerates the engineering design cycle from days of manual catalog cross-referencing to seconds of computational screening.
3. **Decentralized Manufacturing & Sourcing Resilience:** Equips local engineering firms and decentralized operations with the analytical capacity to evaluate local domestic stocks against international imports, preventing costly supply chain disruptions.
4. **Elimination of Catastrophic AI Risks:** Guarantees zero hallucinations through strict deterministic boundary filtering and verified data provenance.

---

## 3. PROJECT OBJECTIVES

### 3.1 Main Objective
To design, implement, and validate an autonomous, deterministic engineering material selection and multi-objective optimization system (EMS-OS) that integrates Michael F. Ashby mechanics across a 1,490+ standardized materials catalog, local Ollama foundation reasoning, cloud Gemini tie-break arbitration, and supply chain techno-economics.

### 3.2 Specific Objectives
1. **Standardized Materials Database Curation:** Assemble, clean, and normalize a comprehensive catalog of 1,490+ standard engineering materials (metals, steels, aluminums, titaniums, superalloys, technical ceramics, continuous composites, and polymers) with verified mechanical, thermal, environmental, and techno-economic properties.
2. **Scientific Specification Parser Development:** Engineer an NLP translation module tailored for qualified mechanical engineers that parses structured design criteria, numerical limits ($\sigma_y$, $E$, $\rho$, $T$), and governing international standards (ISO, ASTM, ASME, DIN).
3. **Ashby Optimization Engine Implementation:** Formulate and execute analytical Ashby performance index algorithms for bending, axial tension, plate flexure, torsion, pressure containment, and thermal dissipation.
4. **Transparent Chain-of-Thought Pipeline:** Construct an engineering reasoning pipeline that transparently logs and displays all six phases of optimization (specification parsing, database screening, quantitative scoring, close contender detection, cloud arbitration, and techno-economic synthesis).
5. **Automated Cloud Internet Arbitration Protocol:** Formulate a tie-break detector that identifies competing candidate materials within an 8.0% score delta and automatically invokes Google Cloud Gemini API over the internet to perform deep metallurgical trade-off arbitration.
6. **Techno-Economic Sourcing & Inventory Module:** Implement Wilson-Harris Economic Order Quantity (EOQ) optimization, MOQ constraint validation, logistics lead-time modeling, and multi-criteria TOPSIS composite ranking.
7. **Empirical Benchmarking & Evaluation:** Stress-test the system across 15 adversarial mechanical edge cases and conduct a comparative evaluation experiment against baseline pure LLM and RAG-only systems.

---

## 4. THEORETICAL FORMULATION & METHODOLOGY

### 4.1 Ashby Performance Index Formulations
The system implements analytical performance indices derived from first-principles continuum mechanics:

| Component Function | Primary Loading Mode | Governing Constraint | Ashby Index to Maximize ($M$) |
| :--- | :--- | :--- | :--- |
| **Cantilever Spar / Beam** | Bending Deflection | Elastic Stiffness ($EI$) | $M = \frac{E^{1/2}}{\rho}$ |
| **Beam / Chassis Rail** | Bending Fracture | Plastic Yield Moment ($M_y$) | $M = \frac{\sigma_y^{2/3}}{\rho}$ |
| **Structural Tie / Cable** | Axial Tension | Elastic Deflection ($\Delta L$) | $M = \frac{E}{\rho}$ |
| **Tie / Pressure Vessel** | Axial Tension / Hoop Stress | Yield Burst Limit | $M = \frac{\sigma_y}{\rho}$ |
| **Skin Panel / Plate** | Out-of-Plane Bending | Flexural Plate Rigidity ($D$) | $M = \frac{E^{1/3}}{\rho}$ |
| **Cranial / Armor Plate** | Out-of-Plane Impact | Puncture / Yield Fracture | $M = \frac{\sigma_y^{1/2}}{\rho}$ |
| **Rotating Disc / Flywheel** | Centrifugal Rotation | Burst Angular Velocity ($\omega_b$) | $M = \frac{\sigma_y}{\rho}$ |
| **Elastic Spring / Damping** | Reversible Deflection | Maximum Elastic Energy Density | $M = \frac{\sigma_y^2}{E}$ |
| **Heat Sink / Thermal Fin** | Steady-State Fourier Conduction | Heat Flux Dissipation per Mass | $M = \lambda \text{ or } \frac{\lambda}{\rho}$ |
| **Thermal Barrier** | Transient Insulation | Heat Ingress Minimization | $M = \frac{1}{\lambda}$ |
| **Cyclic Machine Shaft** | Dynamic Alternating Stress | Fatigue Endurance Limit ($10^7$ cycles) | $M = \frac{\sigma_f}{\rho}$ |

### 4.2 Environmental Degradation Kinetics Modeling
Real-world service environments degrade mechanical properties. The engine applies deterministic penalty multipliers before ranking:
- **Freshwater Submersion & Hydrolysis:**
  $$\sigma_{y,\text{eff}} = \sigma_{y,0} \cdot (1 - \delta_{\text{water}})$$
  $$E_{\text{eff}} = E_0 \cdot (1 - \delta_{E,\text{water}})$$
  Where for hygroscopic polymers like unreinforced PLA, empirical testing shows $\delta_{\text{water}} = 28.4\%$ and $\delta_{E,\text{water}} = 7.2\%$.
- **Thermal Service Limit:** Materials where the operating temperature exceeds the Heat Deflection Temperature ($T_{\text{service}} > T_{\text{HDT}}$) or continuous service threshold are deterministically disqualified.

### 4.3 Techno-Economic Sourcing & Inventory Formulations
Material performance cannot be decoupled from financial and supply chain constraints.

#### 1. Economic Order Quantity (EOQ)
Using the Wilson-Harris lot-sizing model, the optimal batch order quantity that minimizes the sum of procurement setup costs and inventory carrying charges is formulated as:
$$\text{EOQ} = \sqrt{\frac{2 \cdot D \cdot S}{H}}$$
where:
- $D$ = Annual project demand (kg/year),
- $S$ = Order setup and procurement administration cost ($USD/order):
  - Domestic Local Stock: $S \approx \$120$ USD
  - Regional Distribution: $S \approx \$320$ USD
  - Global Import: $S \approx \$680$ USD (customs clearing, maritime tariffs)
- $H = i \cdot C_m$ = Annual inventory holding cost per kg-year, where $i = 20\%$ (annual carrying rate) and $C_m$ is raw material cost per kg.

#### 2. Minimum Order Quantity (MOQ) Constraint Validation
Suppliers mandate minimum production runs ($MOQ$). The engine evaluates batch feasibility:
- If $D \ge MOQ$: Batch feasibility is optimal.
- If $D < MOQ$: Sourcing incurs a small-lot penalty or requires carrying surplus stock ($MOQ - D$), quantified as:
  $$\Delta C_{\text{surplus}} = (MOQ - D) \cdot C_m \cdot i$$

#### 3. Multi-Criteria Decision Analysis (MCDA / TOPSIS Formulation)
Candidates are evaluated across normalized technical and commercial dimensions (0 to 100):
$$S_{\text{composite}} = w_{\text{tech}} \cdot S_{\text{tech}} + w_{\text{cost}} \cdot S_{\text{cost}} + w_{\text{avail}} \cdot S_{\text{avail}} + w_{\text{lead}} \cdot S_{\text{lead}} + w_{\text{mfg}} \cdot S_{\text{mfg}}$$
where:
- $S_{\text{tech}}$ = Normalized Ashby mechanical performance index,
- $S_{\text{cost}}$ = Normalized cost-efficiency metric ($M / (\rho \cdot C_m)$),
- $S_{\text{avail}}$ = Sourcing availability score (Domestic = 95, Regional = 72, Global Import = 45),
- $S_{\text{lead}}$ = Logistics lead-time score ($100 - 1.5 \times \text{LeadDays}$),
- $S_{\text{mfg}}$ = Manufacturability / machinability rating relative to 1212 steel.
- Standard engineering baseline weights: $w_{\text{tech}} = 0.40, w_{\text{cost}} = 0.25, w_{\text{avail}} = 0.15, w_{\text{lead}} = 0.10, w_{\text{mfg}} = 0.10$.

### 4.4 Multi-Engine Reasoning & Cloud AI Arbitration Protocol
To eliminate local LLM hallucinations while avoiding constant cloud reliance, the system implements an automatic dual-engine arbitration workflow:
1. **Local Base Execution:** The user's query is parsed, screened, and matched using the local Ollama LLM (`llama3.2`).
2. **Ambiguity & Close Contender Detection:** The engine calculates the performance delta between Rank 1 and Rank 2:
   $$\Delta_{\text{score}} = \frac{|\text{Score}_1 - \text{Score}_2|}{\text{Score}_1} \times 100\%$$
3. **Automated Cloud Trigger:** If $\Delta_{\text{score}} \le 8.0\%$ or if sharp conflicting trade-offs exist (e.g., higher yield strength vs. higher fracture toughness), the system automatically connects to Google Cloud Gemini API over the internet.
4. **Attribution & Transparency:** The Cloud AI evaluates microstructural mechanisms (e.g. grain boundary embrittlement, fatigue notch sensitivity) and delivers a definitive verdict. The final report explicitly records:
   *"Connected to the internet / Gemini API to arbitrate between Material A and Material B..."*

---

## 5. SYSTEM ARCHITECTURE & IMPLEMENTATION

The architecture consists of seven interconnected software modules developed in Python 3.11:

```
[ Qualified Mechanical Engineer Input (ISO / ASTM / ASME) ]
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 1. Scientific Specification Parser (src/nlp_parser.py)  │
│ - Extracts numerical constraints (E, Sy, rho, T_max)   │
│ - Identifies governing international standards         │
│ - Determines primary functional loading geometry       │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 2. High-Throughput Database (src/materials_db.py)      │
│ - 1,490+ standardized materials (ANSI, ISO, DIN, JIS)  │
│ - Mechanical, thermal, environmental, economic data    │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 3. Ashby Mechanics Engine (src/ashby_engine.py)        │
│ - Analytical index calculation (M = E^1/2 / rho, etc.) │
│ - Environmental degradation & temperature screening    │
│ - Deterministic candidate ranking                      │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 4. Supply Chain Optimizer (src/economics_engine.py)    │
│ - Wilson-Harris Economic Order Quantity (EOQ) sizing   │
│ - Minimum Order Quantity (MOQ) penalty assessment      │
│ - Domestic vs. Import logistics lead-time modeling     │
│ - Multi-Criteria Decision Analysis (MCDA) leaderboard │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 5. Multi-Engine Orchestrator (src/llm_orchestrator.py) │
│ - Foundation: Local Standalone LLM (llama3.2 / Ollama) │
│ - Tie-Break Detector (Delta <= 8.0%)                   │
│ - Cloud Internet Tie-Breaker: Google Gemini API        │
│ - Chain-of-Thought Thinking Process Logger             │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│ 6. Interactive Web UI & Reporting (app.py)             │
│ - Streamlit reactive interface with Ad-Hoc Explorer    │
│ - Interactive 2D/3D Plotly Ashby property charts       │
│ - Real-time Ollama daemon health monitor               │
│ - Exportable Markdown Engineering Specification Report │
└────────────────────────────────────────────────────────┘
```

---

## 6. VERIFICATION, BENCHMARKING & EXPERIMENTAL PLAN

To satisfy academic defense standards, the project incorporates a rigorous 3-way comparative evaluation experiment:

### 6.1 Experimental Comparison Setup
The system will be evaluated against a test suite of 15 adversarial mechanical engineering design cases:
- **Pipeline A (Baseline):** Pure Unconstrained LLM (Zero-shot GPT-4 / Llama 3.2 without RAG or physical constraints).
- **Pipeline B (RAG-Only):** Standard Vector Retrieval RAG without deterministic mathematical filtering.
- **Pipeline C (EMS-OS Full System):** Complete proposed architecture (Scientific Parser -> 1,490+ Database -> Ashby Filtering -> Cloud Gemini Arbitration -> Techno-Economic Sourcing).

### 6.2 Quantitative Evaluation Metrics
1. **Physical Feasibility Rate (%):** Percentage of recommended materials that strictly satisfy all mathematical stress, deflection, and temperature constraints.
2. **Hallucination Rate (%):** Instances where the model cites incorrect mechanical constants ($\sigma_y$, $E$, $\rho$) compared against ASTM/ISO datasheets.
3. **Degradation Awareness Rate (%):** Frequency with which the system correctly disqualifies hydro-degradable or thermally unviable materials.
4. **Supply Chain Completeness (%):** Successful generation of realistic procurement parameters (EOQ batch size, MOQ feasibility, lead times).

---

## 7. PROJECT WORK PLAN & SCHEDULE

The project will be executed over an 8-month timeline structured into four main phases:

```
Month:        1    2    3    4    5    6    7    8
Phase 1: Database Curation & SI Standardization
[==========]
Phase 2: Ashby Physics & Supply Chain Formulation
     [==========]
Phase 3: Software Implementation (Ollama, Gemini, UI)
          [===============]
Phase 4: Comparative Benchmarking & Thesis Defense
                    [===============]
```

### Milestone Schedule:
- **Milestone 1 (Month 2):** Master materials catalog completed with 1,490+ standardized records across ANSI, ISO, DIN, and JIS.
- **Milestone 2 (Month 4):** Ashby mechanics engine, scientific specification parser, and economics engine fully implemented and unit-tested.
- **Milestone 3 (Month 6):** Local Ollama integration, cloud Gemini tie-breaking arbitration, and interactive Streamlit UI operational.
- **Milestone 4 (Month 8):** Comparative experimental evaluation completed, results analyzed, and final thesis report prepared for defense.

---

## 8. RESOURCE BUDGET

| Category | Item Description | Source / Status | Estimated Cost (KES) |
| :--- | :--- | :--- | :--- |
| **Hardware** | Engineering Defense Laptop (Intel Core i7, 16GB RAM, Dedicated GPU) | Existing Student Equipment | 0 |
| **Local Software** | Ollama Engine & Llama 3.2 Open Weights | Open Source | 0 |
| **Database** | Autodesk / ANSI / ISO Literature Materials Dataset | Open Academic Datasets | 0 |
| **Cloud Computing** | Google Cloud Gemini API Tier (Arbitration Requests) | Google AI Studio Free/Standard Tier | 3,500 |
| **Documentation** | Thesis Printing, Technical Schematics & Binding | University Press | 6,500 |
| **Total** | | | **10,000 KES** |

---

## 9. CONCLUSION

The proposed **Engineering Material Selection & Optimization System (EMS-OS)** addresses a critical deficiency in contemporary mechanical design. By replacing generic, hallucination-prone AI prompts with a rigorous scientific parser, deterministic Ashby mechanics, a 1,490+ material database, automatic cloud Gemini tie-breaking arbitration, and Wilson-Harris supply chain economics, the project provides mechanical engineers with an indispensable, mathematically grounded design platform. The system bridges the gap between pure physics and procurement feasibility, delivering immense academic and industrial value.

---

## 10. REFERENCES

1. **Ashby, M. F. (2011).** *Materials Selection in Mechanical Design* (4th ed.). Butterworth-Heinemann, Oxford.
2. **Ashby, M. F., & Johnson, K. (2013).** *Materials and Design: The Art and Science of Material Selection in Product Design*. Butterworth-Heinemann.
3. **ISO 527-1:2019.** *Plastics — Determination of tensile properties — Part 1: General principles*. International Organization for Standardization.
4. **ASTM D638-14.** *Standard Test Method for Tensile Properties of Plastics*. ASTM International, West Conshohocken, PA.
5. **ASME Boiler and Pressure Vessel Code (BPVC), Section VIII:** *Rules for Construction of Pressure Vessels*. American Society of Mechanical Engineers, 2023.
6. **Silver, E. A., Pyke, D. F., & Peterson, R. (1998).** *Inventory Management and Production Planning and Scheduling* (3rd ed.). John Wiley & Sons.
7. **Lewis, P. R., & Reynolds, K. (2004).** *Forensic Materials Engineering: Case Studies*. CRC Press.
8. **Tuck, C. J., Hague, R. J. M., & Burns, N. (2007).** Rapid manufacturing: impact on supply chain management. *International Journal of Technology Management*, 37(1/2), 23-44.
9. **Vaswani, A., et al. (2017).** Attention is all you need. *Advances in Neural Information Processing Systems (NeurIPS 2017)*, 30.
10. **Touvron, H., et al. (2023).** Llama: Open and efficient foundation language models. *arXiv preprint arXiv:2302.13971*.

---
*End of Proposal Document.*
