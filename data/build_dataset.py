"""
Generates the comprehensive engineering intent and constraint training dataset.
Contains 250+ diverse mechanical engineering design prompts spanning:
1. Automotive aerodynamics (spoilers, splitters, wings, diffusers)
2. Renewable energy (wind turbine blades, hydrokinetic rotors, solar cookers)
3. Aerospace & drones (airframes, drone arms, satellite brackets)
4. Structural members (cantilever beams, architectural trusses, crane hooks)
5. Pure tension cables (suspension cables, tethers, elevator ropes)
6. Pressure containment (hydrogen tanks, autoclaves, air receivers, water pipes)
7. Thermal systems (CPU heatsinks, cryogenic dewars, furnace refractories, rocket nozzles)
8. Tribology & kinematics (gears, bushings, bearings)
9. Biomedical & implants (hip joints, bone plates, dental copings)
10. Consumer & protective gear (phone cases, shoes, flexible bumpers)
11. Cutting tools (knives, chisels, saws, shredder blades)
12. Optical components (safety visors, sight glasses, drone domes)
"""

import json
import os

DATASET = [
    # 1. Automotive Aerodynamics (Spoilers, Wings, Splitters, Diffusers)
    {
        "prompt": "I want to create a spoiler for a car",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "I need a rear spoiler wing for a sports car to provide downforce",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "car spoiler",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "I want to make a car spoiler that is strong and lightweight",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "lightweight aerodynamic rear wing for a race car to generate downforce at high speed",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "front splitter for track car bumper to prevent high-speed lift",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "rear diffuser fins for sports car underbody aerodynamics",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "aerodynamic trunk lid lip spoiler for highway driving efficiency",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "carbon fiber look car rear wing that will sit in direct sunlight without warping",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "aerodynamic canards and dive planes for motorsport front fascia",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "GT3 racing wing blade with endplates subjected to 300 kg downforce at 200 km/h",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "ducktail trunk spoiler for sports coupe exterior tuning",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "active aerodynamic rear wing flap adjusting angle under braking",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "aftermarket car spoiler for sedan boot lid",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "automotive exterior wing mounted on rear hatch to reduce wake turbulence",
        "component_classification": "automotive_aerodynamic_wing_or_spoiler",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 2. Wind Turbine Blades & Renewable Energy
    {
        "prompt": "I need to make blades for a wind turbine",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "small residential wind turbine rotor blades that withstand wind gusts without hitting the tower",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "wind turbine blade that operates in outdoor rain and sun with cyclic fatigue resistance",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "fatigue_efficiency",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "horizontal axis wind turbine aerofoil blade for rural microgrid in Kenya",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "vertical axis wind turbine Savonius scoop blade",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "plate_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "wind turbine blade spar cap resisting millions of wind bending cycles",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "fatigue_efficiency",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "blades for a wind generator to provide power off grid",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "aerodynamic blade for 5kW wind turbine with high lift-to-drag ratio",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "wind power rotor blade surviving desert UV and dust storms",
        "component_classification": "wind_turbine_blade",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 3. Hydrokinetic Turbines & Marine Rotors (River Benchmark)
    {
        "prompt": "I want to make a blade that will push water, carry a heavy load, and sit in a river all day, but I don't know the exact weight.",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "underwater hydrokinetic turbine runner blade submerged in muddy river current",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "submerged propeller blade for a boat operating in saltwater",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "water wheel paddle submerged in irrigation canal in rural Kenya",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "centrifugal water pump impeller rotating in hot industrial wastewater",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "flywheel_inertia",
        "outdoor_uv": False, "submerged_water": True, "high_temp": True, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "cross-flow hydro turbine runner blades placed in high-velocity waterfall",
        "component_classification": "turbine_blade_or_impeller",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 4. Bicycle Frames & Lightweight Chassis
    {
        "prompt": "I want to design a lightweight and stiff bicycle frame that won't flex under heavy rider pedaling.",
        "component_classification": "bicycle_frame_or_chassis",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "bicycle frame for mountain biking over rough rocky terrain with shock loads",
        "component_classification": "bicycle_frame_or_chassis",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "lightweight road racing bike down-tube and bottom bracket shell",
        "component_classification": "bicycle_frame_or_chassis",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "cargo e-bike heavy duty frame to transport 150 kg luggage",
        "component_classification": "bicycle_frame_or_chassis",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "quadcopter drone arm frame that holds high thrust motors without vibrating",
        "component_classification": "aerospace_airframe_or_drone",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "carbon drone arms resisting motor torsional vibration during acrobatic flight",
        "component_classification": "aerospace_airframe_or_drone",
        "governing_ashby_index": "beam_stiffness",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 5. Thermal Management & Heat Sinks
    {
        "prompt": "I need a material for a high-performance CPU heat sink to dissipate 200W of heat as fast as possible.",
        "component_classification": "thermal_heat_sink",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "LED stadium floodlight cooling heatsink fins to prevent thermal degradation",
        "component_classification": "thermal_heat_sink",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": True, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "solar inverter cooling radiator block in hot Garissa desert Kenya",
        "component_classification": "thermal_heat_sink",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": True, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "cooling jacket heat exchanger for chemical plant carrying hydrochloric acid",
        "component_classification": "thermal_heat_sink",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "electric vehicle battery pack cooling cold plate plate to extract heat during rapid charging",
        "component_classification": "thermal_heat_sink",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 6. Extreme Heat, Rocket Nozzles & Furnaces
    {
        "prompt": "I need a material for an exhaust nozzle operating under continuous 700 C heat and mechanical stress.",
        "component_classification": "high_temperature_nozzle",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "combustion chamber nozzle throat withstanding 1200 C supersonic gas erosion",
        "component_classification": "high_temperature_nozzle",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "ceramic kiln wall insulation lining to stop heat loss at 1000 C",
        "component_classification": "thermal_insulator_or_refractory",
        "governing_ashby_index": "thermal_insulation",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "battery thermal runaway fireproof barrier plate resisting 800 C torch without conducting electricity",
        "component_classification": "thermal_insulator_or_refractory",
        "governing_ashby_index": "thermal_insulation",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "cryogenic liquid helium dewar neck insulation tube to prevent boiloff at 4 Kelvin",
        "component_classification": "thermal_insulator_or_refractory",
        "governing_ashby_index": "thermal_insulation",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": True,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 7. Pressure Vessels, Tanks & Containment
    {
        "prompt": "700 bar compressed hydrogen storage tank cylinder for fuel cell electric car",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "deep sea submersible external pressure hull resisting 600 bar hydrostatic crushing at 6000m depth",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "workshop compressed air receiver tank holding 10 bar without bursting",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "chemical reactor autoclave chamber operating at 250 C and 50 bar steam",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "lightweight reusable sports water bottle for hiking and drinking",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": True, "cutting": False, "optical": False
    },
    {
        "prompt": "municipal drinking water conduit pipe buried underground",
        "component_classification": "pressure_vessel_or_tank",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": True, "cutting": False, "optical": False
    },

    # 8. Pure Tension Ties & Cables
    {
        "prompt": "suspension bridge vertical hanger cable holding heavy vehicular deck weight",
        "component_classification": "pure_tension_member",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "deep water oil rig tension leg tether holding floating platform to sea floor",
        "component_classification": "pure_tension_member",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "bicycle wheel tension spoke wire resisting high rotational cyclic pull",
        "component_classification": "pure_tension_member",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "high altitude weather balloon mooring tether requiring minimal weight per meter",
        "component_classification": "pure_tension_member",
        "governing_ashby_index": "tie_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 9. High-Speed Rotors & Flywheels
    {
        "prompt": "high-speed kinetic energy storage flywheel spinning at 60,000 RPM",
        "component_classification": "high_speed_rotor_or_flywheel",
        "governing_ashby_index": "flywheel_inertia",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "dental drill micro-turbine spinning at 400,000 rpm sterilized in autoclave",
        "component_classification": "high_speed_rotor_or_flywheel",
        "governing_ashby_index": "flywheel_inertia",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": True, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "turbocharger compressor wheel impeller resisting centrifugal hoop burst at 150,000 RPM",
        "component_classification": "high_speed_rotor_or_flywheel",
        "governing_ashby_index": "flywheel_inertia",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 10. Elastic Springs & Compliant Dampers
    {
        "prompt": "I want to make a shock-absorbing smartphone case that will survive high drops without cracking.",
        "component_classification": "protective_case_or_cushion",
        "governing_ashby_index": "elastic_energy",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "running shoe midsole cushion foam that absorbs heel strike impact without bottoming out",
        "component_classification": "protective_case_or_cushion",
        "governing_ashby_index": "elastic_energy",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "marine dock piling fender bumper absorbing ferry boat impact kinetic energy",
        "component_classification": "protective_case_or_cushion",
        "governing_ashby_index": "elastic_energy",
        "outdoor_uv": True, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "coil spring for automotive suspension absorbing road bumps",
        "component_classification": "elastic_spring_or_damper",
        "governing_ashby_index": "elastic_energy",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "micro-flexure hinge for precision optical mirror alignment",
        "component_classification": "elastic_spring_or_damper",
        "governing_ashby_index": "elastic_energy",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 11. Industrial Cutting Tools & Knives
    {
        "prompt": "sugarcane cutting machete blade for smallholder farmers in western Kenya",
        "component_classification": "cutting_tool_or_blade",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": True, "optical": False
    },
    {
        "prompt": "food processing butcher knife in commercial poultry abattoir steam washdown",
        "component_classification": "cutting_tool_or_blade",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": True, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": True, "cutting": True, "optical": False
    },
    {
        "prompt": "glass scoring scribe wheel to scratch soda-lime glass sheets without dulling",
        "component_classification": "cutting_tool_or_blade",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": True, "optical": False
    },
    {
        "prompt": "woodworking planer blade cutting through kiln-dried tropical hardwood",
        "component_classification": "cutting_tool_or_blade",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": True, "optical": False
    },
    {
        "prompt": "plastic recycling granulator shredder blade chopping dirty bottles",
        "component_classification": "cutting_tool_or_blade",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": True, "optical": False
    },

    # 12. Biomedical & Orthopedic Implants
    {
        "prompt": "I need a biocompatible material for an orthopedic hip joint implant that won't corrode in body fluids.",
        "component_classification": "biocompatible_orthopedic_implant",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": True, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "spinal fusion interbody cage supporting lumbar vertebrae with bone ingrowth",
        "component_classification": "biocompatible_orthopedic_implant",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": True, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "bone fracture fixation plate screwed to human femur bone",
        "component_classification": "biocompatible_orthopedic_implant",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": True, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "dental crown coping withstand chewing forces without leaching ions into mouth",
        "component_classification": "biocompatible_orthopedic_implant",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": False, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": True, "food_safe": True, "cutting": False, "optical": False
    },

    # 13. Heavy Lifting & Structural Beams
    {
        "prompt": "I need a material for a heavy-duty crane lifting hook that must lift 10 tons without brittle fracture.",
        "component_classification": "heavy_duty_lifting_hook",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "forklift heavy duty steel carriage fork tines lifting palletized shipping containers",
        "component_classification": "heavy_duty_lifting_hook",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "building roof support cantilever beam carrying snow and wind load",
        "component_classification": "structural_cantilever_beam",
        "governing_ashby_index": "beam_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },

    # 14. Tribology, Gears & Bushings
    {
        "prompt": "I need a low-friction, wear-resistant material for high-speed transmission gears with smooth sliding.",
        "component_classification": "low_friction_wear_gear",
        "governing_ashby_index": "fatigue_efficiency",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": False
    },
    {
        "prompt": "dry running sliding bushing sleeve bearing inside food packaging machine with zero grease contamination",
        "component_classification": "low_friction_wear_gear",
        "governing_ashby_index": "fatigue_efficiency",
        "outdoor_uv": False, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": True, "cutting": False, "optical": False
    },

    # 15. Culinary Cookware
    {
        "prompt": "kitchen non-stick cooking frying pan base that heats up uniformly without scorching food",
        "component_classification": "culinary_cookware",
        "governing_ashby_index": "thermal_conductivity",
        "outdoor_uv": False, "submerged_water": False, "high_temp": True, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": True, "cutting": False, "optical": False
    },

    # 16. Optical Transparency & Windows
    {
        "prompt": "transparent safety visor face shield protecting workers from flying high-velocity fragments",
        "component_classification": "optical_window_or_shield",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": True, "submerged_water": False, "high_temp": False, "cryogenic": False,
        "chemical": False, "biomedical": False, "food_safe": False, "cutting": False, "optical": True
    },
    {
        "prompt": "underwater camera transparent optical dome port resisting ocean pressure at 100 meters depth",
        "component_classification": "optical_window_or_shield",
        "governing_ashby_index": "plate_strength",
        "outdoor_uv": True, "submerged_water": True, "high_temp": False, "cryogenic": False,
        "chemical": True, "biomedical": False, "food_safe": False, "cutting": False, "optical": True
    }
]

def augment_dataset(base_data):
    from collections import defaultdict
    by_class = defaultdict(list)
    for item in base_data:
        by_class[item["component_classification"]].append(item)

    prefixes = [
        "What is the best material for a ",
        "Recommend an optimal material to build a ",
        "I need to fabricate a ",
        "How do I choose a material for a ",
        "I want to make a ",
        "Looking for a material for a "
    ]

    augmented = []
    # For each class, ensure at least 18-20 balanced samples
    target_per_class = 20
    for comp_class, items in by_class.items():
        class_samples = list(items)
        idx = 0
        while len(class_samples) < target_per_class and idx < len(items) * len(prefixes):
            base_item = items[idx % len(items)]
            p = base_item["prompt"]
            prefix = prefixes[(idx // len(items)) % len(prefixes)]
            # Clean prompt
            clean_p = p.lower()
            for starter in ["i want to make a ", "i want to create a ", "i need a material for a ", "i need a material for an ", "i need to make "]:
                if clean_p.startswith(starter):
                    clean_p = clean_p[len(starter):]
                    break
            new_p = prefix + clean_p
            new_item = dict(base_item)
            new_item["prompt"] = new_p
            class_samples.append(new_item)
            idx += 1
        augmented.extend(class_samples)
    return augmented

def main():
    target_path = os.path.join("data", "engineering_intent_dataset.json")
    full_dataset = augment_dataset(DATASET)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(full_dataset, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(full_dataset)} training samples in '{target_path}'.")

if __name__ == "__main__":
    main()
