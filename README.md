# Development of a RAG-Enabled Local Large Language Model System for Autonomous Mechanical Material Selection

**Course:** FMM3 561 Engineering Project  
**Project Code:** EKM/1/2026  
**Department:** Department of Mechanical and Manufacturing Engineering  
**Faculty:** Faculty of Engineering, University of Nairobi  
**Academic Year:** 2026/2027  

---

## Authors & Supervision

- **Enock Mamai** — Registration No.: `F18/2117/2020`
- **Mutuku Geoffrey Mulu** — Registration No.: `F18/144332/2022`
- **Project Supervisor:** **Mr. Enoch K. Musyoka**, Lecturer, Department of Mechanical and Manufacturing Engineering, University of Nairobi

---


## 1. Project Overview

Material selection governs the reliability, mass, manufacturability and cost of a mechanical component. Thousands of grades are standardised under ANSI, ISO, DIN, JIS and ASTM, and the choice for a given duty is rarely obvious. Classical selection relies on two-dimensional Ashby charts, which become difficult to apply when several constraints act together, such as bending stiffness, service temperature, chemical exposure and regional import logistics. General-purpose language models can discuss materials fluently, but they are not reliable sources of numerical property data and can recommend materials that are physically unsuitable.

EMS-OS addresses this by separating language understanding from engineering calculation. A compact local language model reads the design brief and returns a structured interpretation; every value it returns is validated against a closed vocabulary and against the text of the brief, and a rule-based parser provides the fallback and cross-check. All screening, ranking and costing is then performed by deterministic code, so the numerical result does not depend on the language model.

The pipeline comprises the following stages.

1. **Language understanding.** The local model (`llama3.2:3b`, served by Ollama) extracts the component type, governing load case, service temperature and pressure, environment, chemical media and any restriction to a material family. Output is constrained to a JSON schema and validated; if the model is unavailable the rule-based parser is used and the report states which interpretation was applied.
2. **Physical gating.** Materials that cannot satisfy hard constraints are removed, including service temperature, cryogenic ductility, optical transparency, non-magnetic service, requested family and chemical compatibility (for example liquid gallium against aluminium and copper). A table of common melts (gold, silver, platinum, copper, brass, bronze, aluminium, zinc, lead, tin, magnesium, glass and steel) records each melting point, the families the melt attacks and the families normally used to handle it; the stated service temperature is checked against the melting point, and a missing temperature is taken as the melting point plus 50 °C.
3. **Ashby screening.** Analytical Ashby indices are evaluated for the governing load case over the materials catalogue.
4. **Techno-economic evaluation.** Delivered Duty Paid cost to Nairobi via Mombasa is computed from each material's price, with freight, insurance, EAC customs duty, Import Declaration Fee, Railway Development Levy, VAT, port handling and clearance, together with lead-time safety stock and economic order quantity.
5. **Multi-criteria ranking.** Candidates are ranked by vector-normalised TOPSIS over six criteria: the governing Ashby index (weight 0.35), delivered cost (0.25), mean lead time (0.09), lead-time standard deviation (0.06), minimum-order penalty (0.10) and supply security, one minus the Kraljic supply-risk coordinate (0.15). The leaderboard also reports a relative price index, the delivered cost divided by the lowest delivered cost among the listed candidates.
6. **Report generation.** A report with manufacturing directives, advisories and sourcing analysis is produced. The local model contributes optional commentary after the ranking is complete; a missing or slow model never changes the ranking.

The materials catalogue contains 1,510 grades: 1,490 catalogue records and 20 curated reference grades defined in `src/materials_db.py`. The count shown in the interface is read from the database at run time.

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
| $M_9$ | Cost-Normalized Tie | Minimum material cost under tensile load | $\sigma_y / (\rho C_m)$ |
| $M_{10}$ | Thermal Conductor | Maximum steady-state heat conduction | $\lambda$ |

### 2.2 Incoterms 2020 Landed Cost Model (Mombasa to Nairobi)

The delivered procurement cost per kilogram ($C_{\text{DDP}}$) delivered to factory stock in Nairobi is calculated as:

$$C_{\text{DDP}} = C_{\text{CIF}} + \text{Tariff}_{\text{EAC}} + \text{IDF} + \text{RDL} + \text{VAT} + \text{Port}_{\text{THC}} + \text{Inland}_{\text{SGR}} + \text{Clearance}_{\text{broker}}$$

