"""
Techno-Economic & Supply Chain Optimization Engine for Engineering Material Selection.

Mathematical Formulations & Peer-Reviewed Literature Foundations:
1. Kraljic Portfolio Matrix (Kraljic, 1983) - Supply Risk vs. Financial Impact classification.
2. Incoterms 2020 Landed Cost Mechanics (ICC, 2020; Stopford, 2009) - EXW, FOB, CIF, DDP multi-stage accumulation.
3. Stochastic Delivery Lead Times & Lead-Time Variance (Silver, Pyke & Peterson, 1998) - DDLT convolution & safety stock.
4. Wilson-Harris Economic Order Quantity (EOQ) with Quantity Discounts and MOQ Gating (Harris, 1913; Wilson, 1934; Hadley & Whitin, 1963).
5. Multi-Criteria Decision Analysis (MCDA) via TOPSIS (Hwang & Yoon, 1981) - Synthesizing Ashby technical performance with landed economics.

Academic Citations:
- Ashby, M. F. (2011). Materials Selection in Mechanical Design (4th ed.). Butterworth-Heinemann.
- Harris, F. W. (1913). How Many Parts to Make at Once. The Magazine of Management, 10(2), 135-136, 152.
- Wilson, R. H. (1934). A Scientific Routine for Stock Control. Harvard Business Review, 13(1), 116-128.
- Hadley, G., & Whitin, T. M. (1963). Analysis of Inventory Systems. Prentice-Hall.
- Kraljic, P. (1983). Purchasing Must Become Supply Management. Harvard Business Review, 61(5), 109-117.
- Silver, E. A., Pyke, D. F., & Peterson, R. (1998). Inventory Management and Production Planning and Scheduling (3rd ed.). John Wiley & Sons.
- Hwang, C. L., & Yoon, K. (1981). Multiple Attribute Decision Making: Methods and Applications. Springer-Verlag.
- Stopford, M. (2009). Maritime Economics (3rd ed.). Routledge.
- International Chamber of Commerce (ICC). (2020). Incoterms 2020: ICC Rules for the Use of Domestic and International Trade Terms. ICC Pub. No. 723E.
"""

import math
from typing import Dict, Any, List, Optional, Tuple


