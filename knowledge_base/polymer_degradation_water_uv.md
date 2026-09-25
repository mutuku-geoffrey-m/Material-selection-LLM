# Environmental Degradation Dynamics: Water Saturation, Hydrolysis, and UV Exposure

## 1. Aquatic Exposure and Hydrolytic Degradation
Deploying 3D-printed components in continuous freshwater river environments (such as Kenyan micro-hydro turbines) exposes polymeric chains to aggressive hydrolytic and mechanical degradation mechanisms.

### 1.1 Polylactic Acid (PLA) in Water-Saturated Environments
PLA is a bio-derived aliphatic polyester. When immersed in freshwater:
1. **Water Ingress & Plasticization:** Water molecules penetrate the amorphous inter-spherulitic regions of PLA, disrupting intermolecular hydrogen bonding and acting as an internal plasticizer.
2. **Hydrolytic Cleavage:** Water molecules react with ester linkages ($-\text{COO}-$) along the polyester backbone via hydrolytic ester cleavage:
   $$\sim\text{COO}\sim + \text{H}_2\text{O} \longrightarrow \sim\text{COOH} + \text{HO}\sim$$
   This reaction reduces the polymer's molecular weight ($M_w$) and induces embrittlement.
3. **Empirical Loss of Mechanical Properties (Ref 22):**
   - **Tensile Strength:** Drops by up to **28.4%** in water-saturated conditions.
   - **Tensile Modulus:** Drops by up to **7.2%**.
   - **Cyclic Fatigue Resistance:** Under continuous hydrodynamic pulsing in turbulent river flow, micro-cracks propagate along hydrolyzed layer interfaces, causing premature fatigue rupture at stresses below $18\text{ MPa}$.
   - **Engineering Verdict:** Pure PLA is **unsuitable and disqualified** for submerged micro-hydrokinetic turbine components.

### 1.2 Polyethylene Terephthalate Glycol (PETG) Resilience
PETG is a glycol-modified variant of polyethylene terephthalate.
- **Hydrophobicity:** The presence of cyclohexane dimethanol (CHDM) prevents crystallization and creates a tightly packed, chemically resistant amorphous barrier with very low equilibrium water absorption ($< 0.14\%$).
- **Degradation Resistance:** Submerged PETG retains $>96.5\%$ of its dry tensile strength (only a minor $\sim 3.1\%$ loss) and undergoes virtually zero hydrolytic chain scission at ambient river water temperatures ($15^\circ\text{C} - 28^\circ\text{C}$).
- **Fatigue Endurance:** Retains ductility and exhibits a high fatigue limit of $\sim 24\text{ MPa}$.

### 1.3 Carbon Fiber Reinforcement (PETG-CF)
While neat PETG resists water, its Young's modulus ($E \approx 2.1\text{ GPa}$) is relatively low, leading to substantial blade tip deflection under hydrodynamic drag forces.
- **Modulus Enhancement:** Incorporating 15-20% chopped high-modulus carbon fibers raises the in-plane Young's modulus to **$5.8 - 6.2\text{ GPa}$** (a $280\%$ increase over neat PETG).
- **Creep Resistance:** Carbon fiber networks restrict long-term viscoelastic chain slippage (creep), maintaining hydrodynamic pitch angle under continuous flow.
- **Hydrolytic Integrity:** Fiber-matrix interfacial coupling agents prevent capillary wicking along the fiber lengths, preserving high stiffness in water.

## 2. Ultraviolet (UV) Photodegradation under African Equatorial Solar Radiation
Kenya's equatorial location subjects outdoor infrastructure to intense solar UV irradiance (UV-A and UV-B index routinely exceeding 11).

### 2.1 Material UV Vulnerability
- **PLA & ABS:** Undergo severe photo-oxidative degradation. In ABS, UV photons cleave the unsaturated polybutadiene rubber phase, causing severe yellowing, surface chalking, micro-cracking, and loss of impact toughness within weeks of outdoor exposure.
- **PETG:** Possesses moderate inherent UV resistance, but long-term exposure can cause superficial yellowing.
- **PETG-CF:** Exceptional UV resistance. Carbon fibers act as an opaque barrier, absorbing and scattering incident UV photons and shielding the inner polymer matrix from photolytic cleavage.
- **ASA (Benchmark):** Acrylonitrile Styrene Acrylate utilizes saturated acrylic ester elastomer instead of polybutadiene, providing the highest UV stability of any non-fluoropolymer filament.