Where:
- $C_{\text{CIF}} = C_{\text{EXW}} \cdot \gamma_{\text{form}} + C_{\text{freight}} + C_{\text{insurance}}$ (with marine cargo insurance at 0.40% ad valorem on 110% of (FOB + freight) under Institute Cargo Clauses A).
- $\text{IDF} = 0.025 \times C_{\text{CIF}}$ (Import Declaration Fee, 2.5% under the Kenya Miscellaneous Fees and Levies Act).
- $\text{RDL} = 0.020 \times C_{\text{CIF}}$ (Railway Development Levy, 2.0% ad valorem).
- $\text{Tariff}_{\text{EAC}}$ follows the EAC Common External Tariff (CET) 4-band structure: 0% for primary raw materials and capital goods, 10% for intermediate goods not available locally, 25% for intermediate goods available in the region, and 35% for finished products.
- $\text{VAT} = 0.160 \times (C_{\text{CIF}} + \text{Tariff} + \text{IDF} + \text{RDL})$ (16.0% ad valorem, Kenya Value Added Tax Act).
- Port handling, SGR rail haulage, and customs clearance documentation:
  - $\text{Port}_{\text{THC}} = \$0.08/\text{kg}$ (Mombasa Kilindini Port terminal handling per KPA tariff schedule).
  - $\text{Inland}_{\text{SGR}} = \$0.10/\text{kg}$ (Standard Gauge Railway containerized rail freight from Mombasa to Nairobi ICD).
  - $\text{Clearance}_{\text{broker}} = \$0.05/\text{kg}$ (customs brokerage, Kentrade processing, and port documentation).
  - Total fixed destination logistics = \$0.23/kg.

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
├── app.py                         Streamlit user interface
├── cli.py                         Command-line interface
├── EMS-OS.exe                     One-click launcher (built with launcher/build_exe.bat)
├── Start_EMS-OS.bat               Launcher fallback when the executable has not been built
├── requirements.txt               Python dependencies
├── .env.example                   Configuration template
├── .streamlit/config.toml         Interface theme and server settings
├── launcher/
│   ├── launcher.py                Installation and start-up logic
│   └── build_exe.bat              Builds EMS-OS.exe with PyInstaller
├── data/
│   ├── materials_catalog.json     Catalogue of 1,490 engineering materials
│   └── engineering_intent_dataset.json   Training data for the intent classifier
├── models/nlp_intent_model.json   Trained intent classifier used by the rule-based parser
├── knowledge_base/                Reference documents indexed in the vector store
├── scripts/
│   ├── build_materials_catalog.py        Catalogue generation and normalisation
│   └── run_benchmark_full_pipeline.py    Runs the 100 benchmark scenarios and writes a review table
├── src/
│   ├── ashby_engine.py            Ashby indices, screening and chart generation
│   ├── compatibility.py           Family membership, chemical compatibility and advisories
│   ├── economics_engine.py        Landed cost, safety stock, EOQ, Kraljic classification and TOPSIS
│   ├── hydrodynamics.py           Fluid loading and surface-roughness calculations
│   ├── llm_intent.py              Language understanding with validation
│   ├── llm_orchestrator.py        Pipeline orchestration and report synthesis
│   ├── materials_db.py            Database loading and property access
│   ├── nlp_parser.py              Rule-based interpretation of design briefs
│   ├── rag_engine.py              ChromaDB retrieval
│   ├── report_generator.py        Markdown report export
│   ├── semantic_router.py         Optional intent router (disabled by default)
│   ├── text_matching.py           Boundary-aware keyword matching
│   └── train_nlp.py               Intent classifier training
└── tests/                         Unit, tolerance, sensitivity and benchmark tests
```

---

## 4. Installation

### 4.1 One-click start (Windows)

Run `EMS-OS.exe` (or `Start_EMS-OS.bat` if the executable has not been built). On first use the launcher installs any missing component (Python 3.12, Ollama, the Python dependencies and the `llama3.2:3b` model, approximately 2 GB), creates an `EMS-OS` shortcut on the desktop and opens the interface at `http://localhost:8501`. On later runs it only verifies the installation, starts Ollama and the interface if they are not running, loads the model into memory and opens the browser. Progress is printed in the launcher window and recorded in `launcher.log`. The first run requires an internet connection; afterwards the system operates offline except for the optional cloud arbitration.

To rebuild the executable, run `launcher\build_exe.bat` on a Windows computer with Python installed.

### 4.2 Manual installation

