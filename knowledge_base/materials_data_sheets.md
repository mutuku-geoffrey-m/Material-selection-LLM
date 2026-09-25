# Material Data Sheets (MDS) Knowledge Base for RAG Ingestion

## 1. Polylactic Acid (PLA)
- **Polymer Family:** Aliphatic Thermoplastic Polyester
- **Density:** 1240 kg/m³ (1.24 g/cm³)
- **Tensile Yield Strength:** 55 MPa (Dry, In-plane XY)
- **Ultimate Tensile Strength:** 60 MPa
- **Tensile Strength Z-axis (Interlayer):** 32 MPa
- **Young's Modulus (E):** 3.5 GPa (Dry)
- **Elongation at Break:** 6.0% (Brittle)
- **Flexural Modulus:** 3.8 GPa
- **Impact Strength (Izod Notched):** 3.2 kJ/m²
- **Fatigue Endurance Limit:** 18 MPa at 10^6 cycles
- **Glass Transition Temperature (Tg):** 58°C
- **Heat Deflection Temperature (HDT 0.45 MPa):** 52°C
- **Moisture & Water Saturation:** 28.4% tensile strength loss when saturated in water; 7.2% Young's modulus reduction.
- **UV Resistance:** Poor. Degrades rapidly under solar UV radiation.
- **FDM Processing:** Nozzle 190-220°C, Bed 45-60°C, Enclosure: Not required, Warping: Very Low, Standard Brass Nozzle (0.4mm).
- **Evaluation for Micro-Hydro:** UNACCEPTABLE for submerged blades due to severe hydrolytic water loss, low fatigue limit, and brittle failure under debris strikes.

## 2. Polyethylene Terephthalate Glycol (PETG)
- **Polymer Family:** Glycol-Modified Polyethylene Terephthalate Copolymer
- **Density:** 1270 kg/m³ (1.27 g/cm³)
- **Tensile Yield Strength:** 45 MPa
- **Ultimate Tensile Strength:** 50 MPa
- **Tensile Strength Z-axis:** 36 MPa (Strong inter-layer fusion)
- **Young's Modulus (E):** 2.1 GPa
- **Elongation at Break:** 18.0% (Ductile)
- **Flexural Modulus:** 2.2 GPa
- **Impact Strength (Izod Notched):** 7.5 kJ/m²
- **Fatigue Endurance Limit:** 24 MPa at 10^6 cycles
- **Glass Transition Temperature (Tg):** 80°C
- **Heat Deflection Temperature (HDT 0.45 MPa):** 70°C
- **Moisture & Water Saturation:** Only 3.1% tensile strength reduction in water; hydrophobic, chemically resilient.
- **UV Resistance:** Good.
- **FDM Processing:** Nozzle 230-250°C, Bed 70-85°C, Enclosure: Not required, Warping: Low, Standard Brass Nozzle (0.4mm).
- **Evaluation for Micro-Hydro:** Good moisture resistance, but lower Young's modulus (2.1 GPa) allows excessive blade tip deflection under hydrodynamic river forces.

## 3. Carbon Fiber Reinforced PETG (PETG-CF)
- **Polymer Family:** Short Carbon Fiber Composite (15-20% chopped CF)
- **Density:** 1320 kg/m³ (1.32 g/cm³)
- **Tensile Yield Strength:** 52 MPa
- **Ultimate Tensile Strength:** 65 MPa
- **Tensile Strength Z-axis:** 38 MPa
- **Young's Modulus (E):** 5.8 - 6.2 GPa (High stiffness)
- **Elongation at Break:** 4.5%
- **Flexural Modulus:** 5.9 GPa
- **Impact Strength (Izod Notched):** 6.2 kJ/m²
- **Fatigue Endurance Limit:** 36 MPa at 10^6 cycles (Superior fatigue threshold)
- **Glass Transition Temperature (Tg):** 82°C
- **Heat Deflection Temperature (HDT 0.45 MPa):** 78°C
- **Moisture & Water Saturation:** Highly hydrophobic, <3.8% change in water.
- **UV Resistance:** Excellent. Carbon fibers block UV light and protect polymer matrix.
- **FDM Processing:** Nozzle 240-265°C, Bed 75-85°C, Enclosure: Not required, Warping: Very Low. Hardened Steel or Tungsten Carbide nozzle (0.4mm - 0.6mm) MANDATORY due to abrasive fibers.
- **Evaluation for Micro-Hydro:** OPTIMAL MATERIAL for 3D-printed micro-hydro blades. High stiffness prevents flutter; superior fatigue resistance withstands cyclic river pulses; hydrophobic matrix prevents hydrolytic swelling. Requires epoxy surface smoothing to eliminate 40% boundary layer drag penalty.

