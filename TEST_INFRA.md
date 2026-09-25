# E2E Test Infra: Material Selection LLM

## Test Philosophy
- Opaque-box, requirement-driven verification derived directly from engineering physics and user requirements in `ORIGINAL_REQUEST.md`.
- Anti-hardcoding integrity: Outputs must derive dynamically from Michael Ashby mathematical optimization formulas and physical property parameters, not hardcoded strings or superficial keyword lookup.
- Methodology: Category-Partition + Boundary Value Analysis (BVA) + Pairwise Combinatorial Testing + Real-World Workload Testing.

---

## 4-Tier Test Suite Architecture

### Tier 1: Feature Coverage (Loading Modes & Indices)
Covers all 8 mechanical and thermal loading modes with fundamental Ashby performance indices:
1. Bending beams (stiffness $E^{1/2}/\rho$, strength $\sigma_y^{2/3}/\rho$)
2. Tensile ties (stiffness $E/\rho$, strength $\sigma_y/\rho$)
3. Shell plates in bending (stiffness $E^{1/3}/\rho$, strength $\sigma_y^{1/2}/\rho$)
4. Rotational rotors / flywheels ($\sigma_y/\rho$)
5. Elastic dampers / springs ($\sigma_y^2/E$, $\sigma_y^2/(\rho E)$)
6. Cutting tools (Rockwell hardness $H$, wear resistance)
7. Thermal conductors ($k$) and insulators ($1/k$)
8. Pressure vessels (hoop stress $\sigma_y/\rho$, leak-before-break $K_{1c}/\sigma_y$)

### Tier 2: Boundary & Extreme Environmental Conditions
Covers extreme environments, degradation mechanisms, and boundary temperatures:
1. Submerged freshwater/marine (PLA ester hydrolysis: -28.4% tensile loss, -7.2% modulus drop)
2. Solar equatorial UV exposure (ABS polybutadiene photolysis embrittlement vs ASA/PETG-CF resistance)
3. Cryogenic temperatures (liquid nitrogen $-196^\circ\text{C}$, liquid helium $-269^\circ\text{C}$; ductile-to-brittle transition DBTT)
4. Extreme furnace heat (up to 1100°C: polymer HDT failure, metal homologous creep $T_H \ge 0.5 T_{melt}$, nickel superalloy & alumina survival)
5. Corrosive chemicals / strong mineral acids (316L SS, PEEK, PTFE, ceramics vs reactive metals)
6. High vacuum / deep space outgassing (NASA low-outgassing CVCM < 0.1%, TML < 1.0%)

### Tier 3: Cross-Feature Combinations & Regulatory Constraints
Pairwise combinations of mechanical loading under regulatory boundaries:
1. ISO 10993 cytotoxicity (in vivo orthopedic implants: eliminates cytotoxic Al, Cu; mandates Ti-6Al-4V ELI, PEEK, 316L, Al2O3)
2. FDA 21 CFR 177 food contact (prohibits loose/chopped carbon fibers in food; approves virgin PETG, 316L SS, POM)
3. Optical transparency ($T > 85\%$, haze < 2%: mandates amorphous Polycarbonate; eliminates opaque composites/metals)
4. Ultra-lightweight racing (extreme specific stiffness/strength: CFRP prepreg, Ti-6Al-4V)
5. Heavy crane hoisting (critical yield strength, toughness, and high safety factor)
6. Rural micro-grid viable fabrication (field repairability in Kenya: open-frame FDM printing, common spares)

### Tier 4: Real-World Multi-Domain Capstone Applications
Complex realistic engineering scenarios exercising multiple interacting physics domains:
1. Torrential river micro-hydro turbine blade ($M = \sigma_y^{2/3}/\rho$, water immersion, Schlichting hydrodynamic roughness drag, hardened nozzle, epoxy smoothing)
2. Deep-sea oceanographic pressure hull (external compressive buckling + saline corrosion)
3. High-temperature gas turbine flame holder nozzle (1100°C furnace gas + creep resistance)
4. Spacecraft solar array deployment hinge boom (high vacuum + thermal cycling $\pm 120^\circ\text{C}$)
5. Cryogenic liquid hydrogen transport valve (20 K, non-sparking, no low-temperature embrittlement)
6. High-speed surgical drill casing (ISO 10993 + steam autoclave sterilization 134°C)

---

## Anti-Hardcoding Forensic Verification Criteria
1. **Mathematical Provenance**: The calculated performance index $M_{calc}$ must match the first-principles formula evaluated on the selected material's properties within tolerance $\le 10^{-4}$.
2. **Property Perturbation Sensitivity**: If a candidate material's property (e.g. modulus or strength) is artificially modified, the calculated index $M$ must scale according to the mathematical exponent.
3. **Boundary Invalidation**: If the service temperature exceeds a polymer's $HDT$, the material must be disqualified, regardless of high room-temperature modulus.
4. **Capstone Continuity**: All 4 capstone benchmarks must remain strictly intact:
   - River turbine blade $\to$ `PETG-CF`
   - Hardened steel nozzle directive for chopped carbon fiber
   - Explicit `28.4%` PLA tensile degradation citation
   - Hydrodynamic `epoxy` smoothing protocol (XTC-3D) eliminating 40% drag penalty

---

## Test Execution Command
```powershell
.\.venv\Scripts\pytest -v tests/test_audit_100.py
```
Master test runner (all 56 regression tests + 100 audit tests):
```powershell
.\.venv\Scripts\python run_tests.py
```