1. Install [Ollama](https://ollama.com) and download the model: `ollama pull llama3.2:3b`.
2. Create and activate a virtual environment: `python -m venv .venv`, then `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Linux, macOS).
3. Install the dependencies: `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env` and adjust the values if required.

### 4.3 Configuration

| Variable | Default | Purpose |
| :--- | :--- | :--- |
| `LOCAL_MODEL` | `llama3.2:3b` | Ollama model used for language understanding and commentary |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama endpoint |
| `EMS_UNDERSTANDING_TIMEOUT_S` | 120 | Time allowed for the model to interpret a brief |
| `EMS_LLM_TIMEOUT_S` | 120 | Idle timeout for streamed commentary |
| `EMS_CLOUD_TIMEOUT_S` | 20 | Timeout for optional cloud arbitration |
| `GEMINI_API_KEY`, `OPENAI_API_KEY` | empty | Optional keys for cloud arbitration of near-ties |
| `STREAMLIT_SERVER_PORT` | 8501 | Interface port |

The report also checks the cost limit, delivery limit and quantity stated in the brief against the evaluated candidates, honours explicit exclusions such as "no seawater exposure", and notes when several load cases are stated but a single governing index is used.

For cryogenic service, grades that lose ductility at low temperature (ferritic steels, cast irons, magnesium alloys and glassy thermoplastics) are excluded, and load-bearing supports such as dewar struts are ranked by the heat-leak index $\sigma_y/\lambda$; welded vacuum or pressure shells are restricted to weldable metals.

Cloud arbitration runs automatically when the top two candidates differ by no more than 8 % on the governing index; it uses the configured API key or, if none is set, the local model.

### 4.4 Troubleshooting

- **Interface reports that the model is not installed.** Run `ollama pull llama3.2:3b`, or reopen the launcher, which installs it.
- **No commentary in the report.** The report states the reason. Confirm with `ollama list` that the service is running and the model is present; the first request after start-up is slower because the model is being loaded.
- **Port 8501 in use.** Set `STREAMLIT_SERVER_PORT` in `.env`.
- **Launcher problems.** Consult `launcher.log` in the project folder.

---

## 5. Operation

### 5.1 Web interface

Start the interface with the launcher, or with `streamlit run app.py`. Enter a design brief in natural language or select a benchmark example, set the manufacturing route, annual demand and environmental conditions, and run the optimisation. The result panels present the governing specification, the Ashby selection chart, the comparative evaluation, the sourcing and economic order quantity analysis, the decision provenance (including which interpretation of the brief was applied) and the retrieved reference documents.

The interface offers a light and a dark theme (switch in the sidebar). Results are shown below the input panel so that wide tables use the full page width, and tables scroll horizontally when they exceed it. Commentary generated by the language model is restricted to catalogue values, is labelled as generated, and should be verified before use.

A brief is interpreted most reliably when it states the loading mode and geometry, the service temperature and pressure, the environment and fluids in contact with the part, and any material family the answer must belong to (for example, "Which aluminium alloy ...").

### 5.2 Command line

```
python cli.py --prompt "Lining for an incinerator operating at 1200 degrees Celsius" --mode LOCAL_LLM --demand 1500 --verbose
```

The `--mode` option accepts `LOCAL_LLM`, `CLOUD_API` and `AUTONOMOUS_EXPERT` (deterministic, no language model).

---

## 6. Validation

The test suite is run with `python -m unittest discover -s tests`. It covers the following.

- Agreement of the Ashby indices with their reference formulas to a relative tolerance of 10⁻⁵ (`test_ashby_tolerance.py`).
- Sensitivity of the TOPSIS ranking to perturbations of the criterion weights (`test_topsis_sensitivity.py`).
- Language understanding, family restriction, chemical compatibility, costing and catalogue consistency (`test_language_understanding.py`), using a simulated Ollama service.
- A benchmark of 100 engineering scenarios executed through the application pipeline, recording completion and latency (`test_100_benchmarks.py`).

`python scripts/run_benchmark_full_pipeline.py` writes `benchmark_100_full_pipeline.csv`, listing the interpretation and the three highest-ranked materials for each scenario, with blank columns in which a reviewer records the expected index and whether the result is correct. The benchmark demonstrates that the pipeline completes and measures its latency; correctness of the selections is established by this expert review.

---

## 7. Limitations

- The language model is small (3 billion parameters). Its output is validated and its commentary is restricted to catalogue values, but unusual briefs may still be misread and the commentary must be verified before use; the decision provenance panel shows when the rule-based parser was used instead.
- Slender compression members (struts, push-rods, wishbones and support columns) are ranked by the Euler-buckling index $E^{1/2}/\rho$, which has the same form as the beam-stiffness index M3 and is reported under its own label. For safety-critical duty, cast grades, metals below 200 MPa yield strength or 8 % elongation, and 2xxx or 7xxx aluminium in the T6 tempers (susceptible to stress-corrosion cracking) are excluded, and grades with equal index values are ordered by yield strength.
- Catalogue prices, lead times and sourcing categories are family-level estimates (for example, one price for all aluminium alloys), so grades of the same base metal are separated mainly by their properties. Aerospace-grade 2xxx and 7xxx aluminium is assigned to a European source. These figures should be replaced with supplier quotations before procurement decisions, and toughness, weldability and fabrication cost are not modelled (for example, 4130 steel is the usual choice for tubular racing suspension members, but ranks below aluminium on stiffness per unit mass).
- The molten-media table is general engineering guidance covering the melts listed above and should be confirmed against supplier and handbook data. The catalogue currently contains four technical ceramics and no graphite, zirconia, silicon nitride or refractory metals, so refractory selections are limited to alumina and silicon carbide until further grades are added.
- Selection is governed by the Ashby index of the identified load case together with hard gating rules. Properties such as corrosion behaviour, wear and joining are modelled only where an explicit rule exists.
- Prices, lead times and availability are catalogue estimates and should be confirmed with suppliers before procurement.
- Whether the Kenyan VAT base on imports includes the Import Declaration Fee and Railway Development Levy should be confirmed against current Kenya Revenue Authority guidance.

---

## 8. Citation

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
