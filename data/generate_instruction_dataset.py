"""
Generates instruction-tuning dataset for fine-tuning local Large Language Models
(e.g., Llama-3.2, Mistral-7B, Phi-3) using QLoRA/LoRA on Hugging Face / Unsloth / Ollama.

Format: Standard Alpaca / ChatML JSONL with instruction, input context, and verified Ashby response.
"""

import json
import os

INSTRUCTION_PROMPT = (
    "You are an expert mechanical engineering consultant specializing in Michael Ashby's "
    "material selection methodologies, continuum mechanics, and manufacturing constraints. "
    "Given the user's component description, identify the governing Ashby performance index, "
    "derive the mathematical optimization formula, evaluate environmental and physical constraints, "
    "and recommend the optimal engineering material with comparative justification."
)

SAMPLE_PAIRS = [
    {
        "user_query": "I want to create a spoiler for a car",
        "component": "Automotive Aerodynamic Rear Wing / Spoiler",
        "ashby_index": "Plate Bending Stiffness (M = E^(1/3) / ρ) and Beam Bending Stiffness (M = E^(1/2) / ρ)",
        "environmental_factors": "Direct solar UV radiation, all-weather temperature swings (-20°C to +50°C), road salt and rain exposure.",
        "primary_recommendation": "Carbon Fiber Reinforced PETG (PETG-CF) or Acrylonitrile Styrene Acrylate (ASA)",
        "technical_rationale": (
            "An automotive rear spoiler acts as an aerodynamic downforce wing subject to distributed dynamic pressure "
            "(q = 0.5 * rho_air * v^2). The governing objective is minimum mass for a specified flexural stiffness to prevent "
            "flutter and aerodynamic stall without penalizing the vehicle's rear polar moment of inertia. "
            "Heavy metals such as Titanium Ti-6Al-4V (density 4.43 g/cm^3, $110/kg) and Alloy Steel 4140 (7.85 g/cm^3) "
            "are commercially unviable and dynamically counterproductive, adding excessive mass to the rear overhang. "
            "For performance applications, Carbon Fiber Reinforced PETG (PETG-CF) provides high specific modulus (6.05 GPa) "
            "at low density (1.32 g/cm^3) with intrinsic carbon fiber UV shielding. For mass-market OEM exterior trim, "
            "ASA provides exceptional photolytic UV stability against yellowing and impact toughness."
        ),
        "manufacturing_directives": "FDM 3D printing with hardened steel nozzle (245-265°C, bed 75-85°C) or injection molding."
    },
    {
        "user_query": "I need to make blades for a wind turbine",
        "component": "Horizontal-Axis Wind Turbine Aerofoil Blade",
        "ashby_index": "Beam Bending Stiffness against Tip Deflection (M = E^(1/2) / ρ) and Specific Fatigue Strength (M = σ_fatigue / ρ)",
        "environmental_factors": "Outdoor solar UV, torrential rain droplet erosion, 10^8 high-cycle alternating aerodynamic fatigue cycles.",
        "primary_recommendation": "Continuous Carbon Fiber Prepreg (CFRP Prepreg) or Carbon Fiber Reinforced PETG (PETG-CF)",
        "technical_rationale": (
            "Wind turbine blades operate as rotating cantilever aerodynamic beams. Under extreme wind gusts, the spar cap "
            "must resist excessive flapwise tip deflection to avoid catastrophic tower strike, while surviving millions of "
            "alternating cyclic loads. Unreinforced PLA is strictly disqualified due to environmental creep, brittle cyclic "
            "fatigue propagation, and rapid moisture plasticization. CFRP Prepreg offers the premier specific modulus (85 GPa, "
            "1.55 g/cm^3) and infinite fatigue endurance limit, while PETG-CF offers an accessible decentralized FDM alternative "
            "for rural microgrids in developing regions."
        ),
        "manufacturing_directives": "Vacuum-assisted resin transfer molding (VARTM) or FDM spanwise X-Y orientation with 100% root infill."
    },
    {
        "user_query": "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight.",
        "component": "Submerged Hydrokinetic River Turbine Blade / Impeller",
        "ashby_index": "Beam Bending Strength under Hydrodynamic Thrust (M = σ_y^(2/3) / ρ)",
        "environmental_factors": "Continuous freshwater submersion, suspended river silt abrasion, biological biofilm adhesion.",
        "primary_recommendation": "Carbon Fiber Reinforced PETG (PETG-CF)",
        "technical_rationale": (
            "Submerged hydro-turbines experience sustained hydrodynamic thrust bending and cyclical vortex shedding. "
            "Virgin PLA undergoes rapid hydrolytic ester cleavage in freshwater, suffering an empirical 28.4% drop in tensile strength "
            "and 7.2% reduction in modulus within 30 days of water saturation. PETG offers hydrophobic chemical resistance "
            "with zero hydrolytic degradation. Chopped carbon fiber reinforcement elevates flexural modulus from 2.1 GPa to 6.05 GPa, "
            "suppressing hydrodynamic tip flutter and raising fatigue endurance limit to 36.0 MPa."
        ),
        "manufacturing_directives": "Mandatory hardened steel nozzle (0.4-0.6mm); post-process with 2-part self-leveling epoxy resin (XTC-3D protocol) to eliminate raw FDM surface roughness (Ra < 1.2 μm) and recover 11.4% aerodynamic/hydrodynamic drag penalty."
    },
    {
        "user_query": "I need a material for a high-performance CPU heat sink to dissipate 200W of heat as fast as possible.",
        "component": "Electronic Heatsink & Heat Spreader",
        "ashby_index": "Solid Thermal Conduction (M = λ)",
        "environmental_factors": "Continuous elevated temperature (60°C to 95°C), zero moisture.",
        "primary_recommendation": "Pure Copper (Copper_C11000) or Aluminium Alloy (Aluminium_6061_T6)",
        "technical_rationale": (
            "Heat dissipation from concentrated semiconductor dies is governed by Fourier's law of thermal conduction "
            "(q = -λ * grad(T)). Polymers (λ = 0.15 - 0.35 W/mK) act as thermal insulators and are completely unviable. "
            "Pure Copper provides elite thermal conductivity (λ = 390 W/mK) for localized heat spreading, while Aluminium 6061-T6 "
            "(λ = 167 W/mK) provides the optimal thermal performance per unit mass (λ / ρ) for fin arrays."
        ),
        "manufacturing_directives": "CNC high-speed milling from forged billet or skived fin extrusion."
    },
    {
        "user_query": "I need a biocompatible material for an orthopedic hip joint implant that won't corrode in body fluids.",
        "component": "Orthopedic Hip Stem / Joint Prosthesis",
        "ashby_index": "Biocompatible Specific Bending Strength (M = σ_y / ρ) and Biocompatibility (ISO 10993)",
        "environmental_factors": "Physiological saline solution (0.9% NaCl), million-cycle gait fatigue, osseointegration interface.",
        "primary_recommendation": "Titanium Alloy (Titanium_Ti6Al4V) or Medical-Grade PEEK",
        "technical_rationale": (
            "Orthopedic implants demand certified biological inertness (ASTM F136), zero cytotoxic metal ion release, "
            "and an elastic modulus closely matched to cortical bone (E_bone ≈ 18 GPa) to prevent stress shielding and bone resorption. "
            "Titanium Ti-6Al-4V forms a passivated TiO2 layer immune to physiological chloride attack, offering high fatigue "
            "endurance limit (510 MPa). Medical-grade PEEK offers radiolucency and Young's modulus (3.8 GPa) ideal for spinal cages."
        ),
        "manufacturing_directives": "Selective Laser Melting (SLM / DMLS) additive manufacturing or 5-axis CNC machining under ISO 13485 cleanroom conditions."
    }
]

def main():
    target_path = os.path.join("data", "instruction_tuning_dataset.jsonl")
    with open(target_path, "w", encoding="utf-8") as f:
        for sample in SAMPLE_PAIRS:
            entry = {
                "instruction": INSTRUCTION_PROMPT,
                "input": sample["user_query"],
                "output": (
                    f"### Component Identification: {sample['component']}\n"
                    f"### Governing Ashby Index: {sample['ashby_index']}\n"
                    f"### Environmental & Boundary Conditions: {sample['environmental_factors']}\n"
                    f"### Primary Material Recommendation: {sample['primary_recommendation']}\n\n"
                    f"### Detailed Engineering Rationale:\n{sample['technical_rationale']}\n\n"
                    f"### Manufacturing & Processing Directives:\n{sample['manufacturing_directives']}"
                )
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"Generated instruction-tuning dataset with {len(SAMPLE_PAIRS)} multi-turn pairs at: {target_path}")

if __name__ == "__main__":
    main()