class EconomicsEngine:
    """
    Evaluates raw material procurement economics, import logistics, MOQ constraints,
    EOQ batch sizing, lead-time variance, Kraljic portfolio risk, and Hwang-Yoon TOPSIS rankings.
    """

    DEFAULT_ANNUAL_DEMAND_KG: float = 1000.0  # Standard engineering baseline annual requirement
    DEFAULT_HOLDING_RATE: float = 0.22         # 22% annual inventory carrying charge (cost of capital + storage + obsolescence)
    DEFAULT_SERVICE_LEVEL_Z: float = 1.645     # 95% cycle service level quantile (Z_alpha)

    # Geographic Sourcing Origins to Nairobi/Mombasa Industrial Hub
    ORIGIN_PARAMETERS: Dict[str, Dict[str, Any]] = {
        "Domestic East Africa": {
            "origin_name": "Domestic East Africa (Nairobi/Mombasa Stock)",
            "primary_mode": "Domestic Road Freight / SGR Rail",
            "lead_time_mean_days": 3.0,
            "lead_time_std_days": 1.0,
            "origin_risk_factor": 0.05,
            "local_availability_index": 0.95,
            "substitutability_index": 0.85,
            "origin_handling_usd_kg": 0.00,
            "ocean_freight_usd_kg": 0.00,
            "air_freight_usd_kg": 1.50,
            "eac_cet_tariff_rate": 0.00,
            "setup_cost_usd": 120.0
        },
        "Regional Africa": {
            "origin_name": "Regional Africa (South Africa Hub / Durban)",
            "primary_mode": "Coastal Feeder Vessel / Cross-Border Trucking",
            "lead_time_mean_days": 18.0,
            "lead_time_std_days": 4.0,
            "origin_risk_factor": 0.25,
            "local_availability_index": 0.65,
            "substitutability_index": 0.70,
            "origin_handling_usd_kg": 0.12,
            "ocean_freight_usd_kg": 0.14,
            "air_freight_usd_kg": 4.50,
            "eac_cet_tariff_rate": 0.00,  # AfCFTA/COMESA preferential regime
            "setup_cost_usd": 280.0
        },
        "Asian Manufacturing Hubs": {
            "origin_name": "Asian Manufacturing Hubs (China / India / Japan)",
            "primary_mode": "Deep-Sea Container Shipping (Mombasa Port)",
            "lead_time_mean_days": 35.0,
            "lead_time_std_days": 8.0,
            "origin_risk_factor": 0.40,
            "local_availability_index": 0.45,
            "substitutability_index": 0.60,
            "origin_handling_usd_kg": 0.18,
            "ocean_freight_usd_kg": 0.22,
            "air_freight_usd_kg": 7.50,
            "eac_cet_tariff_rate": 0.10,  # EAC CET Band 2 intermediate raw stock
            "setup_cost_usd": 550.0
        },
        "European Specialty Mills": {
            "origin_name": "European Specialty Mills (Germany / UK / Sweden)",
            "primary_mode": "Maritime Liner (Rotterdam/Hamburg -> Mombasa)",
            "lead_time_mean_days": 45.0,
            "lead_time_std_days": 12.0,
            "origin_risk_factor": 0.35,
            "local_availability_index": 0.25,
            "substitutability_index": 0.35,
            "origin_handling_usd_kg": 0.22,
            "ocean_freight_usd_kg": 0.32,
            "air_freight_usd_kg": 9.00,
            "eac_cet_tariff_rate": 0.10,
            "setup_cost_usd": 680.0
        },
        "North American Aerospace Stock": {
            "origin_name": "North American Aerospace Stock (USA)",
            "primary_mode": "Transatlantic Liner / Intermodal Sea-Freight",
            "lead_time_mean_days": 55.0,
            "lead_time_std_days": 14.0,
            "origin_risk_factor": 0.30,
            "local_availability_index": 0.15,
            "substitutability_index": 0.25,
            "origin_handling_usd_kg": 0.25,
            "ocean_freight_usd_kg": 0.42,
            "air_freight_usd_kg": 11.50,
            "eac_cet_tariff_rate": 0.10,
            "setup_cost_usd": 750.0
        }
    }

    # Backward compatibility mapping for legacy category strings
    LEGACY_CATEGORY_MAP: Dict[str, str] = {
        "Domestic Local Stock": "Domestic East Africa",
        "Regional Distribution": "Regional Africa",
        "Global Import": "Asian Manufacturing Hubs"
    }

    # East African Community (EAC) Statutory Customs Fees
    EAC_IDF_RATE: float = 0.025   # Import Declaration Fee (2.5% of CIF)
    EAC_RDL_RATE: float = 0.020   # Railway Development Levy (2.0% of CIF)
    KENYA_VAT_RATE: float = 0.16  # Value Added Tax (16.0%)
    MARINE_INSURANCE_RATE: float = 0.0040  # 0.40% ad valorem on 110% CIF (Institute Cargo Clauses A)
    PORT_HANDLING_USD_KG: float = 0.08     # Mombasa port wharfage and terminal handling
    INLAND_FREIGHT_MOMBASA_NAIROBI_USD_KG: float = 0.10  # SGR rail freight / bonded trucking
    CLEARING_BROKERAGE_USD_KG: float = 0.05             # KRA Kentrade clearance documentation

    # Maximum Allowable Material Shelf Life before Microstructural / Chemical Degradation (Years)
    # Beyond this horizon, forced MOQ storage causes matrix oxidation, hydrolysis, or alloy embrittlement
    SHELF_LIFE_YEARS: Dict[str, float] = {
        "Continuous Fiber Composite": 0.5,           # 6 months (requires -18°C cold chain freezer)
        "Short Fiber Reinforced Polymer Composite": 2.0,  # 2 years (hygroscopic moisture saturation)
        "Thermoplastic Polymer": 2.5,                # 2.5 years (UV and hydrolytic chain scission)
        "Thermoplastic Copolymer": 2.5,
        "Thermoplastic Terpolymer": 2.5,
        "High-Performance Thermoplastic": 2.0,
        "Low-Alloy Steel": 5.0,                      # 5 years (surface corrosion under protective oiling)
        "Carbon Steel": 5.0,
        "Cast Iron": 5.0,
        "Stainless Steel": 10.0,
        "Titanium Alloy": 10.0,
        "Nickel Superalloy": 10.0,
        "Technical Ceramic": 15.0
    }

    @classmethod
    def resolve_origin(cls, sourcing_category: str) -> str:
        """Resolve legacy or alternative sourcing category names into standard origin keys."""
        if sourcing_category in cls.ORIGIN_PARAMETERS:
            return sourcing_category
        return cls.LEGACY_CATEGORY_MAP.get(sourcing_category, "Asian Manufacturing Hubs")

    @classmethod
    def calculate_landed_cost(
        cls,
        exw_cost_usd_kg: float,
        origin_category: str = "Asian Manufacturing Hubs",
        use_air_freight: bool = False,
        custom_tariff_rate: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculate multi-stage Incoterms 2020 Landed Cost (Stopford, 2009; ICC, 2020)
        from Ex Works (EXW) to Delivered Duty Paid (DDP) at Nairobi industrial facility.

        Incoterms 2020 Boundary Equations:
          C_FOB = C_EXW + c_origin_handling
          C_CIF = C_FOB + F_main + C_insurance
          C_DDP = C_CIF + T_customs + C_port + C_inland + C_brokerage
        """
        origin_key = cls.resolve_origin(origin_category)
        params = cls.ORIGIN_PARAMETERS[origin_key]

        c_exw = max(0.1, float(exw_cost_usd_kg))

        # Domestic delivery skips international maritime legs and import duties
        if origin_key == "Domestic East Africa":
            c_fob = c_exw
            c_cif = c_exw
            t_duty = 0.0
            t_idf = 0.0
            t_rdl = 0.0
            t_vat = c_exw * cls.KENYA_VAT_RATE
            c_port = 0.0
            c_inland = 0.15  # local cartage within Nairobi/Mombasa
            c_brokerage = 0.0
            c_ddp = c_exw + t_vat + c_inland
            return {
                "origin_key": origin_key,
                "origin_name": params["origin_name"],
                "incoterm_exw_usd_kg": round(c_exw, 3),
                "incoterm_fob_usd_kg": round(c_fob, 3),
                "incoterm_cif_usd_kg": round(c_cif, 3),
                "incoterm_ddp_usd_kg": round(c_ddp, 3),
                "main_freight_usd_kg": 0.0,
                "insurance_usd_kg": 0.0,
                "eac_duty_usd_kg": 0.0,
                "eac_idf_usd_kg": 0.0,
                "eac_rdl_usd_kg": 0.0,
                "vat_usd_kg": round(t_vat, 3),
                "port_handling_usd_kg": 0.0,
                "inland_freight_usd_kg": round(c_inland, 3),
                "brokerage_usd_kg": 0.0,
                "landed_cost_multiplier": round(c_ddp / c_exw, 3)
            }

        # International Procurement Chain
        c_origin_handling = params["origin_handling_usd_kg"]
        c_fob = c_exw + c_origin_handling

        # Freight mode selection (Ocean Liner vs Air Freight Expedite)
        f_main = params["air_freight_usd_kg"] if use_air_freight else params["ocean_freight_usd_kg"]

        # Marine Cargo Insurance (Institute Cargo Clauses A: 110% CIF coverage)
        c_ins = cls.MARINE_INSURANCE_RATE * 1.10 * (c_fob + f_main)
        c_cif = c_fob + f_main + c_ins

        # Customs Duty (EAC Common External Tariff)
        duty_rate = custom_tariff_rate if custom_tariff_rate is not None else params["eac_cet_tariff_rate"]
        t_duty = duty_rate * c_cif
        t_idf = cls.EAC_IDF_RATE * c_cif
        t_rdl = cls.EAC_RDL_RATE * c_cif

        # VAT calculation base: CIF + Duty + IDF + RDL
        tax_base = c_cif + t_duty + t_idf + t_rdl
        t_vat = cls.KENYA_VAT_RATE * tax_base

        # Port handling, SGR inland freight, and clearance brokerage
        c_port = cls.PORT_HANDLING_USD_KG
        c_inland = cls.INLAND_FREIGHT_MOMBASA_NAIROBI_USD_KG
        c_brokerage = cls.CLEARING_BROKERAGE_USD_KG

        # Total Delivered Duty Paid (DDP) Landed Cost
        c_ddp = c_cif + t_duty + t_idf + t_rdl + t_vat + c_port + c_inland + c_brokerage

        return {
            "origin_key": origin_key,
            "origin_name": params["origin_name"],
            "incoterm_exw_usd_kg": round(c_exw, 3),
            "incoterm_fob_usd_kg": round(c_fob, 3),
            "incoterm_cif_usd_kg": round(c_cif, 3),
            "incoterm_ddp_usd_kg": round(c_ddp, 3),
            "main_freight_usd_kg": round(f_main, 3),
            "insurance_usd_kg": round(c_ins, 4),
            "eac_duty_usd_kg": round(t_duty, 3),
            "eac_idf_usd_kg": round(t_idf, 3),
            "eac_rdl_usd_kg": round(t_rdl, 3),
            "vat_usd_kg": round(t_vat, 3),
            "port_handling_usd_kg": round(c_port, 3),
            "inland_freight_usd_kg": round(c_inland, 3),
            "brokerage_usd_kg": round(c_brokerage, 3),
            "landed_cost_multiplier": round(c_ddp / c_exw, 3)
        }

    @classmethod
    def calculate_stochastic_lead_time_and_safety_stock(
        cls,
        annual_demand_kg: float,
        origin_category: str = "Asian Manufacturing Hubs",
        holding_rate: float = DEFAULT_HOLDING_RATE,
        unit_landed_cost_usd_kg: float = 10.0,
        service_level_z: float = DEFAULT_SERVICE_LEVEL_Z,
        daily_demand_std_pct: float = 0.20
    ) -> Dict[str, Any]:
        """
        Model delivery lead times as stochastic random variables and convolve
        with demand volatility using Silver, Pyke & Peterson (1998):

          E[DDLT] = d * mu_L
          sigma_DDLT = sqrt(mu_L * sigma_d^2 + d^2 * sigma_L^2)
          Safety Stock (SS) = Z_alpha * sigma_DDLT
          Reorder Point (ROP) = d * mu_L + SS
        """
        origin_key = cls.resolve_origin(origin_category)
        params = cls.ORIGIN_PARAMETERS[origin_key]

        mu_L = float(params["lead_time_mean_days"])
        sigma_L = float(params["lead_time_std_days"])
        cv_L = sigma_L / mu_L if mu_L > 0 else 0.0

        daily_demand = max(annual_demand_kg, 1.0) / 365.0
        sigma_d = daily_demand * daily_demand_std_pct

        # Silver-Pyke-Peterson Convolution Theorem
        sigma_ddlt = math.sqrt((mu_L * (sigma_d ** 2)) + ((daily_demand ** 2) * (sigma_L ** 2)))
        safety_stock_kg = service_level_z * sigma_ddlt
        expected_ddlt_kg = daily_demand * mu_L
        reorder_point_kg = expected_ddlt_kg + safety_stock_kg

        # Inventory carrying cost for safety stock buffer
        h_unit = holding_rate * max(0.5, unit_landed_cost_usd_kg)
        annual_safety_stock_holding_cost = safety_stock_kg * h_unit

        return {
            "origin_key": origin_key,
            "lead_time_mean_days": mu_L,
            "lead_time_std_days": sigma_L,
            "coefficient_of_variation_cv_l": round(cv_L, 3),
            "daily_demand_mean_kg": round(daily_demand, 3),
            "daily_demand_std_kg": round(sigma_d, 3),
            "expected_ddlt_kg": round(expected_ddlt_kg, 2),
            "sigma_ddlt_kg": round(sigma_ddlt, 2),
            "safety_stock_kg": round(safety_stock_kg, 2),
            "reorder_point_kg": round(reorder_point_kg, 2),
            "annual_safety_stock_holding_cost_usd": round(annual_safety_stock_holding_cost, 2),
            "service_level_pct": 95.0 if abs(service_level_z - 1.645) < 0.05 else round(99.0, 1)
        }

    @classmethod
    def calculate_eoq(
        cls,
        annual_demand_kg: float,
        cost_per_kg_usd: float,
        sourcing_category: str = "Domestic East Africa",
        custom_setup_cost: Optional[float] = None,
        holding_rate: float = DEFAULT_HOLDING_RATE,
        moq_kg: float = 0.0,
        quantity_discount_tiers: Optional[List[Tuple[float, float]]] = None
    ) -> Dict[str, Any]:
        """
        Wilson-Harris Economic Order Quantity (EOQ) with Quantity Discounts,
        Minimum Order Quantity (MOQ) gating, and Small-Lot Penalties.

        Formulations (Harris, 1913; Wilson, 1934; Hadley & Whitin, 1963):
          EOQ_raw = sqrt((2 * D * S) / H)
          Q_eff = max(EOQ_raw, Q_MOQ)
          TC(Q) = D * C_L + (D / Q) * S + (Q / 2) * H
          Delta_TC_MOQ = TC(Q_eff) - TC(EOQ_raw)
        """
        origin_key = cls.resolve_origin(sourcing_category)
        D = max(annual_demand_kg, 1.0)
        c_base = max(cost_per_kg_usd, 0.5)
        S = custom_setup_cost if custom_setup_cost is not None else cls.ORIGIN_PARAMETERS[origin_key]["setup_cost_usd"]

        # Default standard quantity discount schedule if none provided
        # Format: [(min_qty, discount_fraction)]
        tiers = quantity_discount_tiers or [
            (0.0, 0.00),       # Baseline price
            (100.0, 0.05),     # 5% discount for orders >= 100 kg
            (500.0, 0.12),     # 12% discount for orders >= 500 kg
            (2000.0, 0.20)     # 20% discount for orders >= 2000 kg (industrial mill batch)
        ]

        best_q = None
        best_tc = float("inf")
        best_price = c_base
        best_tier_idx = 0

        # Evaluate each quantity discount tier (Hadley & Whitin, 1963)
        for idx, (tier_min_q, discount_pct) in enumerate(tiers):
            tier_price = c_base * (1.0 - discount_pct)
            tier_H = tier_price * holding_rate

            # Unconstrained optimal order for this tier
            q_unconstrained = math.sqrt((2.0 * D * S) / tier_H)

            # Feasibility gating: must be at least tier threshold and meet MOQ
            q_candidate = max(q_unconstrained, tier_min_q, moq_kg)

            # Check next tier upper bound
            next_tier_min = tiers[idx + 1][0] if idx + 1 < len(tiers) else float("inf")
            if q_candidate >= next_tier_min:
                continue

            tc = (D * tier_price) + ((D / q_candidate) * S) + ((q_candidate / 2.0) * tier_H)
            if tc < best_tc:
                best_tc = tc
                best_q = q_candidate
                best_price = tier_price
                best_tier_idx = idx

        # Calculate theoretical baseline unconstrained Wilson-Harris EOQ at nominal price
        H_nominal = c_base * holding_rate
        eoq_raw = math.sqrt((2.0 * D * S) / H_nominal)
        tc_raw = (D * c_base) + ((D / eoq_raw) * S) + ((eoq_raw / 2.0) * H_nominal)

        # MOQ Penalty and Horizon
        moq_penalty_usd = max(0.0, best_tc - tc_raw) if moq_kg > eoq_raw else 0.0
        excess_inventory_horizon_years = moq_kg / D if D > 0 else 0.0

        orders_per_year = D / best_q if best_q > 0 else 1.0
        cycle_time_days = 365.0 / orders_per_year if orders_per_year > 0 else 365.0
        annual_order_cost = orders_per_year * S
        annual_holding_cost = (best_q / 2.0) * (best_price * holding_rate)
        annual_material_cost = D * best_price

        # Stochastic lead-time and safety stock synthesis
        lt_stats = cls.calculate_stochastic_lead_time_and_safety_stock(
            annual_demand_kg=D,
            origin_category=origin_key,
            holding_rate=holding_rate,
            unit_landed_cost_usd_kg=best_price
        )

        total_annual_with_ss = best_tc + lt_stats["annual_safety_stock_holding_cost_usd"]

        return {
            "eoq_batch_size_kg": round(best_q, 1),
            "unconstrained_wilson_eoq_kg": round(eoq_raw, 1),
            "effective_order_quantity_kg": round(best_q, 1),
            "orders_per_year": round(orders_per_year, 1),
            "order_interval_days": round(cycle_time_days, 1),
            "annual_order_cost_usd": round(annual_order_cost, 2),
            "annual_holding_cost_usd": round(annual_holding_cost, 2),
            "annual_material_cost_usd": round(annual_material_cost, 2),
            "total_annual_procurement_cost_usd": round(best_tc, 2),
            "total_annual_with_safety_stock_usd": round(total_annual_with_ss, 2),
            "order_setup_cost_usd": S,
            "unit_holding_cost_per_kg_year": round(best_price * holding_rate, 2),
            "effective_unit_cost_usd_kg": round(best_price, 2),
            "moq_gating_applied": moq_kg > eoq_raw,
            "moq_penalty_annual_cost_usd": round(moq_penalty_usd, 2),
            "excess_inventory_horizon_years": round(excess_inventory_horizon_years, 2),
            "discount_tier_applied": best_tier_idx,
            "safety_stock": lt_stats
        }

    @classmethod
    def classify_kraljic_matrix(
        cls,
        annual_demand_kg: float,
        unit_landed_cost_usd_kg: float,
        origin_category: str = "Asian Manufacturing Hubs",
        engineering_criticality: float = 0.5,
        total_procurement_spend_budget: float = 50000.0
    ) -> Dict[str, Any]:
        """
        Classify candidate material into the Kraljic Portfolio Matrix (Kraljic, 1983).

        Coordinates:
          1. Financial / Profit Impact (FI in [0, 1])
          2. Supply Risk (SR in [0, 1])

        Quadrants:
          - Strategic: High Impact, High Risk
          - Bottleneck: Low Impact, High Risk
          - Leverage: High Impact, Low Risk
          - Routine: Low Impact, Low Risk
        """
        origin_key = cls.resolve_origin(origin_category)
        params = cls.ORIGIN_PARAMETERS[origin_key]

        spend = annual_demand_kg * unit_landed_cost_usd_kg
        spend_ratio = min(1.0, spend / max(1000.0, total_procurement_spend_budget))
        fi_score = (0.60 * spend_ratio) + (0.40 * min(1.0, max(0.0, engineering_criticality)))

        # Supply Risk composite
        r_origin = params["origin_risk_factor"]
        a_local = params["local_availability_index"]
        mu_L = params["lead_time_mean_days"]
        sigma_L = params["lead_time_std_days"]
        cv_L = min(1.0, sigma_L / mu_L if mu_L > 0 else 0.0)
        s_sub = params["substitutability_index"]

        sr_score = (0.25 * r_origin) + (0.30 * (1.0 - a_local)) + (0.25 * cv_L) + (0.20 * (1.0 - s_sub))

        fi_score = round(min(1.0, max(0.0, fi_score)), 3)
        sr_score = round(min(1.0, max(0.0, sr_score)), 3)

        # Quadrant threshold at (0.45, 0.40) calibrated for East African trade
        if fi_score >= 0.45 and sr_score >= 0.40:
            quadrant = "Strategic"
            strategy = "Strategic Partnership & Buffer Hedging: Long-term supply agreements (LTA), index pricing, dual-sourcing qualification."
        elif fi_score < 0.45 and sr_score >= 0.40:
            quadrant = "Bottleneck"
            strategy = "De-Risk & Standardization: Build safety stock buffer, redesign component to accept standard commercial alloys, negotiate consignment stock."
        elif fi_score >= 0.45 and sr_score < 0.40:
            quadrant = "Leverage"
            strategy = "Competitive Bidding & EOQ Maximization: Exploit buyer power, reverse auctions, quantity discount batching, spot sourcing."
        else:
            quadrant = "Routine"
            strategy = "Process Efficiency & Kanban: Automated replenishment, Vendor Managed Inventory (VMI), blanket POs, local off-the-shelf sourcing."

        return {
            "quadrant": quadrant,
            "profit_impact_coordinate": fi_score,
            "supply_risk_coordinate": sr_score,
            "strategic_policy": strategy,
            "origin_analyzed": params["origin_name"],
            "annual_material_spend_usd": round(spend, 2)
        }

    @classmethod
    def evaluate_material_economics(
        cls,
        material_data: Dict[str, Any],
        annual_demand_kg: float = DEFAULT_ANNUAL_DEMAND_KG,
        ashby_score: float = 1.0,
        engineering_criticality: float = 0.5
    ) -> Dict[str, Any]:
        """
        Synthesize complete supply chain, Incoterms 2020 landed cost, Kraljic risk,
        MOQ gating, Wilson-Harris EOQ, and Silver-Pyke-Peterson lead-time variance.
        """
        tech_econ = material_data.get("techno_economics", {})
        exw_cost = tech_econ.get("raw_cost_usd_per_kg") or material_data.get("cost_per_kg_usd", 6.0)

        # Detect sourcing origin from material properties
        kenya_avail = str(material_data.get("kenya_availability", "")).lower()
        if "very high" in kenya_avail or "widely stocked" in kenya_avail:
            source_cat = "Domestic East Africa"
        elif "high" in kenya_avail or "local distributor" in kenya_avail:
            source_cat = "Domestic East Africa"
        elif "moderate" in kenya_avail or "regional" in kenya_avail:
            source_cat = "Regional Africa"
        elif "low" in kenya_avail or "import" in kenya_avail:
            source_cat = tech_econ.get("sourcing_category") or "Asian Manufacturing Hubs"
        else:
            source_cat = tech_econ.get("sourcing_category") or "Asian Manufacturing Hubs"

        moq_kg = float(tech_econ.get("minimum_order_quantity_kg", 25.0))
        machinability = float(tech_econ.get("machinability_rating_percent", 60.0))
        weldability = str(tech_econ.get("weldability", "Good"))
        consistency = float(tech_econ.get("quality_consistency_rating", 98.0))

        # 1. Incoterms 2020 Landed Cost (EXW -> DDP Nairobi)
        landed_info = cls.calculate_landed_cost(
            exw_cost_usd_kg=exw_cost,
            origin_category=source_cat
        )
        landed_cost_usd_kg = landed_info["incoterm_ddp_usd_kg"]

        # 2. Kraljic Portfolio Classification (Kraljic, 1983)
        kraljic_info = cls.classify_kraljic_matrix(
            annual_demand_kg=annual_demand_kg,
            unit_landed_cost_usd_kg=landed_cost_usd_kg,
            origin_category=source_cat,
            engineering_criticality=engineering_criticality
        )

        # 3. Wilson-Harris EOQ with MOQ and Quantity Discounts (Harris 1913; Wilson 1934)
        eoq_data = cls.calculate_eoq(
            annual_demand_kg=annual_demand_kg,
            cost_per_kg_usd=landed_cost_usd_kg,
            sourcing_category=source_cat,
            moq_kg=moq_kg
        )

        # MOQ feasibility assessment
        moq_satisfied = annual_demand_kg >= moq_kg
        moq_surplus_kg = max(0.0, moq_kg - annual_demand_kg)
        moq_status = (
            "Optimal Batch (Demand >= MOQ)" if moq_satisfied
            else f"Small-Lot Penalty (Order surplus {moq_surplus_kg:.0f} kg to meet MOQ; {eoq_data['excess_inventory_horizon_years']:.1f} yr horizon)"
        )

        # Shelf-Life and Physical Feasibility Non-Compensatory Screening (Ashby 2011; Sen & Yang 1998)
        mat_family = str(material_data.get("family", "Engineering Material"))
        shelf_life_limit = cls.SHELF_LIFE_YEARS.get(mat_family, 3.0)
        eih = eoq_data["excess_inventory_horizon_years"]
        shelf_life_violation = eih > shelf_life_limit

        # Physical feasibility gating flag (from Ashby engine or prior boundary filter)
        is_physically_feasible = bool(material_data.get("is_feasible", True))
        disqualification_reasons = []
        if not is_physically_feasible:
            disqualification_reasons.append(material_data.get("infeasibility_reason", "Failed physical boundary constraints"))
        if shelf_life_violation:
            disqualification_reasons.append(
                f"Supply Chain Shelf-Life Expiry: MOQ ({moq_kg:.0f}kg) forces {eih:.1f} yr inventory, "
                f"exceeding {mat_family} degradation threshold ({shelf_life_limit:.1f} yrs)"
            )

        is_admissible = is_physically_feasible and not shelf_life_violation
        disqualification_reason_str = "; ".join(disqualification_reasons) if disqualification_reasons else None

        # Cost per unit volume (Ashby economic metric: M / (rho * C_L))
        rho = material_data.get("density", 7800.0)
        cost_per_unit_volume = (rho / 1000.0) * landed_cost_usd_kg  # USD per dm^3 (liter)
        performance_per_dollar = (ashby_score / cost_per_unit_volume) if cost_per_unit_volume > 0 else 0.0

        # Sub-scores (0 to 100 scale)
        score_cost = max(5.0, min(100.0, 100.0 - (landed_cost_usd_kg * 0.75)))
        score_avail = max(5.0, min(100.0, (1.0 - kraljic_info["supply_risk_coordinate"]) * 100.0))
        mean_lead = eoq_data["safety_stock"]["lead_time_mean_days"]
        score_lead = max(10.0, min(100.0, 100.0 - (mean_lead * 1.6)))
        score_mfg = (machinability * 0.6) + (consistency * 0.4)

        return {
            "raw_cost_usd_per_kg": exw_cost,
            "landed_cost_usd_per_kg": landed_cost_usd_kg,
            "cost_per_unit_volume_usd_liter": round(cost_per_unit_volume, 2),
            "performance_per_dollar_metric": round(performance_per_dollar, 3),
            "sourcing_category": source_cat,
            "minimum_order_quantity_kg": moq_kg,
            "moq_status": moq_status,
            "shelf_life_limit_years": shelf_life_limit,
            "shelf_life_violation": shelf_life_violation,
            "is_admissible": is_admissible,
            "disqualification_reason": disqualification_reason_str,
            "lead_time_days": mean_lead,
            "logistics_mode": cls.ORIGIN_PARAMETERS[cls.resolve_origin(source_cat)]["primary_mode"],
            "machinability_rating_percent": machinability,
            "weldability": weldability,
            "quality_consistency_percent": consistency,
            "eoq": eoq_data,
            "landed_cost_breakdown": landed_info,
            "kraljic_portfolio": kraljic_info,
            "safety_stock_analysis": eoq_data["safety_stock"],
            "sub_scores": {
                "cost_score": round(score_cost, 1),
                "availability_score": round(score_avail, 1),
                "lead_time_score": round(score_lead, 1),
                "manufacturability_score": round(score_mfg, 1)
            }
        }

    @classmethod
    def calculate_topsis_ranking(
        cls,
        candidate_evaluations: List[Dict[str, Any]],
        weights: Optional[Dict[str, float]] = None
    ) -> List[Dict[str, Any]]:
        """
        Multi-Criteria Decision Making (MCDM) via TOPSIS (Hwang & Yoon, 1981).
        Synthesizes 6 criteria:
          1. Technical Ashby Index (Benefit: max)
          2. Landed Unit Cost (Cost: min)
          3. Delivery Lead Time Mean (Cost: min)
          4. Delivery Lead Time Std Dev (Cost: min)
          5. MOQ Annual Penalty (Cost: min)
          6. Availability / Kraljic Security (Benefit: max)

        Equations:
          r_ij = x_ij / sqrt(sum_k x_kj^2)
          v_ij = w_j * r_ij
          S_i^+ = sqrt(sum_j (v_ij - v_j^+)^2)
          S_i^- = sqrt(sum_j (v_ij - v_j^-)^2)
          C_i^* = S_i^- / (S_i^+ + S_i^-)
        """
        if not candidate_evaluations:
            return []

        w = weights or {
            "tech": 0.35,      # Ashby performance index
            "cost": 0.25,      # Landed cost (USD/kg)
            "lead_mean": 0.15, # Expected lead time (days)
            "lead_std": 0.10,  # Lead-time variance/volatility (days)
            "moq_pen": 0.05,   # MOQ small-lot cost penalty (USD)
            "security": 0.10   # 1 - Kraljic supply risk
        }

        # Normalize weights to sum to 1.0
        total_w = sum(w.values())
        w_norm = {k: v / total_w for k, v in w.items()}

        m = len(candidate_evaluations)
        criteria_keys = ["tech", "cost", "lead_mean", "lead_std", "moq_pen", "security"]
        benefit_keys = {"tech", "security"}

        # Extract decision matrix X
        X: List[List[float]] = []
        for c in candidate_evaluations:
            econ = c["economics"]
            ss = econ["safety_stock_analysis"]
            km = econ["kraljic_portfolio"]
            eoq = econ["eoq"]

            row = [
                max(0.001, float(c.get("technical_ashby_score", 1.0))),
                max(0.1, float(econ["landed_cost_usd_per_kg"])),
                max(0.5, float(ss["lead_time_mean_days"])),
                max(0.1, float(ss["lead_time_std_days"])),
                max(0.0, float(eoq.get("moq_penalty_annual_cost_usd", 0.0))),
                max(0.01, float(1.0 - km["supply_risk_coordinate"]))
            ]
            X.append(row)

        # 1. Vector Normalization
        col_norms = []
        for j in range(len(criteria_keys)):
            col_sum_sq = sum(X[i][j] ** 2 for i in range(m))
            col_norms.append(math.sqrt(col_sum_sq) if col_sum_sq > 0 else 1.0)

        # 2. Weighted Normalized Matrix V
        V: List[List[float]] = []
        for i in range(m):
            v_row = []
            for j, crit in enumerate(criteria_keys):
                r_ij = X[i][j] / col_norms[j]
                v_ij = r_ij * w_norm[crit]
                v_row.append(v_ij)
            V.append(v_row)

        # 3. Determine Positive Ideal Solution (V+) and Negative Ideal Solution (V-)
        v_plus = []
        v_minus = []
        for j, crit in enumerate(criteria_keys):
            col_vals = [V[i][j] for i in range(m)]
            if crit in benefit_keys:
                v_plus.append(max(col_vals))
                v_minus.append(min(col_vals))
            else:
                v_plus.append(min(col_vals))
                v_minus.append(max(col_vals))

        # 4. Calculate Euclidean Distances and Relative Closeness C_i*
        for i in range(m):
            d_plus = math.sqrt(sum((V[i][j] - v_plus[j]) ** 2 for j in range(len(criteria_keys))))
            d_minus = math.sqrt(sum((V[i][j] - v_minus[j]) ** 2 for j in range(len(criteria_keys))))

            if (d_plus + d_minus) > 0:
                c_star = d_minus / (d_plus + d_minus)
            else:
                c_star = 0.5

            candidate_evaluations[i]["topsis_closeness_score"] = round(c_star, 4)
            # Synchronize composite score (0-100 scale) with TOPSIS relative closeness
            candidate_evaluations[i]["composite_score"] = round(c_star * 100.0, 1)

        return candidate_evaluations

    @classmethod
    def rank_candidates_techno_economic(
        cls,
        candidate_materials: List[Dict[str, Any]],
        annual_demand_kg: float = DEFAULT_ANNUAL_DEMAND_KG,
        w_tech: float = 0.35,
        w_cost: float = 0.25,
        w_avail: float = 0.15,
        w_lead: float = 0.15,
        w_mfg: float = 0.10
    ) -> List[Dict[str, Any]]:
        """
        Multi-Criteria Decision Analysis (MCDA) Ranking:
        Combines technical Ashby performance score with Incoterms landed economics,
        Silver-Pyke-Peterson lead-time variance, Kraljic risk, and Hwang-Yoon TOPSIS.
        """
        if not candidate_materials:
            return []

        # Find maximum technical score for reference normalization
        max_tech_score = max([float(m.get("index_value", m.get("final_metric", 1.0))) for m in candidate_materials], default=1.0)
        if max_tech_score <= 0:
            max_tech_score = 1.0

        evaluated_list = []
        for mat in candidate_materials:
            tech_score_raw = float(mat.get("index_value", mat.get("final_metric", 1.0)))
            norm_tech_score = (tech_score_raw / max_tech_score) * 100.0

            econ_eval = cls.evaluate_material_economics(
                material_data=mat,
                annual_demand_kg=annual_demand_kg,
                ashby_score=tech_score_raw
            )

            entry = {
                "key": mat.get("key", mat.get("name", "")),
                "name": mat.get("name", ""),
                "standard": mat.get("standard", "Standard"),
                "family": mat.get("family", "Engineering Material"),
                "technical_ashby_score": round(tech_score_raw, 2),
                "normalized_technical_score": round(norm_tech_score, 1),
                "composite_score": 50.0,  # to be populated by TOPSIS
                "economics": econ_eval,
                "raw_material_data": mat
            }
            evaluated_list.append(entry)

        # Non-Compensatory Conjunctive Screening Gate (Ashby, 2011; Sen & Yang, 1998)
        # Physical feasibility and material shelf-life limits strictly gate TOPSIS entry.
        # An unfeasible or degraded candidate cannot compensate for physical failure via cheap price.
        admissible_entries = []
        disqualified_entries = []

        for entry in evaluated_list:
            if entry["economics"].get("is_admissible", True):
                admissible_entries.append(entry)
            else:
                entry["topsis_closeness_score"] = 0.0000
                entry["composite_score"] = 0.0
                disqualified_entries.append(entry)

        # Execute rigorous Hwang-Yoon TOPSIS Multi-Criteria Decision Synthesis on Admissible Pool
        topsis_weights = {
            "tech": w_tech,
            "cost": w_cost,
            "lead_mean": w_lead * 0.60,
            "lead_std": w_lead * 0.40,
            "moq_pen": 0.05,
            "security": w_avail
        }
        if admissible_entries:
            admissible_entries = cls.calculate_topsis_ranking(admissible_entries, weights=topsis_weights)
            # Sort descending by TOPSIS composite score
            admissible_entries.sort(key=lambda x: x["composite_score"], reverse=True)

        # Concatenate admissible ranked items followed by gated disqualified items
        final_ranked_list = admissible_entries + disqualified_entries

        # Assign explicit ranks and strategic verdicts
        for rank, entry in enumerate(final_ranked_list, 1):
            entry["overall_rank"] = rank
            km_quad = entry["economics"]["kraljic_portfolio"]["quadrant"]
            landed_cost = entry["economics"]["landed_cost_usd_per_kg"]
            mean_lt = entry["economics"]["safety_stock_analysis"]["lead_time_mean_days"]
            is_adm = entry["economics"].get("is_admissible", True)

            if not is_adm:
                reason = entry["economics"].get("disqualification_reason", "Non-compensable constraint violation")
                entry["recommendation_verdict"] = f"Rank {rank} [DISQUALIFIED - Non-Compensable Gate]: {reason}"
            elif rank == 1:
                entry["recommendation_verdict"] = (
                    f"Rank 1: Pareto Optimal Choice ({km_quad} Portfolio, Landed ${landed_cost:.2f}/kg, "
                    f"Lead Time {mean_lt:.0f}d, TOPSIS C*={entry['topsis_closeness_score']:.3f})"
                )
            elif rank == 2:
                entry["recommendation_verdict"] = (
                    f"Rank 2: Strong Alternative Contender ({km_quad} Item, Landed ${landed_cost:.2f}/kg)"
                )
            elif rank == 3:
                entry["recommendation_verdict"] = (
                    f"Rank 3: Secondary Benchmark Candidate ({km_quad} Item)"
                )
            else:
                entry["recommendation_verdict"] = (
                    f"Rank {rank}: Viable Candidate (Subject to {km_quad} Sourcing Risk)"
                )

        return final_ranked_list