## 4. Acrylonitrile Butadiene Styrene (ABS)
- **Density:** 1050 kg/m³
- **Tensile Yield Strength:** 40 MPa
- **Young's Modulus:** 2.3 GPa
- **Elongation at Break:** 12.0%
- **Glass Transition Temp:** 105°C
- **Moisture Degradation:** 8.5% tensile drop in water.
- **UV Resistance:** Poor. Rapid embrittlement under outdoor sunlight.
- **FDM Constraints:** High thermal warping. Heated chamber/enclosure mandatory (>80°C). Prone to delamination in Z-axis under cyclic shear.

## 5. Acrylonitrile Styrene Acrylate (ASA)
- **Density:** 1070 kg/m³
- **Tensile Yield Strength:** 42 MPa
- **Young's Modulus:** 2.4 GPa
- **Elongation at Break:** 15.0%
- **Glass Transition Temp:** 102°C
- **UV Resistance:** Outstanding.
- **FDM Constraints:** Moderate-high warping; requires enclosure. Moderate modulus.

## 6. Polyamide 12 (Nylon PA12)
- **Density:** 1020 kg/m³
- **Tensile Yield Strength:** 38 MPa
- **Young's Modulus:** 1.7 GPa (Dry), drops to 1.3 GPa (Wet)
- **Elongation at Break:** >120%
- **Moisture Degradation:** 15% tensile loss and 20% modulus loss in water due to plasticization.
- **FDM Constraints:** Highly hygroscopic; must be actively dried at 80°C. High flexibility causes blade stall.

## 7. Carbon Fiber Reinforced Nylon (PA12-CF)
- **Density:** 1150 kg/m³
- **Tensile Yield Strength:** 75 MPa
- **Young's Modulus:** 7.5 - 8.2 GPa
- **Elongation at Break:** 5.0%
- **Fatigue Limit:** 48 MPa
- **Moisture Degradation:** 12% tensile loss when water saturated.
- **FDM Constraints:** Requires high temp drying and hardened nozzle. Expensive ($75/kg) and low rural availability in Kenya.

## 8. Polycarbonate (PC)
- **Density:** 1200 kg/m³
- **Tensile Yield Strength:** 62 MPa
- **Young's Modulus:** 2.4 GPa
- **Glass Transition Temp:** 145°C
- **FDM Constraints:** Nozzle >280°C, Bed >110°C, extreme warping without dedicated heated chamber.

## 9. Aluminium 6061-T6 (Benchmark)
- **Density:** 2700 kg/m³
- **Tensile Yield Strength:** 276 MPa
- **Young's Modulus:** 68.9 GPa
- **Fatigue Limit:** 96 MPa
- **Manufacturing:** CNC milling or casting. Cannot be printed via desktop FDM. High lead time and cost in remote areas.

## 10. Stainless Steel 316L (Marine Benchmark)
- **Density:** 8000 kg/m³
- **Tensile Yield Strength:** 290 MPa
- **Young's Modulus:** 193 GPa
- **Fatigue Limit:** 240 MPa
- **Manufacturing:** Foundry casting or DMLS. High weight, heavy rotor inertia, months of import lead time for rural Kenya.
