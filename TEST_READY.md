# E2E Test Suite Ready

## Test Runner
- Audit suite command: `.\.venv\Scripts\pytest -v tests/test_audit_100.py`
- Master regression command: `.\.venv\Scripts\python run_tests.py`
- Total audit test items: 100 (P001 to P100)
- Total regression test items: 56

## Coverage Summary
| Tier | Count | Description |
|---|---|---|
| 1. Feature Coverage | 25 | All 8 mechanical/thermal loading modes in isolation |
| 2. Boundary & Corner | 25 | Cryogenic (-196°C), furnace heat (up to 1100°C), vacuum, acid corrosion, water immersion, UV |
| 3. Cross-Feature Combinations | 25 | Loading modes crossed with regulatory boundaries (ISO 10993, FDA 21 CFR 177, optical clarity, racing) |
| 4. Real-World Application | 25 | Complex multi-physics scenarios (river hydro turbine, deep-sea hull, spacecraft boom, surgical drill) |
| **Total** | **100** | Full 100-prompt engineering audit suite |

## Baseline Results (Pre-Remediation)
- Audit Suite: 30 Passed, 70 Failed (30.0% pass rate) in 65.78s
- Regression Suite: 56 Passed, 0 Failed (100% pass rate) in 24.88s
- Capstone benchmark (P001: River turbine blade => PETG-CF, hardened steel nozzle, 28.4% PLA degradation citation, epoxy smoothing protocol) strictly preserved and passing.

## Identified Remediation Areas for Milestone 3
1. **Pressure Vessels (P089–P100)**: Add cylinder/vessel parsing and hoop stress / leak-before-break index selection.
2. **High-Temperature Creep Gating (P006, P021, P044, P056, P065, P079, P081, P087)**: Enforce metal homologous creep limits ($T_H = T/T_{melt} < 0.5$) in `ashby_engine.py` and supply melting point metadata in `materials_db.py`.
3. **Thermal Insulation (P079–P081, P084)**: Correct parser mapping from `thermal_conductivity` to `thermal_insulation` ($1/k$).
4. **Food Contact Safety (P024, P035, P049, P061)**: Expand food vocabulary parsing (poultry, dairy, puree, cheese) to trigger FDA 21 CFR 177 filters and disqualify chopped carbon fiber composites.
5. **Cryogenic Temperature Regex (P005, P033, P048, P055)**: Support negative temperatures (e.g. `-196 C`) and DBTT disqualification of ferritic steels and brittle elastomers.
6. **Cutting Tools & Wear (P064–P075)**: Implement `CUTTING_TOOL_WEAR` index ($M = H$) and add hardness/wear properties to `materials_db.py`.
