# Hydrodynamic Boundary Layer Physics, Surface Roughness, and Post-Processing Directives

## 1. Boundary Layer Mechanics on Hydrokinetic Turbine Blades
In micro-hydrokinetic river applications, turbine blades convert the kinetic energy of flowing river water into rotational torque. Unlike aircraft wings operating in low-density air, hydrokinetic blades operate in water (density $\rho \approx 1000\text{ kg/m}^3$), where hydrodynamic pressure and skin friction shear stresses are several orders of magnitude higher.

### 1.1 Chord Reynolds Number Envelope
For a hydrokinetic river turbine operating in typical Kenyan river flows (e.g., Tana River, Tungu-Kabiri, Sondu Miriu):
- Water velocity $u = 1.5\text{ to } 4.0\text{ m/s}$
- Hydrofoil chord length $c = 0.10\text{ to } 0.35\text{ m}$
- Water kinematic viscosity $\nu \approx 1.004 \times 10^{-6}\text{ m}^2/\text{s}$ at $20^\circ\text{C}$

The chord Reynolds number is defined by:
$$Re_c = \frac{u \cdot c}{\nu}$$
Substituting typical parameters:
$$Re_{c,min} = \frac{1.5 \times 0.10}{1.004 \times 10^{-6}} \approx 0.15 \times 10^6$$
$$Re_{c,mid} = \frac{2.5 \times 0.18}{1.004 \times 10^{-6}} \approx 0.45 \times 10^6$$
$$Re_{c,max} = \frac{4.0 \times 0.35}{1.004 \times 10^{-6}} \approx 1.4 \times 10^6$$
For higher speed runners or tip sections, $Re_c$ routinely operates between $0.8 \times 10^6$ and $4.8 \times 10^6$.

## 2. FDM Surface Roughness & Boundary Layer Transition
Fused Deposition Modeling extrudes filaments in discrete layers (typically $0.15\text{ mm}$ to $0.30\text{ mm}$ layer height). This leaves macroscopic cusps, grooves, and layer seams along the blade contours.

### 2.1 Roughness Topology
- **Arithmetic Roughness:** As-printed FDM surface roughness typically ranges from $R_a = 15\ \mu\text{m}$ to $25\ \mu\text{m}$ (reaching $30\ \mu\text{m}$ on carbon-fiber composite finishes).
- **Equivalent Sand-Grain Roughness:** $k_s \approx 2.5 \cdot R_a \approx 37.5\ \mu\text{m} \text{ to } 62.5\ \mu\text{m}$.
- **Relative Roughness:** $\frac{k_s}{c} \approx \frac{50 \times 10^{-6}\text{ m}}{0.18\text{ m}} \approx 2.8 \times 10^{-4}$.
- **Skewness Profile ($R_{sk}$):** Layer lines create periodic negative valleys and positive peaks.

### 2.2 Fluid Dynamic Drag Surge and Stall
On an aerodynamically smooth hydrofoil, the boundary layer remains laminar over the forward $20\%\text{ to }40\%$ of the chord before transitioning to turbulent flow.
When macroscopic FDM roughness elements ($k_s$) exceed the critical roughness Reynolds number ($Re_k = \frac{u_k k}{\nu} > 120$):
1. **Premature Boundary Layer Tripping:** Distributed roughness elements trip the boundary layer into fully turbulent flow immediately adjacent to the leading edge ($x/c < 0.05$).
2. **Skin Friction Drag Surge:** Fully turbulent flow exhibits significantly higher wall shear stress than laminar flow.
3. **Lift-to-Drag Ratio Penalty:** Rigorous wind tunnel and flume experiments (Sandia National Laboratories, Ref 52; Ehrmann et al.) demonstrate that distributed surface roughness can decrease the maximum lift-to-drag ratio $(C_L / C_D)_{max}$ by **up to 40%**.
4. **Dynamic Stall & Power Drop:** At higher angles of attack, boundary layer separation occurs prematurely, inducing dynamic stall, blade vibrations, and severely degrading turbine power coefficient ($C_p$).

## 3. Prescribing Post-Processing Directives: Epoxy Resin Surface Optimization
To eliminate the $40\%$ drag penalty, the autonomous material selection tool must prescribe a mandatory surface treatment protocol:

### 3.1 UV-Curable / 2-Part Epoxy Coating Mechanism
Applying a low-viscosity self-leveling epoxy resin (such as the commercially validated XTC-3D formulation):
- **Capillary Valley Filling:** Due to low surface tension, the liquid epoxy flows into the negative skewness valleys between extruded layer lines, leveling the macroscopic grooves.
- **Hydraulically Smooth Regime:** Post-cure wet-sanding reduces the outer surface roughness to $R_a < 1.2\ \mu\text{m}$ ($k_s / c < 1.5 \times 10^{-5}$). In this regime, roughness asperities remain submerged within the laminar sublayer ($y^+ < 5$), fully eliminating the $40\%$ drag penalty and restoring smooth-foil $(C_L / C_D)$ performance.
- **Hermetic Infill Sealing:** Untreated FDM prints possess microscopic pores between beads. Water under dynamic river pressure gradually permeates the blade, filling the internal infill voids (increasing rotor inertia by over $300\%$ and accelerating hydrolytic degradation). The epoxy barrier forms an impenetrable, hermetic shield against deep water ingress.

### 3.2 Actionable Fabrication & Coating Protocol
1. **Print Configuration:** PETG-CF filament, $0.20\text{ mm}$ layer height, $100\%$ infill at blade root, gyroid infill ($40\%$) with $4$ perimeters for mid-span. Hardened steel $0.6\text{ mm}$ nozzle at $250^\circ\text{C}$, bed at $80^\circ\text{C}$.
2. **Surface Degreasing:** Wipe printed blade with isopropyl alcohol.
3. **Resin Application:** Mix 2-part epoxy resin (or UV-curable formulation) and apply a uniform $0.15\text{ mm}$ coat with a foam brush.
4. **Curing:** Allow 3.5 hours ambient cure (or 15 min 395nm UV cure).
5. **Finishing:** Wet-sand sequentially with 400, 800, and 1200-grit silicon carbide paper using water lubrication until mirror-smooth hydrofoil contour is achieved.
