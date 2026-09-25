# Project: Material Selection LLM Engineering Audit & Remediation

## Architecture
The system is a physics-grounded materials selection and engineering recommendation engine combining Michael Ashby optimization physics with natural language parsing and RAG-augmented generation.

### Module Boundaries & Data Flow
1. **User Query / Prompt**: Ingested via CLI or programmatic interface.
2. **NLP Translation Layer (`src/nlp_parser.py`)**:
   - Classifies query into component categories.
   - Extracts boundary conditions (submerged water, solar UV, cryogenic, extreme heat, chemical/acid, vacuum).
   - Extracts regulatory & functional constraints (ISO 10993 biocompatible implants, FDA food contact, optical transparency, elastic damping, cutting hardness).
   - Deduces governing Ashby performance index ($M$) and manufacturing route (FDM, CNC, Universal).
3. **Materials Database (`src/materials_db.py`)**:
   - Authoritative property catalog containing mechanical, thermal, electrical, optical, and environmental degradation parameters for engineering materials across 14+ families.
   - Empirical degradation coefficients (e.g. PLA 28.4% tensile strength loss in water per Ref 22).
4. **Ashby Selection Engine (`src/ashby_engine.py`)**:
   - Dynamically evaluates Michael Ashby performance indices from physical property equations.
   - Implements thermal deflection gating ($T_{service} < HDT$ for polymers; homologous creep limits for metals).
   - Dynamically degrades material properties based on environmental exposure prior to index calculation.
   - Applies sharp regulatory filters (prohibits toxic Al in vivo, loose CF in food contact, opaque materials in optics).
   - Computes ranked recommendations with full calculation provenance.
5. **Hydrodynamics Engine (`src/hydrodynamics.py`)**:
   - Calculates chord Reynolds number ($Re_c$), Schlichting boundary layer skin-friction drag, and surface roughness penalties (40% raw FDM drag penalty eliminated by epoxy coating).
6. **LLM Orchestrator (`src/llm_orchestrator.py`)**:
   - Integrates parsed query, Ashby engine physics tables, and RAG knowledge base.
   - In autonomous expert offline mode, synthesizes mathematically verified engineering reports with explicit equations, tradeoffs, and manufacturing protocols.

---

## Code Layout
- `src/`
  - `nlp_parser.py`: Query categorization, constraint extraction, Ashby index binding.
  - `ashby_engine.py`: Dynamic Ashby performance index formulas, thermal/environmental/regulatory gating, ranking.
  - `materials_db.py`: Material catalog, mechanical/thermal/chemical properties, degradation constants.
  - `hydrodynamics.py`: Boundary layer fluid mechanics, Reynolds number, roughness drag penalty, epoxy protocol.
  - `rag_engine.py`: Vector search and BM25 fallback knowledge base retrieval.
  - `llm_orchestrator.py`: Multi-source synthesis, prompt augmentation, autonomous expert reports.
  - `report_generator.py`: Engineering specification formatting.
- `tests/`
  - `test_materials_db.py`: 6 tests (properties sanity, water degradation, FDM nozzle directives).
  - `test_ashby_engine.py`: 8 tests (Ashby index calculations, ranking, thermal disqualification, UV/water penalties).
  - `test_hydrodynamics.py`: 3 tests (Reynolds number, roughness drag penalty, epoxy smoothing).
  - `test_nlp_parser.py`: 9 tests (component classification, numerical extraction, Ashby index deduction).
  - `test_layman_prompts.py`: 9 tests (layman queries across diverse physical applications).
  - `test_prompt_suite.py`: 18 tests (edge cases, capstone benchmarks, high-temperature, CNC, solar).
  - `test_rag_and_llm.py`: 3 tests (RAG retrieval, augmented prompts, autonomous expert synthesis).
  - `test_audit_100.py`: Comprehensive 100-question multi-domain stress testing and physics audit suite.
- Root scripts:
  - `run_tests.py`: Master test runner.
  - `cli.py`: Interactive CLI interface with benchmark flag (`--benchmark`).

---

## Feature Inventory
Every requirement from the Survey phase and `ORIGINAL_REQUEST.md` is inventoried and mapped to a milestone:

| # | Feature | Description | Milestone | Source |
|---|---|---|---|---|
| 1 | 100-Question Multi-Domain Prompt Catalog | 100 distinct prompts covering 8 loading modes, 6 environments, 6 regulatory domains | M1 | R1 |
| 2 | Test Execution & Evaluation Harness | Automated test runner for the 100 prompts checking index math, material, constraints | M1 | R1, R2 |
| 3 | Anti-Hardcoding Forensic Verification | Mathematical verification that $M$ derives from physical equations ($|M_{calc} - M_{formula}|/M \le 10^{-5}$) | M2 | R2 |
| 4 | Thermal Deflection & Creep Gating | Enforce $T_{service} < HDT$ (polymers) and homologous creep $T_H < 0.4-0.5 T_{melt}$ (metals) | M3 | R2, R3 |
| 5 | Environmental Degradation Penalties | Empirical degradation under water (PLA -28.4%), UV photolysis (ABS), chemical acids, vacuum outgassing | M3 | R2, R3 |
| 6 | Regulatory Sharp Filters | Strict prohibition of toxic Al in vivo (ISO 10993), loose CF in food (FDA 21 CFR 177), opaque in optics | M3 | R2, R3 |
| 7 | Pressure Vessel & Toughness Modeling | Hoop stress index $M = \sigma_y/\rho$ and leak-before-break fracture toughness $M = K_{1c}/\sigma_y$ | M3 | R1, R3 |
| 8 | NLP Parsing Gaps Remediation | Regex and parsing for pressure vessels, negative cryogenic temperatures, vacuum booms, acid exposure | M3 | R3 |
| 9 | Capstone Benchmark Safeguards | Preserve river turbine blade => PETG-CF, hardened nozzle, 28.4% PLA citation, epoxy smoothing | M3, M4 | R3 |
| 10 | 56 Existing Regression Tests Pass | Ensure 100% pass rate across all 56 existing automated regression tests | M4 | R4 |
| 11 | 100-Question Audit Suite Pass | Ensure 100% pass rate across all 100 new audit tests | M4 | R4 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|---|---|---|---|
| 1 | Test Suite Creation | Author 100 distinct non-trivial engineering prompts and test harness (`tests/test_audit_100.py`) | none | IN_PROGRESS |
| 2 | Baseline Execution & Physics Integrity Audit | Run the 100 audit tests against the current engine, perform forensic audit of equation provenance | M1 | PLANNED |
| 3 | Root-Cause Investigation & Codebase Remediation | Remediate all identified gaps in `materials_db.py`, `ashby_engine.py`, `nlp_parser.py`, while preserving capstones | M2 | PLANNED |
| 4 | Complete Test Verification | Verify 56 regression tests + 100 audit tests pass with 100% success rate, execute final multi-agent gate | M3 | PLANNED |

---

## Interface Contracts

### 1. `nlp_parser.py` $\to$ `ashby_engine.py`
- `parse_query(query_text: str) -> dict`:
  - Output fields: `component_type`, `suggested_index`, `loading_type`, `manufacturing_route`, `boundary_conditions` (`submerged_aquatic_exposure`, `outdoor_uv_exposure`, `food_contact_safe`, `biocompatible_implant_required`, `optical_transparency_required`, `chemical_acid_exposure`, `high_vacuum_exposure`, `is_cryogenic`), `numerical_constraints` (`service_temperature_c`, `pressure_bar`, `operating_rpm`).

### 2. `ashby_engine.py` $\to$ `materials_db.py`
- `calculate_ashby_index(material: dict, index_name: str, water_degraded: bool = False, print_orientation: str = "xy") -> float`
- `rank_materials(parsed_constraints: dict) -> list[tuple[str, float, dict]]`
- Evaluates properties: $\rho$ (density), $E$ (modulus), $\sigma_y$ (yield strength), $\sigma_u$ (UTS), $\lambda$ / $k$ (thermal conductivity), $HDT$, $T_{melt}$, $K_{1c}$ (fracture toughness), environmental drop factors.

### 3. `llm_orchestrator.py` $\to$ `ashby_engine.py` / `nlp_parser.py`
- Ingests parsed constraints and top ranked materials from `rank_materials()`.
- Generates structured synthesis citing exact Ashby index equation, performance score, thermal limits, degradation citations, and manufacturing directives.
