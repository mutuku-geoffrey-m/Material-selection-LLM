"""
Techno-Economic & Supply Chain Optimization Engine for Engineering Material Selection.
Computes Economic Order Quantity (EOQ), evaluates Minimum Order Quantity (MOQ) constraints,
calculates shipping and logistics lead-time delays, assesses manufacturing reproducibility,
and computes a Multi-Criteria Decision Analysis (MCDA) ranking across technical and economic dimensions.
"""

import math
from typing import Dict, Any, List, Optional


class EconomicsEngine:
    """
    Evaluates raw material procurement economics, import logistics, MOQ constraints,
    EOQ batch sizing, and manufacturing reproducibility.
    """

    DEFAULT_ANNUAL_DEMAND_KG = 1000.0  # Standard engineering baseline annual requirement
    DEFAULT_HOLDING_RATE = 0.20         # 20% annual inventory carrying charge
    
    # Baseline setup / order procurement overheads by sourcing category
    ORDER_SETUP_COSTS = {
        "Domestic Local Stock": 120.0,    # USD (local PO, domestic dispatch, ground freight)
        "Regional Distribution": 320.0,   # USD (regional border clearance, bonded logistics)
        "Global Import": 680.0            # USD (international freight, tariffs, customs broker)
    }

    # Logistics lead-time ranges (in days)
    LEAD_TIME_DAYS = {
        "Domestic Local Stock": {"min": 2, "max": 5, "nominal": 3, "mode": "Road Freight"},
        "Regional Distribution": {"min": 7, "max": 14, "nominal": 10, "mode": "Cross-Border Trucking / Rail"},
        "Global Import": {"min": 30, "max": 60, "nominal": 42, "mode": "International Ocean Freight (or 7d Air Expedited)"}
    }

    @classmethod
    def calculate_eoq(
        cls,
        annual_demand_kg: float,
        cost_per_kg_usd: float,
        sourcing_category: str = "Domestic Local Stock",
        custom_setup_cost: Optional[float] = None,
        holding_rate: float = DEFAULT_HOLDING_RATE
    ) -> Dict[str, Any]:
        """
        Calculate Economic Order Quantity (EOQ) using the classical Wilson-Harris formulation:
        EOQ = sqrt((2 * D * S) / H)
        where:
          D = Annual demand in kg
          S = Procurement setup/order cost in USD
          H = Holding cost per kg-year (holding_rate * cost_per_kg)
        """
        D = max(annual_demand_kg, 1.0)
        C = max(cost_per_kg_usd, 0.5)
        S = custom_setup_cost or cls.ORDER_SETUP_COSTS.get(sourcing_category, 250.0)
        H = C * holding_rate

        eoq_kg = math.sqrt((2.0 * D * S) / H)
        orders_per_year = D / eoq_kg
        cycle_time_days = 365.0 / orders_per_year if orders_per_year > 0 else 365.0
        
        annual_order_cost = orders_per_year * S
        annual_holding_cost = (eoq_kg / 2.0) * H
        annual_material_cost = D * C
        total_annual_cost = annual_material_cost + annual_order_cost + annual_holding_cost

        return {
            "eoq_batch_size_kg": round(eoq_kg, 1),
            "orders_per_year": round(orders_per_year, 1),
            "order_interval_days": round(cycle_time_days, 1),
            "annual_order_cost_usd": round(annual_order_cost, 2),
            "annual_holding_cost_usd": round(annual_holding_cost, 2),
            "annual_material_cost_usd": round(annual_material_cost, 2),
            "total_annual_procurement_cost_usd": round(total_annual_cost, 2),
            "order_setup_cost_usd": S,
            "unit_holding_cost_per_kg_year": round(H, 2)
        }

    @classmethod
    def evaluate_material_economics(
        cls,
        material_data: Dict[str, Any],
        annual_demand_kg: float = DEFAULT_ANNUAL_DEMAND_KG,
        ashby_score: float = 1.0
    ) -> Dict[str, Any]:
        """
        Synthesize complete supply chain, availability, MOQ, EOQ, and reproducibility metrics
        for a single candidate material.
        """
        tech_econ = material_data.get("techno_economics", {})
        cost_kg = tech_econ.get("raw_cost_usd_per_kg") or material_data.get("cost_per_kg_usd", 6.0)
        source_cat = tech_econ.get("sourcing_category") or (
            "Domestic Local Stock" if material_data.get("kenya_availability") in ["High", "Very High"] else "Global Import"
        )
        moq_kg = tech_econ.get("minimum_order_quantity_kg", 25.0)
        lead_days = tech_econ.get("typical_lead_time_days") or cls.LEAD_TIME_DAYS.get(source_cat, {}).get("nominal", 14)
        machinability = tech_econ.get("machinability_rating_percent", 60.0)
        weldability = tech_econ.get("weldability", "Good")
        consistency = tech_econ.get("quality_consistency_rating", 98.0)

        # Compute EOQ
        eoq_data = cls.calculate_eoq(
            annual_demand_kg=annual_demand_kg,
            cost_per_kg_usd=cost_kg,
            sourcing_category=source_cat
        )

        # Check MOQ constraint
        moq_satisfied = annual_demand_kg >= moq_kg
        moq_surplus_kg = max(0.0, moq_kg - annual_demand_kg)
        moq_status = "Optimal Batch (Demand >= MOQ)" if moq_satisfied else f"Small-Lot Penalty (Order surplus {moq_surplus_kg:.0f} kg to meet MOQ)"

        # Cost per unit performance (Ashby economic metric: M / (rho * Cm))
        rho = material_data.get("density", 7800.0)
        cost_per_unit_volume = (rho / 1000.0) * cost_kg  # USD per dm^3 (liter)
        performance_per_dollar = (ashby_score / cost_per_unit_volume) if cost_per_unit_volume > 0 else 0.0

        # Sub-scores (0 to 100 scale)
        # Cost score: cheaper is higher score (normalized against $100/kg ceiling)
        score_cost = max(5.0, min(100.0, 100.0 - (cost_kg * 0.85)))
        
        # Availability & supply chain score
        if source_cat == "Domestic Local Stock":
            score_avail = 95.0
        elif source_cat == "Regional Distribution":
            score_avail = 72.0
        else: # Global Import
            score_avail = 45.0

        # Lead time score: shorter lead time is higher score
        score_lead = max(10.0, min(100.0, 100.0 - (lead_days * 1.5)))

        # Reproducibility & manufacturing ease score
        score_mfg = (machinability * 0.6) + (consistency * 0.4)

        return {
            "raw_cost_usd_per_kg": cost_kg,
            "cost_per_unit_volume_usd_liter": round(cost_per_unit_volume, 2),
            "performance_per_dollar_metric": round(performance_per_dollar, 3),
            "sourcing_category": source_cat,
            "minimum_order_quantity_kg": moq_kg,
            "moq_status": moq_status,
            "lead_time_days": lead_days,
            "logistics_mode": cls.LEAD_TIME_DAYS.get(source_cat, {}).get("mode", "Standard Freight"),
            "machinability_rating_percent": machinability,
            "weldability": weldability,
            "quality_consistency_percent": consistency,
            "eoq": eoq_data,
            "sub_scores": {
                "cost_score": round(score_cost, 1),
                "availability_score": round(score_avail, 1),
                "lead_time_score": round(score_lead, 1),
                "manufacturability_score": round(score_mfg, 1)
            }
        }

    @classmethod
    def rank_candidates_techno_economic(
        cls,
        candidate_materials: List[Dict[str, Any]],
        annual_demand_kg: float = DEFAULT_ANNUAL_DEMAND_KG,
        w_tech: float = 0.40,
        w_cost: float = 0.25,
        w_avail: float = 0.15,
        w_lead: float = 0.10,
        w_mfg: float = 0.10
    ) -> List[Dict[str, Any]]:
        """
        Multi-Criteria Decision Analysis (MCDA) Ranking:
        Combines technical Ashby performance score with economic viability,
        lead times, MOQ feasibility, and manufacturing reproducibility.
        """
        if not candidate_materials:
            return []

        # Find max technical score for normalization
        max_tech_score = max([m.get("index_value", 1.0) for m in candidate_materials], default=1.0)
        if max_tech_score <= 0:
            max_tech_score = 1.0

        evaluated_list = []
        for mat in candidate_materials:
            tech_score_raw = mat.get("index_value", 1.0)
            norm_tech_score = (tech_score_raw / max_tech_score) * 100.0

            econ_eval = cls.evaluate_material_economics(
                material_data=mat,
                annual_demand_kg=annual_demand_kg,
                ashby_score=tech_score_raw
            )

            subs = econ_eval["sub_scores"]
            composite_score = (
                (norm_tech_score * w_tech) +
                (subs["cost_score"] * w_cost) +
                (subs["availability_score"] * w_avail) +
                (subs["lead_time_score"] * w_lead) +
                (subs["manufacturability_score"] * w_mfg)
            )

            evaluated_list.append({
                "key": mat.get("key", mat.get("name", "")),
                "name": mat.get("name", ""),
                "standard": mat.get("standard", "Standard"),
                "family": mat.get("family", "Engineering Material"),
                "technical_ashby_score": round(tech_score_raw, 2),
                "normalized_technical_score": round(norm_tech_score, 1),
                "composite_score": round(composite_score, 1),
                "economics": econ_eval,
                "raw_material_data": mat
            })

        # Sort descending by composite score
        evaluated_list.sort(key=lambda x: x["composite_score"], reverse=True)

        # Assign explicit ranks
        for rank, entry in enumerate(evaluated_list, 1):
            entry["overall_rank"] = rank
            if rank == 1:
                entry["recommendation_verdict"] = "Rank 1: Optimal Multi-Objective Trade-Off (Top Technical & Sourcing Feasibility)"
            elif rank == 2:
                entry["recommendation_verdict"] = "Rank 2: Strong Alternative Contender"
            elif rank == 3:
                entry["recommendation_verdict"] = "Rank 3: Secondary Benchmark Candidate"
            else:
                entry["recommendation_verdict"] = f"Rank {rank}: Viable Candidate (Subject to Constraints)"

        return evaluated_list
