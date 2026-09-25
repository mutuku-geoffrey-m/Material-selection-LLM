# Fused Deposition Modeling (FDM) Additive Manufacturing Constraints

## 1. Introduction & Physical Mechanics
Fused Deposition Modeling (FDM) / Fused Filament Fabrication (FFF) constructs three-dimensional parts by extruding molten thermoplastic filaments layer-by-layer through a heated nozzle. While FDM dramatically democratizes localized manufacturing—reducing tooling and mold costs by over 50%—it introduces critical physical phenomena not captured by traditional isotropic material charts.

## 2. Mechanical Anisotropy and Layer Adhesion
Unlike injection molded or subtractively machined metals, FDM components exhibit pronounced anisotropic mechanical properties. The tensile strength and modulus depend directly on the angle between the applied stress vector and the extruded filament lines.

### 2.1 Anisotropy Ratios
1. **In-Plane ($X-Y$ Axis):** High tensile strength governed by the continuous polymeric backbones and aligned carbon fibers along the extruded bead.
2. **Inter-Layer ($Z$ Axis):** Governed solely by thermal fusion and polymer reptation across the adjacent layer boundaries.
- **PLA:** $XY$ tensile strength $\approx 55\text{ MPa}$, $Z$-axis tensile strength $\approx 32\text{ MPa}$ (anisotropy ratio $\approx 0.58$).
- **ABS:** $XY$ tensile strength $\approx 40\text{ MPa}$, $Z$-axis tensile strength $\approx 22\text{ MPa}$ (anisotropy ratio $\approx 0.55$). High thermal contraction induces internal interlaminar residual stresses, making ABS highly susceptible to layer cleavage.
- **PETG:** $XY$ tensile strength $\approx 45\text{ MPa}$, $Z$-axis tensile strength $\approx 36\text{ MPa}$ (anisotropy ratio $\approx 0.80$). Excellent melt mobility yields superior layer-to-layer weld strength.
- **PETG-CF:** $XY$ tensile strength $\approx 62\text{ MPa}$, $Z$-axis tensile strength $\approx 38\text{ MPa}$ (anisotropy ratio $\approx 0.61$). While chopped fibers align along the extrusion path providing massive in-plane stiffness ($E \approx 6.2\text{ GPa}$), they do not cross the inter-layer boundary, leaving $Z$-strength dependent on the base PETG matrix.

### 2.2 Optimal Turbine Blade Print Orientation
- **Cantilever Bending Loading:** Hydrodynamic river thrust exerts maximum tensile and compressive bending stresses along the span of the blade from root to tip.
- **Orientation Directive:** Blades must be oriented with their long spanwise axis lying in the $X-Y$ plane (e.g. at a 30° to 45° tilt supported by dense tree supports, or split into spanwise halves).
- **Failure Mode Warning:** Printing blades vertically (span along $Z$-axis) concentrates cyclic hydrodynamic bending moments directly across the weakest interlaminar weld planes, leading to rapid catastrophic root fracture.

## 3. Abrasive Nozzle Wear from Carbon Fiber Reinforcement
Carbon fibers embedded in composite filaments (such as PETG-CF and PA-CF) possess extreme micro-hardness (Mohs hardness 7-8), far exceeding the hardness of standard brass nozzles (Mohs hardness 3).
- **Brass Nozzle Degradation:** Extruding just 250 to 500 grams of carbon fiber composite filament erodes a standard 0.40 mm brass nozzle orifice into an irregular oval exceeding 0.65 mm.
- **Consequences:** Loss of extrusion pressure, severe under-extrusion, stringing, dimensional inaccuracy, and degraded surface finish.
- **Mandatory Directive:** Hardened steel, tungsten carbide, or polycrystalline diamond/ruby nozzles must be installed. A 0.60 mm nozzle orifice is recommended to prevent fiber clumping and clogging.

## 4. Hygroscopic Sensitivity & Filament Conditioning
Polymer filaments absorb ambient atmospheric moisture via hydrogen bonding:
- **Nylon (PA12 / PA6):** Highly hygroscopic. Saturated nylon hydrolyzes during extrusion at 260°C, causing steam voids, foaming, popping, and up to 50% loss of tensile strength. Must be dried at 80°C for 8 hours and printed from an airtight desiccant feedbox.
- **PETG & PETG-CF:** Moderately hygroscopic. Absorbed moisture causes polymer chain scission in the melt zone and cosmetic stringing. Must be dried at 65°C for 6 hours prior to critical structural prints.
- **PLA:** Low-to-moderate moisture absorption. Should be dried at 45°C for 4 hours if stored in high-humidity tropical environments.

## 5. Thermal Chamber & Warping Dynamics
- **PLA & PETG-CF:** Extremely low thermal expansion coefficient. Low shrinkage allows printing without heated enclosures on open-frame portable printers.
- **ABS & PC:** High thermal shrinkage coefficient ($> 1.0 \times 10^{-4}\ \text{K}^{-1}$). Subject to catastrophic corner warping, bed release, and layer cracking without an active heated build chamber ($> 80^\circ\text{C}$), rendering them unsuitable for decentralized rural repairs.
