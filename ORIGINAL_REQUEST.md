# Original User Request

## 2026-09-17T15:22:27Z

Deploy an autonomous multi-agent stress-testing and auditing team to subject the universal material selection system to 100 diverse, challenging engineering questions across all major physical domains, verify that answers are computed from Michael Ashby optimization physics rather than hardcoded pattern-matching, investigate every identified deficiency, and apply comprehensive fixes to the codebase.

Working directory: c:/Users/jeffm/Desktop/university projects/Material selection LLM
Integrity mode: benchmark

## Requirements

### R1. Comprehensive 100-Question Multi-Domain Stress Test Suite
Generate a comprehensive suite of 100 distinct, non-trivial engineering prompts spanning all mechanical loading modes (bending beams, tensile ties, shell plates, rotational rotors, elastic dampers, cutting tools, thermal conductors/insulators, pressure vessels) across diverse operating environments (submerged freshwater/marine, solar UV, cryogenic temperatures, extreme furnace heat up to 1100°C, corrosive chemical/acids, high vacuum) and special regulatory constraints (ISO 10993 biomedical implants, FDA food contact, optical transparency, ultra-lightweight racing, heavy crane hoisting, rural micro-grids).

### R2. Anti-Hardcoding & Physics Integrity Audit
Subject all 100 outputs to rigorous materials science evaluation. The auditing agent must verify:
- The governing Ashby performance index (M) mathematically matches the load geometry (e.g. beam vs tie vs plate vs rotor vs thermal).
- The top material satisfies all thermal deflection limits (T_service < HDT for polymers), environmental degradation constraints (e.g. PLA hydrolysis penalty in water, ABS UV embrittlement), and regulatory filters (no toxic aluminium in vivo, no loose carbon fiber in food, no opaque materials for optics).
- Results are derived from dynamic physical property equations in src/ashby_engine.py and src/materials_db.py, not brittle hardcoded string matches.

### R3. Autonomous Root-Cause Investigation & Codebase Remediation
For any prompt where the system fails, chooses an unphysical material, selects the wrong Ashby formula, or fails to extract implicit engineering constraints:
- Trace the root cause into src/nlp_parser.py, src/ashby_engine.py, src/materials_db.py, or src/llm_orchestrator.py.
- Apply permanent, principled engineering fixes without breaking any existing capstone benchmarks (river turbine blade => PETG-CF, hardened steel nozzle, 28.4% PLA degradation citation, epoxy smoothing protocol).

### R4. Complete Test Verification
Ensure all 56 existing automated regression tests plus the new 100-question audit suite execute with a 100% pass rate.
