"""
Ingestion & Enrichment Pipeline for 1,600+ Engineering Materials Catalog.
Downloads standardized materials data (ANSI, ISO, DIN, JIS, BS, NF, CSN, GOST),
normalizes SI units, categorizes material families, assigns thermal, environmental,
machinability, cost, and supply chain / sourcing parameters (MOQ, EOQ, Lead Times).
"""

import os
import csv
import json
import io
import urllib.request
from typing import Dict, Any, List

def build_materials_catalog():
    print("Fetching standard engineering materials database from literature repository...")
    url = "https://raw.githubusercontent.com/purushottamnawale/material-selection-using-machine-learning/master/Data.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    raw_csv = urllib.request.urlopen(req, timeout=30.0).read().decode("utf-8")
    
    reader = csv.DictReader(io.StringIO(raw_csv))
    rows = list(reader)
    print(f"Loaded {len(rows)} raw material records.")
    
    catalog: Dict[str, Dict[str, Any]] = {}
    
    # Process each record
    for idx, row in enumerate(rows):
        mat_raw = row.get("Material", "").strip()
        if not mat_raw:
            continue
        std = row.get("Std", "").strip()
        heat_treat = row.get("Heat treatment", "").strip()
        
        # Parse numerical properties
        def safe_float(val, default=0.0):
            try:
                v = float(str(val).strip())
                return v if v > 0 else default
            except (ValueError, TypeError):
                return default

        su_mpa = safe_float(row.get("Su"), 400.0)      # Ultimate tensile strength (MPa)
        sy_mpa = safe_float(row.get("Sy"), 250.0)      # Yield strength (MPa)
        e_mpa = safe_float(row.get("E"), 200000.0)     # Young's modulus (MPa)
        g_mpa = safe_float(row.get("G"), 78000.0)      # Shear modulus (MPa)
        mu = safe_float(row.get("mu"), 0.3)            # Poisson's ratio
        rho = safe_float(row.get("Ro"), 7850.0)        # Density (kg/m^3)
        elongation = safe_float(row.get("A5"), 15.0)   # Elongation (%)
        hardness_bhn = safe_float(row.get("Bhn"), 150.0)

        # Convert E and G to GPa
        e_gpa = round(e_mpa / 1000.0, 2)
        g_gpa = round(g_mpa / 1000.0, 2)

        # Construct clean unique key & title
        name_parts = [std, mat_raw]
        if heat_treat and heat_treat.lower() != "none":
            name_parts.append(f"({heat_treat})")
        full_name = " ".join(name_parts)
        
        clean_key = f"{std}_{mat_raw}_{heat_treat}".replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "").replace("/", "_").replace(".", "_")
        clean_key = "".join([c for c in clean_key if c.isalnum() or c == "_"])
        while "__" in clean_key:
            clean_key = clean_key.replace("__", "_")
        clean_key = clean_key.strip("_")

        # Determine Material Family
        mat_lower = mat_raw.lower()
        if "steel" in mat_lower:
            if any(w in mat_lower for w in ["304", "316", "410", "430", "stainless", "inox"]):
                family = "Stainless Steel"
                k_therm = 16.0
                cost_kg = 5.2
                corrosion = "Excellent"
                machinability = 50.0 # % relative to 1212
                moq_kg = 50.0
                lead_days = 7
                source_cat = "Domestic Local Stock"
            elif any(w in mat_lower for w in ["4140", "4340", "8620", "alloy", "crmo", "ni"]):
                family = "Alloy Steel"
                k_therm = 42.0
                cost_kg = 3.5
                corrosion = "Fair"
                machinability = 65.0
                moq_kg = 100.0
                lead_days = 5
                source_cat = "Domestic Local Stock"
            elif any(w in mat_lower for w in ["tool", "d2", "o1", "a2", "m2", "h13", "skd"]):
                family = "Tool Steel"
                k_therm = 25.0
                cost_kg = 8.5
                corrosion = "Moderate"
                machinability = 40.0
                moq_kg = 25.0
                lead_days = 14
                source_cat = "Regional Distribution"
            else:
                family = "Carbon Steel"
                k_therm = 50.0
                cost_kg = 1.8
                corrosion = "Poor"
                machinability = 75.0
                moq_kg = 200.0
                lead_days = 3
                source_cat = "Domestic Local Stock"
        elif "aluminum" in mat_lower or "aluminium" in mat_lower:
            family = "Aluminum Alloy"
            k_therm = 167.0
            cost_kg = 4.8
            corrosion = "Good"
            machinability = 90.0
            moq_kg = 50.0
            lead_days = 4
            source_cat = "Domestic Local Stock"
        elif any(w in mat_lower for w in ["copper", "brass", "bronze", "muntz", "cartridge"]):
            family = "Copper & Brass Alloys"
            k_therm = 115.0 if ("brass" in mat_lower or "bronze" in mat_lower) else 385.0
            cost_kg = 9.5
            corrosion = "Very Good"
            machinability = 85.0
            moq_kg = 25.0
            lead_days = 7
            source_cat = "Domestic Local Stock"
        elif any(w in mat_lower for w in ["titanium", "ti6al4v", "ti-", "grade 5"]):
            family = "Titanium Alloy"
            k_therm = 7.2
            cost_kg = 45.0
            corrosion = "Superior"
            machinability = 25.0
            moq_kg = 10.0
            lead_days = 21
            source_cat = "Global Import"
        elif any(w in mat_lower for w in ["cast iron", "grey", "malleable", "nodular", "ductile"]):
            family = "Cast Iron & Ductile Iron"
            k_therm = 45.0
            cost_kg = 2.2
            corrosion = "Fair"
            machinability = 70.0
            moq_kg = 500.0
            lead_days = 10
            source_cat = "Domestic Local Stock"
        elif any(w in mat_lower for w in ["nickel", "inconel", "monel", "hastelloy"]):
            family = "Nickel Superalloy"
            k_therm = 11.4
            cost_kg = 55.0
            corrosion = "Exceptional"
            machinability = 20.0
            moq_kg = 20.0
            lead_days = 35
            source_cat = "Global Import"
        elif "magnesium" in mat_lower:
            family = "Magnesium Alloy"
            k_therm = 96.0
            cost_kg = 6.8
            corrosion = "Moderate"
            machinability = 95.0
            moq_kg = 50.0
            lead_days = 18
            source_cat = "Regional Distribution"
        else:
            family = "Specialty Structural Metal"
            k_therm = 30.0
            cost_kg = 6.0
            corrosion = "Good"
            machinability = 55.0
            moq_kg = 50.0
            lead_days = 14
            source_cat = "Regional Distribution"

        # Max operating temperature estimate
        if "aluminum" in family.lower() or "magnesium" in family.lower():
            t_max_c = 180.0
        elif "titanium" in family.lower():
            t_max_c = 420.0
        elif "nickel" in family.lower():
            t_max_c = 750.0
        elif "stainless" in family.lower():
            t_max_c = 550.0
        else:
            t_max_c = 350.0

        catalog[clean_key] = {
            "name": full_name,
            "standard": std,
            "grade": mat_raw,
            "heat_treatment": heat_treat if heat_treat else "None",
            "family": family,
            "density": rho,
            "youngs_modulus_iso": e_gpa,
            "youngs_modulus_print_xy": e_gpa,
            "youngs_modulus_print_z": e_gpa,
            "shear_modulus_gpa": g_gpa,
            "poissons_ratio": mu,
            "yield_strength": sy_mpa,
            "ultimate_tensile_strength": su_mpa,
            "tensile_strength_z": sy_mpa,
            "flexural_modulus": e_gpa,
            "flexural_strength": sy_mpa * 1.3,
            "elongation_at_break": elongation,
            "brinell_hardness": hardness_bhn,
            "impact_strength_izod": round(sy_mpa * 0.12, 1),
            "fatigue_strength_limit": round(su_mpa * 0.45, 1),
            "max_service_temp_c": t_max_c,
            "thermal_conductivity": k_therm,
            "specific_heat_capacity": 480.0 if "steel" in family.lower() else (900.0 if "aluminum" in family.lower() else 520.0),
            "thermal_expansion_coefficient": 12.0 if "steel" in family.lower() else 23.0,
            "water_absorption_24h": 0.0,
            "water_saturation_tensile_drop": 0.0,
            "water_saturation_modulus_drop": 0.0,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": corrosion,
            "chemical_resistance": "Good",
            "fdm_printability": {
                "ease_of_printing": "Not FDM Printable",
                "nozzle_temperature_min": 0,
                "nozzle_temperature_max": 0,
                "bed_temperature_min": 0,
                "bed_temperature_max": 0,
                "chamber_temperature_recommended": 0,
                "enclosure_required": False,
                "print_speed_mm_s": 0,
                "cooling_fan_percent": 0,
                "warping_risk": "N/A (Metals require DMLS/SLM or CNC Machining)"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": cost_kg,
                "sourcing_category": source_cat,
                "minimum_order_quantity_kg": moq_kg,
                "typical_lead_time_days": lead_days,
                "machinability_rating_percent": machinability,
                "weldability": "Good" if "carbon" in family.lower() or "stainless" in family.lower() else "Fair",
                "quality_consistency_rating": 98.0,
                "eoq_setup_cost_usd": 150.0 if source_cat == "Domestic Local Stock" else 550.0,
                "annual_holding_cost_rate": 0.20
            }
        }

    print(f"Standard metals processed: {len(catalog)} materials.")

    # Now add our curated high-performance Polymers, Advanced Composites, Technical Ceramics, and 3D printing filaments
    specialty_materials = {
        "PLA_Pro": {
            "name": "Polylactic Acid Pro (PLA+)",
            "standard": "ISO 527",
            "grade": "PLA Plus Filaments",
            "heat_treatment": "None",
            "family": "Engineering Thermoplastic (Biodegradable)",
            "density": 1240.0,
            "youngs_modulus_iso": 3.5,
            "youngs_modulus_print_xy": 3.4,
            "youngs_modulus_print_z": 2.6,
            "shear_modulus_gpa": 1.3,
            "poissons_ratio": 0.36,
            "yield_strength": 55.0,
            "ultimate_tensile_strength": 60.0,
            "tensile_strength_z": 32.0,
            "flexural_modulus": 3.8,
            "flexural_strength": 85.0,
            "elongation_at_break": 6.0,
            "brinell_hardness": 18.0,
            "impact_strength_izod": 3.2,
            "fatigue_strength_limit": 18.0,
            "max_service_temp_c": 52.0,
            "thermal_conductivity": 0.13,
            "specific_heat_capacity": 1800.0,
            "thermal_expansion_coefficient": 68.0,
            "water_absorption_24h": 0.35,
            "water_saturation_tensile_drop": 28.4,
            "water_saturation_modulus_drop": 7.2,
            "uv_resistance": "Poor",
            "hydrolysis_resistance": "Poor",
            "corrosion_resistance": "Good",
            "chemical_resistance": "Fair",
            "fdm_printability": {
                "ease_of_printing": "Excellent",
                "nozzle_temperature_min": 190,
                "nozzle_temperature_max": 220,
                "bed_temperature_min": 45,
                "bed_temperature_max": 60,
                "chamber_temperature_recommended": 25,
                "enclosure_required": False,
                "print_speed_mm_s": 80,
                "cooling_fan_percent": 100,
                "warping_risk": "Very Low"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 20.0,
                "sourcing_category": "Domestic Local Stock",
                "minimum_order_quantity_kg": 1.0,
                "typical_lead_time_days": 1,
                "machinability_rating_percent": 80.0,
                "weldability": "Poor (Solvent/Thermal only)",
                "quality_consistency_rating": 99.0,
                "eoq_setup_cost_usd": 25.0,
                "annual_holding_cost_rate": 0.15
            }
        },
        "PETG_Engineering": {
            "name": "Polyethylene Terephthalate Glycol (PETG)",
            "standard": "ISO 527",
            "grade": "Engineering Co-Polyester",
            "heat_treatment": "None",
            "family": "Engineering Thermoplastic",
            "density": 1270.0,
            "youngs_modulus_iso": 2.1,
            "youngs_modulus_print_xy": 2.05,
            "youngs_modulus_print_z": 1.85,
            "shear_modulus_gpa": 0.77,
            "poissons_ratio": 0.38,
            "yield_strength": 45.0,
            "ultimate_tensile_strength": 50.0,
            "tensile_strength_z": 36.0,
            "flexural_modulus": 2.15,
            "flexural_strength": 70.0,
            "elongation_at_break": 18.0,
            "brinell_hardness": 16.0,
            "impact_strength_izod": 6.8,
            "fatigue_strength_limit": 22.0,
            "max_service_temp_c": 70.0,
            "thermal_conductivity": 0.19,
            "specific_heat_capacity": 1300.0,
            "thermal_expansion_coefficient": 60.0,
            "water_absorption_24h": 0.12,
            "water_saturation_tensile_drop": 5.1,
            "water_saturation_modulus_drop": 2.8,
            "uv_resistance": "Moderate",
            "hydrolysis_resistance": "Good",
            "corrosion_resistance": "Excellent",
            "chemical_resistance": "Good",
            "fdm_printability": {
                "ease_of_printing": "Good",
                "nozzle_temperature_min": 230,
                "nozzle_temperature_max": 250,
                "bed_temperature_min": 75,
                "bed_temperature_max": 90,
                "chamber_temperature_recommended": 30,
                "enclosure_required": False,
                "print_speed_mm_s": 50,
                "cooling_fan_percent": 40,
                "warping_risk": "Low"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 24.0,
                "sourcing_category": "Domestic Local Stock",
                "minimum_order_quantity_kg": 1.0,
                "typical_lead_time_days": 1,
                "machinability_rating_percent": 85.0,
                "weldability": "Moderate",
                "quality_consistency_rating": 98.0,
                "eoq_setup_cost_usd": 25.0,
                "annual_holding_cost_rate": 0.15
            }
        },
        "PETG_CF_Reinforced": {
            "name": "PETG Carbon Fiber Reinforced (PETG-CF 15%)",
            "standard": "ISO 527",
            "grade": "15% Chopped Carbon Fiber",
            "heat_treatment": "None",
            "family": "Short-Fiber Reinforced Polymer",
            "density": 1320.0,
            "youngs_modulus_iso": 7.2,
            "youngs_modulus_print_xy": 6.8,
            "youngs_modulus_print_z": 2.9,
            "shear_modulus_gpa": 2.5,
            "poissons_ratio": 0.35,
            "yield_strength": 62.0,
            "ultimate_tensile_strength": 68.0,
            "tensile_strength_z": 38.0,
            "flexural_modulus": 6.9,
            "flexural_strength": 105.0,
            "elongation_at_break": 3.8,
            "brinell_hardness": 22.0,
            "impact_strength_izod": 7.5,
            "fatigue_strength_limit": 32.0,
            "max_service_temp_c": 78.0,
            "thermal_conductivity": 0.32,
            "specific_heat_capacity": 1250.0,
            "thermal_expansion_coefficient": 25.0,
            "water_absorption_24h": 0.08,
            "water_saturation_tensile_drop": 3.2,
            "water_saturation_modulus_drop": 1.5,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Good",
            "fdm_printability": {
                "ease_of_printing": "Good",
                "nozzle_temperature_min": 240,
                "nozzle_temperature_max": 260,
                "bed_temperature_min": 80,
                "bed_temperature_max": 90,
                "chamber_temperature_recommended": 35,
                "enclosure_required": False,
                "print_speed_mm_s": 50,
                "cooling_fan_percent": 30,
                "warping_risk": "Very Low (Carbon fibers reduce shrinkage)"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 48.0,
                "sourcing_category": "Domestic Local Stock",
                "minimum_order_quantity_kg": 1.0,
                "typical_lead_time_days": 2,
                "machinability_rating_percent": 70.0,
                "weldability": "Fair",
                "quality_consistency_rating": 97.0,
                "eoq_setup_cost_usd": 35.0,
                "annual_holding_cost_rate": 0.18
            }
        },
        "PEEK_Optima": {
            "name": "Polyether Ether Ketone (PEEK)",
            "standard": "ASTM D638",
            "grade": "Unfilled Medical/Aerospace Grade",
            "heat_treatment": "Annealed 200C",
            "family": "High-Performance Semi-Crystalline Polymer",
            "density": 1300.0,
            "youngs_modulus_iso": 4.1,
            "youngs_modulus_print_xy": 3.9,
            "youngs_modulus_print_z": 3.2,
            "shear_modulus_gpa": 1.5,
            "poissons_ratio": 0.38,
            "yield_strength": 100.0,
            "ultimate_tensile_strength": 105.0,
            "tensile_strength_z": 75.0,
            "flexural_modulus": 4.0,
            "flexural_strength": 165.0,
            "elongation_at_break": 45.0,
            "brinell_hardness": 28.0,
            "impact_strength_izod": 8.0,
            "fatigue_strength_limit": 60.0,
            "max_service_temp_c": 250.0,
            "thermal_conductivity": 0.25,
            "specific_heat_capacity": 1340.0,
            "thermal_expansion_coefficient": 45.0,
            "water_absorption_24h": 0.05,
            "water_saturation_tensile_drop": 0.5,
            "water_saturation_modulus_drop": 0.2,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Exceptional",
            "fdm_printability": {
                "ease_of_printing": "Difficult",
                "nozzle_temperature_min": 390,
                "nozzle_temperature_max": 430,
                "bed_temperature_min": 130,
                "bed_temperature_max": 160,
                "chamber_temperature_recommended": 90,
                "enclosure_required": True,
                "print_speed_mm_s": 25,
                "cooling_fan_percent": 0,
                "warping_risk": "High"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 185.0,
                "sourcing_category": "Regional Distribution",
                "minimum_order_quantity_kg": 1.0,
                "typical_lead_time_days": 10,
                "machinability_rating_percent": 75.0,
                "weldability": "Good (Ultrasonic/Laser)",
                "quality_consistency_rating": 99.5,
                "eoq_setup_cost_usd": 85.0,
                "annual_holding_cost_rate": 0.22
            }
        },
        "CFRP_Autoclave_T700": {
            "name": "Carbon Fiber Reinforced Polymer (Toray T700 / Epoxy Prepreg)",
            "standard": "ASTM D3039",
            "grade": "Quasi-Isotropic [0/45/90]s Prepreg",
            "heat_treatment": "Autoclave Cured 180C 6bar",
            "family": "Continuous Fiber Composite",
            "density": 1550.0,
            "youngs_modulus_iso": 70.0,
            "youngs_modulus_print_xy": 70.0,
            "youngs_modulus_print_z": 9.5,
            "shear_modulus_gpa": 26.0,
            "poissons_ratio": 0.30,
            "yield_strength": 600.0,
            "ultimate_tensile_strength": 820.0,
            "tensile_strength_z": 50.0,
            "flexural_modulus": 65.0,
            "flexural_strength": 950.0,
            "elongation_at_break": 1.4,
            "brinell_hardness": 45.0,
            "impact_strength_izod": 65.0,
            "fatigue_strength_limit": 480.0,
            "max_service_temp_c": 140.0,
            "thermal_conductivity": 5.0,
            "specific_heat_capacity": 1000.0,
            "thermal_expansion_coefficient": 2.0,
            "water_absorption_24h": 0.10,
            "water_saturation_tensile_drop": 4.0,
            "water_saturation_modulus_drop": 2.0,
            "uv_resistance": "Good (with UV clearcoat)",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Exceptional",
            "fdm_printability": {
                "ease_of_printing": "Not FDM Printable",
                "nozzle_temperature_min": 0,
                "nozzle_temperature_max": 0,
                "bed_temperature_min": 0,
                "bed_temperature_max": 0,
                "chamber_temperature_recommended": 0,
                "enclosure_required": False,
                "print_speed_mm_s": 0,
                "cooling_fan_percent": 0,
                "warping_risk": "N/A (Autoclave Tooling)"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 95.0,
                "sourcing_category": "Global Import",
                "minimum_order_quantity_kg": 25.0,
                "typical_lead_time_days": 28,
                "machinability_rating_percent": 30.0, # Requires diamond tooling
                "weldability": "Bonded Adhesive Only",
                "quality_consistency_rating": 99.0,
                "eoq_setup_cost_usd": 650.0,
                "annual_holding_cost_rate": 0.25
            }
        },
        "Alumina_Ceramic_99": {
            "name": "Technical Alumina Ceramic (Al2O3 99.5%)",
            "standard": "ASTM C1161",
            "grade": "Sintered Technical Ceramic",
            "heat_treatment": "Sintered 1650C",
            "family": "Technical Ceramic",
            "density": 3920.0,
            "youngs_modulus_iso": 375.0,
            "youngs_modulus_print_xy": 375.0,
            "youngs_modulus_print_z": 375.0,
            "shear_modulus_gpa": 152.0,
            "poissons_ratio": 0.22,
            "yield_strength": 310.0, # Flexural / Compressive strength > 2500 MPa
            "ultimate_tensile_strength": 310.0,
            "tensile_strength_z": 310.0,
            "flexural_modulus": 375.0,
            "flexural_strength": 380.0,
            "elongation_at_break": 0.1,
            "brinell_hardness": 1450.0, # Vickers ~1600 HV
            "impact_strength_izod": 2.5,
            "fatigue_strength_limit": 180.0,
            "max_service_temp_c": 1600.0,
            "thermal_conductivity": 32.0,
            "specific_heat_capacity": 880.0,
            "thermal_expansion_coefficient": 8.0,
            "water_absorption_24h": 0.0,
            "water_saturation_tensile_drop": 0.0,
            "water_saturation_modulus_drop": 0.0,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Exceptional",
            "fdm_printability": {
                "ease_of_printing": "Not FDM Printable",
                "nozzle_temperature_min": 0,
                "nozzle_temperature_max": 0,
                "bed_temperature_min": 0,
                "bed_temperature_max": 0,
                "chamber_temperature_recommended": 0,
                "enclosure_required": False,
                "print_speed_mm_s": 0,
                "cooling_fan_percent": 0,
                "warping_risk": "N/A (Sintered)"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 38.0,
                "sourcing_category": "Regional Distribution",
                "minimum_order_quantity_kg": 10.0,
                "typical_lead_time_days": 21,
                "machinability_rating_percent": 5.0, # Requires diamond grinding
                "weldability": "Glass/Ceramic Brazing Only",
                "quality_consistency_rating": 99.8,
                "eoq_setup_cost_usd": 250.0,
                "annual_holding_cost_rate": 0.18
            }
        },
        "Silicon_Carbide_SiC": {
            "name": "Reaction Bonded Silicon Carbide (SiC)",
            "standard": "ASTM C1161",
            "grade": "Ceramic Armor & Seal Rings",
            "heat_treatment": "Reaction Sintered",
            "family": "Technical Ceramic",
            "density": 3100.0,
            "youngs_modulus_iso": 410.0,
            "youngs_modulus_print_xy": 410.0,
            "youngs_modulus_print_z": 410.0,
            "shear_modulus_gpa": 175.0,
            "poissons_ratio": 0.17,
            "yield_strength": 450.0,
            "ultimate_tensile_strength": 450.0,
            "tensile_strength_z": 450.0,
            "flexural_modulus": 410.0,
            "flexural_strength": 480.0,
            "elongation_at_break": 0.1,
            "brinell_hardness": 2200.0,
            "impact_strength_izod": 3.0,
            "fatigue_strength_limit": 250.0,
            "max_service_temp_c": 1380.0,
            "thermal_conductivity": 120.0,
            "specific_heat_capacity": 670.0,
            "thermal_expansion_coefficient": 4.0,
            "water_absorption_24h": 0.0,
            "water_saturation_tensile_drop": 0.0,
            "water_saturation_modulus_drop": 0.0,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Exceptional",
            "fdm_printability": {
                "ease_of_printing": "Not FDM Printable",
                "nozzle_temperature_min": 0,
                "nozzle_temperature_max": 0,
                "bed_temperature_min": 0,
                "bed_temperature_max": 0,
                "chamber_temperature_recommended": 0,
                "enclosure_required": False,
                "print_speed_mm_s": 0,
                "cooling_fan_percent": 0,
                "warping_risk": "N/A"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 75.0,
                "sourcing_category": "Global Import",
                "minimum_order_quantity_kg": 5.0,
                "typical_lead_time_days": 30,
                "machinability_rating_percent": 2.0,
                "weldability": "None",
                "quality_consistency_rating": 99.9,
                "eoq_setup_cost_usd": 400.0,
                "annual_holding_cost_rate": 0.20
            }
        },
        "Inconel_718_Superalloy": {
            "name": "Nickel Superalloy Inconel 718 (AMS 5662 / N07718)",
            "standard": "AMS 5662",
            "grade": "Precipitation Hardened Aerospace Superalloy",
            "heat_treatment": "Solution Heat Treated & Aged",
            "family": "Nickel Superalloy",
            "density": 8190.0,
            "youngs_modulus_iso": 211.0,
            "youngs_modulus_print_xy": 211.0,
            "youngs_modulus_print_z": 211.0,
            "shear_modulus_gpa": 80.0,
            "poissons_ratio": 0.29,
            "yield_strength": 1100.0,
            "ultimate_tensile_strength": 1375.0,
            "tensile_strength_z": 1100.0,
            "flexural_modulus": 211.0,
            "flexural_strength": 1400.0,
            "elongation_at_break": 18.0,
            "brinell_hardness": 360.0,
            "impact_strength_izod": 48.0,
            "fatigue_strength_limit": 600.0,
            "max_service_temp_c": 700.0,
            "thermal_conductivity": 11.4,
            "specific_heat_capacity": 435.0,
            "thermal_expansion_coefficient": 13.0,
            "water_absorption_24h": 0.0,
            "water_saturation_tensile_drop": 0.0,
            "water_saturation_modulus_drop": 0.0,
            "uv_resistance": "Superior",
            "hydrolysis_resistance": "Superior",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Exceptional",
            "fdm_printability": {
                "ease_of_printing": "Not FDM Printable",
                "nozzle_temperature_min": 0,
                "nozzle_temperature_max": 0,
                "bed_temperature_min": 0,
                "bed_temperature_max": 0,
                "chamber_temperature_recommended": 0,
                "enclosure_required": False,
                "print_speed_mm_s": 0,
                "cooling_fan_percent": 0,
                "warping_risk": "N/A"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 65.0,
                "sourcing_category": "Global Import",
                "minimum_order_quantity_kg": 25.0,
                "typical_lead_time_days": 45,
                "machinability_rating_percent": 18.0, # Highly abrasive / work-hardening
                "weldability": "Very Good (EBW, TIG)",
                "quality_consistency_rating": 99.7,
                "eoq_setup_cost_usd": 650.0,
                "annual_holding_cost_rate": 0.22
            }
        },
        "Polycarbonate_Optical": {
            "name": "Polycarbonate Clear Optical Grade (PC Lexan)",
            "standard": "ISO 527",
            "grade": "Optical Transparency Extrusion/Sheet",
            "heat_treatment": "Stress Relieved",
            "family": "Transparent Optical Polymer",
            "density": 1200.0,
            "youngs_modulus_iso": 2.4,
            "youngs_modulus_print_xy": 2.3,
            "youngs_modulus_print_z": 1.9,
            "shear_modulus_gpa": 0.86,
            "poissons_ratio": 0.39,
            "yield_strength": 65.0,
            "ultimate_tensile_strength": 70.0,
            "tensile_strength_z": 45.0,
            "flexural_modulus": 2.4,
            "flexural_strength": 95.0,
            "elongation_at_break": 110.0,
            "brinell_hardness": 20.0,
            "impact_strength_izod": 65.0, # Notched impact 65-75 kJ/m2 (extremely impact resistant)
            "fatigue_strength_limit": 25.0,
            "max_service_temp_c": 125.0,
            "thermal_conductivity": 0.20,
            "specific_heat_capacity": 1200.0,
            "thermal_expansion_coefficient": 65.0,
            "water_absorption_24h": 0.15,
            "water_saturation_tensile_drop": 2.0,
            "water_saturation_modulus_drop": 1.0,
            "uv_resistance": "Very Good (UV Stabilized)",
            "hydrolysis_resistance": "Good",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Fair",
            "fdm_printability": {
                "ease_of_printing": "Moderate",
                "nozzle_temperature_min": 260,
                "nozzle_temperature_max": 290,
                "bed_temperature_min": 105,
                "bed_temperature_max": 120,
                "chamber_temperature_recommended": 70,
                "enclosure_required": True,
                "print_speed_mm_s": 40,
                "cooling_fan_percent": 15,
                "warping_risk": "Moderate to High"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 18.0,
                "sourcing_category": "Domestic Local Stock",
                "minimum_order_quantity_kg": 5.0,
                "typical_lead_time_days": 3,
                "machinability_rating_percent": 85.0,
                "weldability": "Solvent / Ultrasonic",
                "quality_consistency_rating": 99.0,
                "eoq_setup_cost_usd": 50.0,
                "annual_holding_cost_rate": 0.18
            }
        },
        "TPU_Elastomer_95A": {
            "name": "Thermoplastic Polyurethane 95A (TPU)",
            "standard": "ISO 37",
            "grade": "Elastomeric Flex Shore 95A",
            "heat_treatment": "None",
            "family": "Thermoplastic Elastomer",
            "density": 1210.0,
            "youngs_modulus_iso": 0.15,
            "youngs_modulus_print_xy": 0.14,
            "youngs_modulus_print_z": 0.12,
            "shear_modulus_gpa": 0.05,
            "poissons_ratio": 0.48,
            "yield_strength": 18.0,
            "ultimate_tensile_strength": 35.0,
            "tensile_strength_z": 28.0,
            "flexural_modulus": 0.16,
            "flexural_strength": 22.0,
            "elongation_at_break": 550.0,
            "brinell_hardness": 10.0,
            "impact_strength_izod": 999.0, # No break
            "fatigue_strength_limit": 15.0,
            "max_service_temp_c": 80.0,
            "thermal_conductivity": 0.22,
            "specific_heat_capacity": 1500.0,
            "thermal_expansion_coefficient": 150.0,
            "water_absorption_24h": 0.40,
            "water_saturation_tensile_drop": 5.0,
            "water_saturation_modulus_drop": 3.0,
            "uv_resistance": "Good",
            "hydrolysis_resistance": "Good",
            "corrosion_resistance": "Exceptional",
            "chemical_resistance": "Good",
            "fdm_printability": {
                "ease_of_printing": "Moderate",
                "nozzle_temperature_min": 210,
                "nozzle_temperature_max": 230,
                "bed_temperature_min": 40,
                "bed_temperature_max": 60,
                "chamber_temperature_recommended": 25,
                "enclosure_required": False,
                "print_speed_mm_s": 25,
                "cooling_fan_percent": 100,
                "warping_risk": "Very Low"
            },
            "techno_economics": {
                "raw_cost_usd_per_kg": 32.0,
                "sourcing_category": "Domestic Local Stock",
                "minimum_order_quantity_kg": 1.0,
                "typical_lead_time_days": 2,
                "machinability_rating_percent": 20.0,
                "weldability": "Thermal",
                "quality_consistency_rating": 98.0,
                "eoq_setup_cost_usd": 30.0,
                "annual_holding_cost_rate": 0.16
            }
        }
    }

    catalog.update(specialty_materials)
    
    # Save to data/materials_catalog.json
    os.makedirs("data", exist_ok=True)
    catalog_path = os.path.join("data", "materials_catalog.json")
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)
        
    print(f"Successfully generated master materials catalog with {len(catalog)} materials at {catalog_path}.")

if __name__ == "__main__":
    build_materials_catalog()
