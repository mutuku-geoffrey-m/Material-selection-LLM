<!-- ========================================================================== -->
<!-- UNIVERSITY OF NAIROBI                                                      -->
<!-- FACULTY OF ENGINEERING                                                     -->
<!-- DEPARTMENT OF MECHANICAL AND MANUFACTURING ENGINEERING                     -->
<!-- ========================================================================== -->

<div align="center">

# UNIVERSITY OF NAIROBI
## FACULTY OF ENGINEERING
### DEPARTMENT OF MECHANICAL AND MANUFACTURING ENGINEERING

<br/>

**FMM3 561 ENGINEERING PROJECT**

**PROJECT CODE : JMO/2/25**

<br/>

## DEVELOPMENT OF A COMPUTATIONAL MATERIAL SELECTION AND OPTIMIZATION SYSTEM (EMS-OS) INTEGRATING ASHBY CONTINUUM MECHANICS, LOCAL FOUNDATION LARGE LANGUAGE MODELS, AND SUPPLY CHAIN TECHNO-ECONOMICS

<br/>

### AUTHORS:
**MUTUKU GEOFFREY MULU - F18/144332/2022**

<br/>

### PROJECT SUPERVISOR:
**PROF. JULIUS M. OGOLA**

<br/>

A proposal submitted in fulfilment for the Degree of Bachelor of Science in Mechanical Engineering in the Department of Mechanical and Manufacturing Engineering at the University of Nairobi

<br/>

**2026**

</div>

<div style="page-break-after: always;"></div>

---

<div align="right"><i>i | Page</i></div>

# Declaration

I hereby declare that the proposal titled **'Development of a Computational Material Selection and Optimization System (EMS-OS) Integrating Ashby Continuum Mechanics, Local Foundation Large Language Models, and Supply Chain Techno-Economics'** submitted in partial fulfillment for the Degree of Bachelors of Science in Mechanical Engineering at the University of Nairobi is my original work. I have not submitted this project, or any part of this project elsewhere for any Publication, Examination or Degree.

The project was carried out under the guidance and supervision of Prof. Julius M. Ogola, professor at the University of Nairobi. All the data, information, and references used have been duly acknowledged and cited.

<br/><br/>

........................................................................ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ....................................................  
**Mutuku Geoffrey Mulu** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date**  
Registration No.: F18/144332/2022  

<br/><br/>

**Supervisor**  

........................................................................ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ....................................................  
**Prof. Julius M. Ogola** &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; **Date**  

<div style="page-break-after: always;"></div>

---

<div align="right"><i>ii | Page</i></div>

# Abstract

The increasing complexity of modern mechanical engineering systems and the rapid expansion of the materials universe (surpassing 100,000 distinct candidate alloys, engineering thermoplastics, technical ceramics, and composite architectures) have rendered material selection an indispensable pillar of mechanical design. However, existing industrial and academic selection practices suffer from critical bottlenecks: traditional manual cross-referencing of two-dimensional Ashby charts is slow and poorly scalable to multi-objective constraints, while contemporary commercial Large Language Models (LLMs) deployed for engineering queries exhibit severe, non-deterministic failure modes. These generic AI tools frequently hallucinate fictitious mechanical constants ($\sigma_y$, $E$, $\rho$), violate fundamental continuum mechanics principles, omit empirical environmental degradation kinetics (such as hydrolytic embrittlement or cryogenic ductile-to-brittle transitions), and operate in complete isolation from real-world procurement realities.

This project focuses on the development of an autonomous, mathematically verified **Engineering Material Selection & Optimization System (EMS-OS)** specifically tailored for qualified mechanical design engineers. The project builds upon foundational materials selection research within the Department of Mechanical and Manufacturing Engineering at the University of Nairobi. The initial prototype established proof-of-concept natural language interpretation but relied on simplistic heuristic keyword matching, a restricted materials database, and lacked physical constraint enforcement and supply chain viability.

The improved EMS-OS architecture combines a local foundational Large Language Model (`llama3.2` running via an embedded Ollama daemon) with a high-throughput deterministic continuum mechanics engine executing Michael F. Ashby performance index calculations. The system queries an expanded, standardized database of over 1,490 engineering materials across ANSI, ISO, DIN, JIS, and ASTM standards. When candidate materials exhibit closely competitive performance indices (score delta $\le 8.0\%$), the platform automatically establishes an external internet arbitration connection to the Google Cloud Gemini API to perform deep metallurgical and microstructural failure-mode resolution. Furthermore, an integrated techno-economic module computes Wilson-Harris Economic Order Quantities (EOQ), Minimum Order Quantity (MOQ) penalties, and transport logistics transit delays (contrasting domestic trucking against Port of Mombasa maritime freight) to establish a comprehensive multi-criteria composite ranking.

System validation will be executed across 100 rigorous engineering audit scenarios and 15 adversarial edge cases, measuring positioning accuracy, physical constraint satisfaction rate, hallucination elimination, and dynamic mathematical provenance relative difference ($\text{rel\_diff} \le 10^{-4}$). The developed platform will serve as an indispensable bridge between theoretical instruction and industrial mechanical design, equipping engineering students and manufacturing practitioners with verified, cost-optimized, and procurable material solutions.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>iii | Page</i></div>

# Acknowledgment

I sincerely express my profound gratitude to Prof. Julius M. Ogola, my project supervisor, for his invaluable guidance, technical insight, and constructive critiques throughout the conceptualization and formulation of this project proposal.

I also extend my sincere appreciation to the academic faculty, laboratory technicians, and administrative staff of the Department of Mechanical and Manufacturing Engineering, Faculty of Engineering, University of Nairobi, for providing the scholarly resources, computational facilities, and supportive academic environment necessary to pursue this research.

Finally, I acknowledge the unwavering support and encouragement of my family, colleagues, and peers, whose continuous faith and motivation have been vital in bringing this engineering proposal to fruition.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>iv | Page</i></div>

# Dedication

This proposal is dedicated to my parents and family for their endless sacrifices, prayers, and unconditional encouragement throughout the course of my engineering education. 

It is also dedicated to my supervisor, lecturers, and academic mentors whose dedication to engineering excellence, intellectual rigor, and pedagogical passion continues to inspire my professional journey. 

Lastly, this work is dedicated to my fellow engineering peers and future mechanical innovators at the University of Nairobi, in the hope that this computational system contributes tangibly to the advancement of decentralized manufacturing, computational engineering design, and technological self-reliance in Kenya and the broader African continent.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>v | Page</i></div>

# Table of Contents

Declaration ....................................................................................................................................... i  
Abstract ............................................................................................................................................ ii  
Acknowledgment ........................................................................................................................... iii  
Dedication ....................................................................................................................................... iv  
List of Figures ................................................................................................................................ vii  
List of Tables ................................................................................................................................ viii  
Abbreviations .................................................................................................................................. ix  
Nomenclature ................................................................................................................................... x  

### CHAPTER 1: INTRODUCTION ................................................................................................ 1
1.1 Background .............................................................................................................................. 1  
1.2 Problem Statement .................................................................................................................... 3  
1.3 Research Objectives ................................................................................................................. 4  
1.4 Justification of the Study .......................................................................................................... 4  
1.5 Scope of the Project .................................................................................................................. 4  

### CHAPTER 2: LITERATURE REVIEW ..................................................................................... 5
2.1 Evolution of Material Selection in Mechanical Engineering ................................................... 5  
2.2 The Ashby Performance Index Methodology .......................................................................... 6  
2.3 Classical Loading Modes and Governing Failure Criteria ...................................................... 7  
&nbsp;&nbsp;&nbsp;&nbsp;1. Axial Tensile Ties .................................................................................................................. 7  
&nbsp;&nbsp;&nbsp;&nbsp;2. Flexural Bending Beams ....................................................................................................... 7  
&nbsp;&nbsp;&nbsp;&nbsp;3. Out-of-Plane Plate Bending ................................................................................................. 8  
&nbsp;&nbsp;&nbsp;&nbsp;4. Torsional Shafts and Drive Axles ......................................................................................... 8  
&nbsp;&nbsp;&nbsp;&nbsp;5. Thin-Walled Pressure Containment Vessels ........................................................................ 9  
&nbsp;&nbsp;&nbsp;&nbsp;6. Elastic Springs and Energy Storage Dampers ...................................................................... 9  
&nbsp;&nbsp;&nbsp;&nbsp;7. Steady-State Heat Dissipation Conduction Fins ................................................................. 10  
&nbsp;&nbsp;&nbsp;&nbsp;8. Transient Thermal Shock Barriers ..................................................................................... 10  
&nbsp;&nbsp;&nbsp;&nbsp;9. High-Speed Rotational Flywheels and Centrifuges ............................................................ 11  
&nbsp;&nbsp;&nbsp;&nbsp;10. Cyclic Alternating Stress and Fatigue Elements .............................................................. 11  
2.4 Multi-Dimensional Material Property Charts ........................................................................ 12  
2.5 Environmental Degradation and Operating Kinetics ............................................................. 13  
&nbsp;&nbsp;&nbsp;&nbsp;2.5.1 Hydrolytic Swelling and Moisture Saturation ............................................................... 13  
&nbsp;&nbsp;&nbsp;&nbsp;2.5.2 Ultraviolet Photo-Oxidative Embrittlement ................................................................... 13  
&nbsp;&nbsp;&nbsp;&nbsp;2.5.3 Thermal Deflection and Elevated Creep Kinetics .......................................................... 14  
&nbsp;&nbsp;&nbsp;&nbsp;2.5.4 Sub-Zero Cryogenic Ductile-to-Brittle Transition (DBTT) ............................................ 14  
2.6 Emergence of Computational Materials Informatics ............................................................. 15  
2.7 Natural Language Processing and Generative LLMs in Engineering ..................................... 15  
2.8 Hallucination Risks and Continuum Mechanics Failures in Generic LLMs ........................... 16  
2.9 Retrieval-Augmented Generation (RAG) and Semantic Vector Indexing ............................... 16  

<div style="page-break-after: always;"></div>

---

<div align="right"><i>vi | Page</i></div>

2.10 Multi-Tier Dual-Engine AI Architecture ............................................................................. 17  
2.11 Supply Chain Logistics, Inventory Optimization, and Techno-Economics ........................... 18  
&nbsp;&nbsp;&nbsp;&nbsp;2.11.1 Classical Wilson-Harris Economic Order Quantity (EOQ) ......................................... 18  
&nbsp;&nbsp;&nbsp;&nbsp;2.11.2 Supplier Minimum Order Quantity (MOQ) Constraints ............................................... 18  
&nbsp;&nbsp;&nbsp;&nbsp;2.11.3 Sourcing Lead Times and Transit Modeling ................................................................ 19  
2.12 Multi-Criteria Decision Analysis (MCDA / TOPSIS) .......................................................... 19  
2.13 Summary of Gaps in Existing Literature ............................................................................. 20  

### CHAPTER 3: MATERIALS AND METHOD ......................................................................... 21
3.1 Design of the Material Selection and Optimization System (EMS-OS) ................................ 21  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1 Conceptual Architecture of the EMS-OS Platform ...................................................... 21  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1.1 System Functional Specifications and Design Requirements .................................... 22  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1.2 Iterative Development and Enhancements from Previous Prototype ......................... 23  
&nbsp;&nbsp;&nbsp;&nbsp;3.1.1.3 Modular Subsystems of the EMS-OS Pipeline ........................................................... 24  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1. Scientific Specification Parser Subsystem ..................................................................... 24  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2. Standardized High-Throughput Materials Catalog .......................................................... 25  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3. Analytical Ashby Mechanics Selection Engine .............................................................. 25  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;4. Supply Chain and Techno-Economic Optimizer ............................................................ 26  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;5. Multi-Engine Dual-Tier Orchestrator ............................................................................. 26  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;6. Interactive User Interface and Automated Reporting ..................................................... 27  
3.2 Design Formulae and Mathematical Formulations ................................................................ 28  
&nbsp;&nbsp;&nbsp;&nbsp;3.2.1 Analytical Ashby Performance Indices ........................................................................ 28  
&nbsp;&nbsp;&nbsp;&nbsp;3.2.2 Environmental Degradation Penalty Formulations ........................................................ 29  
&nbsp;&nbsp;&nbsp;&nbsp;3.2.3 Economic Order Quantity and Supply Chain Logistics Equations ................................ 30  
&nbsp;&nbsp;&nbsp;&nbsp;3.2.4 Multi-Criteria Composite Scoring Model ..................................................................... 31  
3.3 Software Implementation and Computational Stack ............................................................... 32  
3.4 Data Acquisition and Materials Catalog Curation .................................................................. 33  
3.5 Performance Testing and Experimental Verification ............................................................. 34  

### CHAPTER 4: WORK PLAN AND BUDGET ......................................................................... 36
4.1 Budget .................................................................................................................................... 36  
&nbsp;&nbsp;&nbsp;&nbsp;4.1.1 Budget Justification ....................................................................................................... 36  
4.2 Work Plan and Project Schedule ............................................................................................ 37  
&nbsp;&nbsp;&nbsp;&nbsp;4.2.1 Project Milestones and Gantt Chart ............................................................................... 37  

### Appendices .................................................................................................................................. 39
Appendix 1 - Master Table of Ashby Mechanical Performance Indices ..................................... 39  
Appendix 2 - International Engineering Standard Designations and Mappings ........................... 40  
Appendix 3 - Sourcing Category Parameters and Transit Lead Times ......................................... 41  

### References ................................................................................................................................. 42

<div style="page-break-after: always;"></div>

---

<div align="right"><i>vii | Page</i></div>

# List of Figures

Figure 2.2.1 : Schematic of the Michael F. Ashby Material Selection Process ............................... 6  
Figure 2.3.1 : Principal Structural Loading Geometries in Continuum Mechanics ........................ 8  
Figure 2.4.1 : Classical Ashby Chart: Young's Modulus ($E$) versus Material Density ($\rho$) ........ 12  
Figure 2.4.2 : Classical Ashby Chart: Yield Strength ($\sigma_y$) versus Material Density ($\rho$) ........... 12  
Figure 2.8.1 : Typical Hallucination Failure Trajectories in Unconstrained Generative LLMs ....... 16  
Figure 2.9.1 : Architecture of a Retrieval-Augmented Generation (RAG) Vector Pipeline ............ 17  
Figure 2.11.1 : Classical Wilson-Harris Economic Order Quantity (EOQ) Cost Curves ................ 18  
Figure 3.1.1 : Complete System Architecture of the Proposed EMS-OS Platform ....................... 21  
Figure 3.1.2 : Six-Phase Transparent Chain-of-Thought Decision Flowchart ................................ 24  
Figure 3.1.3 : Automatic Cloud AI (Gemini) Tie-Breaker Arbitration Workflow ......................... 27  
Figure 3.3.1 : Interactive Streamlit User Interface and Dynamic 2D/3D Plotly Visualizer .......... 33  

<div style="page-break-after: always;"></div>

---

<div align="right"><i>viii | Page</i></div>

# List of Tables

Table 1.1 : Summary of Typical Mechanical Component Performance Criteria ............................ 2  
Table 2.1 : Comparison of General-Purpose LLMs versus Deterministic Selection Engines ........ 17  
Table 3.1 : Target Functional Specifications and Operating Envelopes for EMS-OS .................. 22  
Table 3.2 : Comparative Upgrades from Previous Prototype to Current EMS-OS ........................ 23  
Table 3.3 : Summary of Governing Mathematical Formulae in the EMS-OS Framework ............. 31  
Table 3.4 : Software Dependencies and System Libraries ............................................................ 32  
Table 3.5 : Performance Parameters and Acceptance Criteria for System Testing ....................... 35  
Table 4.1.1 : Projected Budget for the Development and Validation of EMS-OS ........................ 36  
Table 4.2.1 : Capstone Project Work Plan Schedule (September 2025 - May 2026) ..................... 38  
Table A.1 : Comprehensive Catalog of Governing Continuum Mechanics Ashby Indices ........... 39  
Table A.2 : Mapping of International Testing Standards to Physical Constraints ......................... 40  
Table A.3 : Default Procurement Logistics and Carrying Cost Benchmarks ................................ 41  

<div style="page-break-after: always;"></div>

---

<div align="right"><i>ix | Page</i></div>

# Abbreviations

| Abbreviation | Complete Technical Terminology |
| :--- | :--- |
| **AI** | Artificial Intelligence |
| **AISI** | American Iron and Steel Institute |
| **ANSI** | American National Standards Institute |
| **API** | Application Programming Interface |
| **ASME** | American Society of Mechanical Engineers |
| **ASTM** | American Society for Testing and Materials |
| **CAD** | Computer-Aided Design |
| **CAE** | Computer-Aided Engineering |
| **CAM** | Computer-Aided Manufacturing |
| **CFRP** | Carbon Fiber Reinforced Polymer |
| **CNC** | Computerized Numerical Control |
| **DBTT** | Ductile-to-Brittle Transition Temperature |
| **DIN** | Deutsches Institut für Normung (German Institute for Standardization) |
| **EDM** | Electrical Discharge Machining |
| **EMS-OS** | Engineering Material Selection & Optimization System |
| **EOQ** | Economic Order Quantity |
| **FDM** | Fused Deposition Modeling |
| **FEA** | Finite Element Analysis |
| **FFF** | Fused Filament Fabrication |
| **G-Code** | Geometric Numerical Control Programming Code |
| **GRBL** | Open-Source Embedded G-Code Motion Control Firmware |
| **HDT** | Heat Deflection Temperature |
| **IEEE** | Institute of Electrical and Electronics Engineers |
| **ISO** | International Organization for Standardization |
| **JIS** | Japanese Industrial Standards |
| **LLM** | Large Language Model |
| **LOX** | Liquid Oxygen |
| **MCDA** | Multi-Criteria Decision Analysis |
| **MOQ** | Minimum Order Quantity |
| **NLP** | Natural Language Processing |
| **NEMA** | National Electrical Manufacturers Association |
| **PA12-CF** | Polyamide 12 Reinforced with Chopped Carbon Fibers |
| **PC** | Polycarbonate |
| **PEEK** | Polyether Ether Ketone |
| **PETG** | Polyethylene Terephthalate Glycol |
| **PETG-CF** | Polyethylene Terephthalate Glycol Reinforced with Carbon Fibers |
| **PLA** | Polylactic Acid |
| **PMMA** | Polymethyl Methacrylate (Acrylic) |
| **POM** | Polyoxymethylene (Acetal / Delrin) |
| **PTFE** | Polytetrafluoroethylene (Teflon) |
| **RAG** | Retrieval-Augmented Generation |
| **RPM** | Revolutions Per Minute |
| **TOPSIS** | Technique for Order of Preference by Similarity to Ideal Solution |
| **TPU** | Thermoplastic Polyurethane |
| **UI** | User Interface |
| **UTS** | Ultimate Tensile Strength |
| **UV** | Ultraviolet Radiation |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>x | Page</i></div>

# Nomenclature

### Nomenclature of Equations

| Symbol | Description | SI Units |
| :---: | :--- | :---: |
| $M$ | Ashby Material Performance Index | Dimensionless / Multi-Unit |
| $E$ | Young's Modulus of Elasticity | $\text{GPa}$ or $\text{N/m}^2$ |
| $G$ | Shear Modulus of Rigidity | $\text{GPa}$ or $\text{N/m}^2$ |
| $\rho$ | Material Mass Density | $\text{kg/m}^3$ |
| $\sigma_y$ | Tensile Yield Strength | $\text{MPa}$ or $\text{N/m}^2$ |
| $\sigma_{\text{uts}}$ | Ultimate Tensile Strength | $\text{MPa}$ or $\text{N/m}^2$ |
| $\sigma_f$ | Fatigue Endurance Limit ($10^7$ cycles) | $\text{MPa}$ or $\text{N/m}^2$ |
| $K_{1c}$ | Critical Plane-Strain Fracture Toughness | $\text{MPa}\cdot\sqrt{\text{m}}$ |
| $\lambda$ | Thermal Conductivity | $\text{W/(m}\cdot\text{K)}$ |
| $a$ | Thermal Diffusivity ($a = \lambda / (\rho \cdot C_p)$) | $\text{m}^2/\text{s}$ |
| $C_p$ | Specific Heat Capacity | $\text{J/(kg}\cdot\text{K)}$ |
| $\alpha_L$ | Linear Coefficient of Thermal Expansion | $\text{K}^{-1}$ or $\mu\text{m/(m}\cdot\text{K)}$ |
| $T_{\text{service}}$ | Operating Service Temperature | $^\circ\text{C}$ or $\text{K}$ |
| $T_{\text{melt}}$ | Equilibrium Melting Point Temperature | $^\circ\text{C}$ or $\text{K}$ |
| $T_{\text{HDT}}$ | Heat Deflection Temperature under Flexural Load | $^\circ\text{C}$ |
| $T_H$ | Homologous Temperature ($T_H = T_{\text{service}} / T_{\text{melt}}$) | Dimensionless |
| $D$ | Annual Project Demand for Material | $\text{kg/year}$ |
| $S$ | Sourcing Setup and Order Placement Fixed Cost | $\text{USD/order}$ |
| $C_m$ | Raw Material Unit Cost | $\text{USD/kg}$ |
| $i$ | Annual Inventory Holding Carrying Rate (Default: $0.20$) | $\text{year}^{-1}$ |
| $H$ | Inventory Carrying Cost per Unit Mass per Year ($H = i \cdot C_m$) | $\text{USD/(kg}\cdot\text{year)}$ |
| $\text{EOQ}$ | Optimal Economic Order Quantity | $\text{kg}$ |
| $\text{MOQ}$ | Supplier Mandatory Minimum Order Quantity | $\text{kg}$ |
| $\Delta C_{\text{surplus}}$ | Annual Financial Penalty for Surplus Inventory Holding | $\text{USD/year}$ |
| $L_{\text{days}}$ | Sourcing Logistics Transit Lead Time | $\text{Days}$ |
| $S_{\text{composite}}$ | Multi-Criteria Decision Composite Performance Score | Points ($0 - 100$) |
| $w_{\text{tech}}$ | Weighting Factor for Mechanical Ashby Efficiency ($0.45$) | Dimensionless |
| $w_{\text{cost}}$ | Weighting Factor for Raw Material Procurement Cost ($0.25$) | Dimensionless |
| $w_{\text{lead}}$ | Weighting Factor for Transport Transit Lead Time ($0.15$) | Dimensionless |
| $w_{\text{moq}}$ | Weighting Factor for Batch Size Ordering Flexibility ($0.15$) | Dimensionless |
| $\Delta_{\text{score}}$ | Percentage Performance Delta between Competing Contenders | $\%$ |
| $\text{rel\_diff}$ | Provenance Relative Error between Dynamic and Exact Indices | Dimensionless |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>1 | Page</i></div>

# CHAPTER 1: INTRODUCTION

## 1.1 Background

In mechanical and manufacturing engineering, the selection of materials directly governs the operational integrity, longevity, mass efficiency, manufacturability, and economic viability of any designed component [1]. From high-speed turbine rotors and pressure containment vessels to lightweight robotic booms and surgical implants, the failure to select an optimal material often results in catastrophic mechanical yielding, premature fatigue fracture, excessive structural deflection, or severe operational corrosion [2]. 

Historically, material selection relied predominantly on qualitative rules of thumb, localized empirical traditions, or fragmented trial-and-error prototyping. However, over the past four decades, the materials universe has expanded dramatically, now encompassing over 100,000 distinct commercial alloys, polymers, structural composites, and technical ceramics [3]. To bring mathematical rigor to this complex multi-variable domain, Professor Michael F. Ashby pioneered the **Materials Performance Index Methodology** [4]. By analytically decomposing a component's functional requirements, boundary constraints, and primary optimization objective, the governing engineering equations can be separated into functional, geometric, and material property groups:

$$p = f_1(\text{Functional Requirements}) \times f_2(\text{Geometric Parameters}) \times f_3(\text{Material Properties})$$

Maximizing performance corresponds mathematically to maximizing or minimizing a specific material index ($M$). For example, in a lightweight cantilever beam subjected to bending stiffness constraints (e.g., an aircraft wing spar or robotic manipulator arm), the material performance index to be maximized is:

$$M = \frac{E^{1/2}}{\rho}$$

where $E$ is Young's Modulus of Elasticity ($\text{GPa}$) and $\rho$ is the material density ($\text{kg/m}^3$) [4].

Despite the universal elegance and mathematical validity of the Ashby framework, practical engineering implementation in modern industrial design and educational environments faces three formidable barriers:

1. **Scalability and Dimensionality Limits of Manual Charts:** Traditional Ashby selection relies on static two-dimensional logarithmic bubble charts. While highly visual for two variables (e.g., $E$ versus $\rho$), real-world engineering design routinely requires simultaneous optimization across eight or more orthogonal parameters: tensile yield strength ($\sigma_y$), fracture toughness ($K_{1c}$), fatigue endurance limit ($\sigma_f$), thermal conductivity ($\lambda$), operating temperature limits ($T_{\text{max}}$), chemical resistance, and raw cost ($C_m$). Manual cross-filtering across dozens of 2D charts is extraordinarily labor-intensive, error-prone, and incapable of high-throughput automated screening across thousands of candidate grades [5].

2. **The Peril of Ungrounded Generative AI:** The emergence of generative Large Language Models (LLMs)--such as OpenAI's GPT-4, Google's Gemini, and Meta's Llama family--has spurred interest in deploying AI as natural language engineering assistants. However, extensive academic evaluations demonstrate that generic, ungrounded LLMs suffer from severe hallucination vulnerabilities when queried on mechanical design tasks [6]. They frequently fabricate fictitious yield strengths that violate theoretical crystal lattice physics, confuse yield strength with ultimate tensile strength, recommend hygroscopic polymers (e.g., PLA) for submerged marine hydro-turbines despite known hydrolytic degradation, and fail to enforce deterministic temperature thresholds such as the Heat Deflection Temperature (HDT) or the cryogenic Ductile-to-Brittle Transition Temperature (DBTT) [7]. In critical load-bearing engineering, relying on statistical token probability rather than continuum mechanics can cause catastrophic structural failures.

3. **Complete Isolation from Supply Chain Realities:** Existing computational selection software packages (such as Granta Design / Ansys Granta EduPack) evaluate materials in a theoretical vacuum, completely decoupled from supply chain economics and logistics realities [8]. In actual industrial practice, particularly in developing economies such as Kenya, a material that scores highest in pure physical efficiency may be completely unprocurable. Real-world procurement is heavily constrained by supplier Minimum Order Quantities (MOQ), Economic Order Quantity (EOQ) carrying costs, customs clearance tariffs, and extended international shipping lead times (e.g., 40 to 60 days for sea freight arriving at the Port of Mombasa compared to 2 to 5 days for local domestic steel stock) [9].

Recognizing these challenges, final-year engineering research at the University of Nairobi initiated preliminary investigations into building automated material selection aids for localized manufacturing [10]. The initial proof-of-concept system successfully parsed basic natural language strings and retrieved candidate materials using naive keyword mapping. However, that early iteration exhibited severe functional limitations: it relied on colloquial layman phrasing, lacked formal ASTM/ISO engineering standards mapping, utilized a restricted database of fewer than 20 common polymers and alloys, could not detect edge-case ambiguities or close contenders, and possessed zero supply chain or logistics intelligence.

Building on those foundational findings, the current capstone project establishes a comprehensive, production-grade **Engineering Material Selection & Optimization System (EMS-OS)**. Tailored exclusively for qualified mechanical engineers, the platform couples structured scientific prompts with a local foundation LLM (`llama3.2` executed via Ollama), a persistent ChromaDB Retrieval-Augmented Generation (RAG) vector store, an expanded database of over 1,490 standardized materials, automated Cloud Gemini tie-breaker arbitration, and a classical Wilson-Harris supply chain techno-economic optimizer.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>3 | Page</i></div>

## 1.2 Problem Statement

In mechanical and manufacturing engineering design, selecting the optimal material is critical to preventing structural failure, minimizing parasitic mass, ensuring operational safety, and controlling product life-cycle costs. However, practicing mechanical engineers, decentralized workshops, and engineering students in Kenya currently lack an integrated computational platform capable of translating complex, multi-objective design specifications directly into mathematically verified material selections that are both physically sound and logistically procurable.

Currently, engineers must choose between two flawed alternatives:
1. **Manual Static Selection:** Relying on physical handbooks and static 2D Ashby charts. This process is slow, cumbersome, subjective, and incapable of screening multi-dimensional constraints across the modern universe of over 100,000 engineering materials.
2. **Ungrounded Conversational AI:** Querying generic cloud-hosted LLMs (e.g., standard ChatGPT). These statistical models suffer from catastrophic engineering hallucinations, inventing non-existent material strengths, ignoring environmental degradation kinetics (such as water saturation hydrolysis or UV photo-oxidation), and demonstrating zero adherence to governing international codes (ISO 527, ASTM D638, ASME Section VIII).

Furthermore, all existing computational material selection frameworks completely ignore supply chain feasibility. A design that specifies an exotic aerospace-grade superalloy or specialized continuous-fiber composite may be theoretically optimal in software, yet fundamentally unviable for a localized project due to prohibitive Minimum Order Quantities (MOQ), exorbitant inventory carrying costs, and 3-month international shipping delays. 

Without a unified computational framework that integrates deterministic continuum mechanics, grounded local AI synthesis, cloud-based microstructural arbitration, and supply chain logistics modeling, mechanical engineers will continue to suffer from premature prototype failures, prolonged design cycles, and costly supply chain bottlenecks.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>4 | Page</i></div>

## 1.3 Research Objectives

### Main Objective
The main objective of this capstone research project is to design, develop, implement, and experimentally validate an autonomous, deterministic **Engineering Material Selection & Optimization System (EMS-OS)** that integrates Michael F. Ashby continuum mechanics, a curated database of 1,490+ standardized materials, a local foundational LLM (`llama3.2`), automated Cloud Gemini tie-break arbitration, and supply chain techno-economic modeling for mechanical design applications.

### Specific Objectives
To achieve this main goal, the specific research objectives are:
1. **To curate and standardize a high-throughput engineering materials catalog** comprising over 1,490 distinct materials across ANSI, ISO, DIN, JIS, and ASTM standards with unified mechanical, thermal, environmental, and techno-economic attributes.
2. **To develop a scientific NLP translation module** tailored for qualified mechanical engineers that parses structured design criteria, numerical limits, and governing international regulatory codes (ISO, ASTM, ASME Section VIII, DIN).
3. **To formulate and implement a deterministic Ashby optimization engine** that calculates exact analytical performance indices for bending, tension, shear, pressure containment, thermal dissipation, and cyclic fatigue while enforcing hard environmental and thermal degradation penalties.
4. **To engineer a multi-tier dual-engine AI pipeline** featuring a local standalone foundation model (`llama3.2` via Ollama) with transparent chain-of-thought logging and automated Cloud Gemini API arbitration for competitive close-contender edge cases ($\Delta_{\text{score}} \le 8.0\%$).
5. **To formulate and integrate a supply chain techno-economic optimizer** that computes Wilson-Harris Economic Order Quantities (EOQ), Minimum Order Quantity (MOQ) surplus penalties, logistics lead times, and multi-criteria TOPSIS composite rankings.
6. **To validate and benchmark the system** across 100 standardized engineering audit scenarios and 15 adversarial edge cases, evaluating positioning accuracy, physical constraint satisfaction rate, hallucination elimination, and mathematical provenance.

## 1.4 Justification of the Study

The development of the EMS-OS platform provides direct, measurable benefits across academic, industrial, and national economic domains:
- **Academic Rigor and Innovation:** Bridges the gap between classical continuum mechanics, material science informatics, and modern artificial intelligence, demonstrating how neuro-symbolic architectures eliminate LLM hallucinations in mission-critical engineering.
- **Acceleration of the Mechanical Design Cycle:** Reduces the material selection and constraint evaluation phase from days of manual literature searches to seconds of deterministic computation.
- **Supply Chain Resilience for Local Manufacturing:** By explicitly incorporating domestic road transport lead times versus international sea freight through the Port of Mombasa, the system empowers Kenyan manufacturing enterprises, MSMEs, and decentralized agricultural processors to identify cost-effective, locally stocked engineering substitutes without compromising structural safety.
- **Zero-Failure Engineering Reliability:** Eliminates the risk of catastrophic mechanical failures by enforcing strict, non-overridable continuum mechanics equations and empirical degradation kinetics.

## 1.5 Scope of the Project

The scope of this project encompasses:
- The mathematical derivation and algorithmic encoding of 12 primary Ashby performance indices.
- The curation and structuring of a 1,490+ material JSON/SQLite database with standardized SI units.
- The software development of a Python 3.11 architecture integrating ChromaDB vector storage, Ollama local model execution, and Google Cloud Gemini API connectivity.
- The mathematical formulation of the Wilson-Harris EOQ model, MOQ feasibility checks, and TOPSIS composite scoring.
- The development of a responsive Streamlit graphical user interface featuring interactive 2D/3D Plotly property charts.
- The experimental validation of the system against 100 comprehensive mechanical design test cases.

The project does **not** include primary experimental destructive mechanical tensile testing of raw specimens in the physical laboratory, nor does it encompass custom finite element mesh generation (FEA), focusing instead on the analytical material screening and preliminary design optimization stages.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>5 | Page</i></div>

# CHAPTER 2: LITERATURE REVIEW

## 2.1 Evolution of Material Selection in Mechanical Engineering

The systematic selection of materials has evolved in tandem with the industrial revolutions. In the early nineteenth century, mechanical design was severely constrained by the limited availability of structural materials, primarily timber, cast iron, wrought iron, and plain carbon steels [1]. Component sizing was dictated by large empirical safety factors (frequently exceeding $N = 5$ to $10$) to compensate for unknown material defects, variable carbon contents, and unquantified stress concentrations [2].

As metallurgy advanced throughout the twentieth century--spurred by the development of alloy steels, precipitation-hardened aluminums, titanium alloys, structural polymers, and fiber-reinforced composites--the materials landscape expanded exponentially [3]. By the late twentieth century, the number of engineering materials commercially available surpassed 100,000 [4]. This rapid diversification rendered intuitive or trial-and-error selection dangerous, leading to catastrophic service failures such as the ductile-to-brittle fracture of World War II Liberty ships in cold waters and the rapid stress-corrosion cracking of high-strength aircraft landing gear components [5].

To establish a rational, objective methodology, early researchers attempted quantitative scoring matrices. In 1968, Dieter introduced Weighted Property Indexes (WPI), wherein candidate materials were scored against normalized engineering parameters multiplied by subjective weighting coefficients [6]. However, early matrix approaches suffered from fundamental flaws: they could not isolate the effect of component geometry from material properties, nor could they systematically identify the theoretical physical limits of performance across competing material families [7].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>6 | Page</i></div>

## 2.2 The Ashby Performance Index Methodology

A revolutionary breakthrough occurred in the late 1980s and early 1990s when Professor Michael F. Ashby of the University of Cambridge established the formal **Materials Selection Methodology** [4]. Ashby recognized that any mechanical design problem can be formulated in terms of four distinct categories:

1. **Function:** What the component does (e.g., beam, tie, shaft, plate, column, heat sink, spring).
2. **Objective:** What is to be maximized or minimized (e.g., minimize mass $m$, minimize raw material cost $C$, maximize stored energy $U$, minimize thermal loss $Q$).
3. **Constraints:** Essential boundary limits that must be satisfied (e.g., maximum allowable deflection $\delta \le \delta_{\text{max}}$, yield failure limit $\sigma \le \sigma_y / S_F$, maximum operating temperature $T \le T_{\text{max}}$, corrosion resistance).
4. **Free Variables:** Geometric dimensions that the engineer can adjust freely to satisfy constraints (e.g., cross-sectional area $A$, thickness $t$, diameter $d$).

The analytical procedure involves writing governing equations for the objective function and the active constraint, and then algebraically eliminating the free geometric variable [8]. This separates the performance equation into three independent terms:

$$P = f_1(F) \times f_2(G) \times f_3(M)$$

where $F$ denotes functional loading requirements, $G$ represents geometric specifications, and $M$ is the characteristic **Material Performance Index**.

```
┌──────────────────────────────────────────────────────────┐
│                   DESIGN SPECIFICATION                   │
│         Function, Constraints, Objective, Free Vars      │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│               ELIMINATE FREE VARIABLES                   │
│   Algebraic combination of Objective & Constraint Eqns   │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│           ISOLATE MATERIAL PERFORMANCE INDEX (M)         │
│          M = f(Properties) to be Maximized / Min         │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│               ASHBY SELECTION PROPERTY CHARTS            │
│       Logarithmic Multi-Material Screening Envelopes     │
└──────────────────────────────────────────────────────────┘
```
*Figure 2.2.1: Schematic of the Michael F. Ashby Material Selection Process [4].*

<div style="page-break-after: always;"></div>

---

<div align="right"><i>7 | Page</i></div>

## 2.3 Classical Loading Modes and Governing Failure Criteria

To understand the mathematical foundation of the EMS-OS selection engine, the continuum mechanics derivations for primary structural loading modes must be examined in detail [4, 8].

### 1. Axial Tensile Ties
Consider a structural tie rod of length $L$ and uniform cross-sectional area $A$, carrying an axial tensile force $F$.

**Case A: Minimum Mass with Deflection Constraint (Stiffness Limit)**  
The total mass is $m = A L \rho$, and the elastic elongation is:
$$\delta = \frac{F L}{A E} \le \delta_{\text{max}}$$
The free geometric variable is cross-sectional area $A$. Solving for $A \ge \frac{F L}{\delta_{\text{max}} E}$ and substituting into the mass equation yields:
$$m \ge (F L^2 / \delta_{\text{max}}) \left( \frac{\rho}{E} \right)$$
To minimize mass $m$, the performance index to maximize is:
$$M_1 = \frac{E}{\rho} \quad \text{or} \quad \frac{\rho}{E} \to \text{minimize}$$

**Case B: Minimum Mass with Yield Strength Constraint (Fracture Limit)**  
The axial tensile stress must satisfy $\sigma = F / A \le \sigma_y$. Eliminating area $A \ge F / \sigma_y$:
$$m \ge (F L) \left( \frac{\rho}{\sigma_y} \right)$$
To minimize mass, the specific yield strength index to maximize is:
$$M_2 = \frac{\sigma_y}{\rho}$$

### 2. Flexural Bending Beams
Consider a beam of length $L$ and solid square cross-section $b \times b$ loaded in flexure by a transverse force $F$.

**Case A: Minimum Mass with Flexural Stiffness Constraint**  
The flexural deflection is governed by beam theory:
$$\delta = \frac{C_1 F L^3}{E I} \le \delta_{\text{max}}$$
where for a solid square cross-section, $I = b^4 / 12 = A^2 / 12$. Total mass is $m = A L \rho$. Solving for area $A$:
$$A = \left( \frac{12 C_1 F L^3}{\delta_{\text{max}} E} \right)^{1/2}$$
Substituting $A$ into the mass equation:
$$m = (12 C_1 F L^5 / \delta_{\text{max}})^{1/2} \left( \frac{\rho}{E^{1/2}} \right)$$
To minimize mass, the governing flexural stiffness index to maximize is:
$$M_3 = \frac{E^{1/2}}{\rho}$$

**Case B: Minimum Mass with Bending Yield Strength Constraint**  
The maximum bending moment is $M_{\text{bend}} = C_2 F L$. The outer-fiber failure stress is $\sigma = \frac{M_{\text{bend}} y}{I} = \frac{C_2 F L (b/2)}{b^4 / 12} = \frac{6 C_2 F L}{b^3} \le \sigma_y$. Since $A = b^2$, $b = A^{1/2}$, hence $b^3 = A^{3/2}$.  
Solving for $A \ge \left( \frac{6 C_2 F L}{\sigma_y} \right)^{2/3}$ and substituting into $m = A L \rho$:
$$m = (6 C_2 F L^5 / 2)^{2/3} \left( \frac{\rho}{\sigma_y^{2/3}} \right)$$
To minimize mass, the flexural bending strength index to maximize is:
$$M_4 = \frac{\sigma_y^{2/3}}{\rho}$$

<div style="page-break-after: always;"></div>

---

<div align="right"><i>8 | Page</i></div>

```
         (a) Tensile Tie                      (b) Bending Beam
       F <══════[ A ]══════> F                       F
                                                     │
                                            ┌────────┴────────┐
                                            ▲                 ▲
       M = σ_y / ρ  or  E / ρ               M = σ_y^(2/3) / ρ  or  E^(1/2) / ρ

         (c) Plate Bending                   (d) Torsion Shaft
                 q (pressure)                       T <───┐
             ↓↓↓↓↓↓↓↓↓↓↓↓                                 └───> T
          ─────────────────────
             ▲               ▲              M = τ_y^(2/3) / ρ  or  G^(1/2) / ρ
       M = σ_y^(1/2) / ρ  or  E^(1/3) / ρ
```
*Figure 2.3.1: Principal Structural Loading Geometries in Continuum Mechanics [4].*

### 3. Out-of-Plane Plate Bending
For flat panels, shell plates, and vehicle aerodynamic body panels of span $L$, width $W$, and thickness $t$, subjected to out-of-plane pressure loads:
- **Plate Bending Stiffness:** Governed by flexural plate rigidity $D = \frac{E t^3}{12 (1 - \nu^2)}$. Eliminating thickness $t$ gives the stiff plate index:
  $$M_5 = \frac{E^{1/3}}{\rho}$$
- **Plate Yield Strength:** The maximum surface stress under flexural bending scales with $t^{-2}$. Eliminating thickness yields the strong plate index:
  $$M_6 = \frac{\sigma_y^{1/2}}{\rho}$$

### 4. Torsional Shafts and Drive Axles
For solid circular shafts of radius $R$ transmitting torque $T$:
- **Torsional Stiffness per Unit Mass:** Governed by polar moment of inertia $J = \frac{\pi R^4}{2}$ and shear modulus $G$:
  $$M_7 = \frac{G^{1/2}}{\rho}$$
- **Torsional Strength per Unit Mass:** Governed by maximum surface shear stress $\tau = \frac{T R}{J} \le \tau_y \approx 0.577 \sigma_y$:
  $$M_8 = \frac{\tau_y^{2/3}}{\rho} \approx \frac{\sigma_y^{2/3}}{\rho}$$

<div style="page-break-after: always;"></div>

---

<div align="right"><i>9 | Page</i></div>

### 5. Thin-Walled Pressure Containment Vessels
For cylindrical shells of radius $R$ and wall thickness $t$ carrying internal gauge pressure $P$, the primary failure mode is hoop stress yielding governed by Barlow's formula:
$$\sigma_{\text{hoop}} = \frac{P R}{t} \le \frac{\sigma_y}{S_F}$$
The wall thickness must satisfy $t \ge \frac{P R S_F}{\sigma_y}$. The mass of the containment shell is $m = 2 \pi R L t \rho = 2 \pi R^2 L P S_F \left( \frac{\rho}{\sigma_y} \right)$.  
To minimize vessel mass while safely containing pressure $P$, the index to maximize is:
$$M_9 = \frac{\sigma_y}{\rho}$$

In containment vessels subjected to leak-before-break safety criteria (ASME Section VIII Division 2), catastrophic fast fracture occurs when the crack depth equals wall thickness before plastic yielding occurs. Combining the Irwin fracture equation $K_{1c} = \sigma \sqrt{\pi a_c}$ with wall thickness yields the fracture-safe containment index:
$$M_{9b} = \frac{K_{1c}}{\sigma_y}$$

### 6. Elastic Springs and Energy Storage Dampers
For elastic energy storage devices (leaf springs, helical suspension springs, recoil buffers), the objective is to maximize the reversible strain energy stored per unit volume without plastic yielding:
$$U_v = \int_0^{\epsilon_y} \sigma \, d\epsilon = \frac{1}{2} \sigma_y \epsilon_y = \frac{\sigma_y^2}{2 E}$$
For maximum elastic energy per unit mass, the performance index is:
$$M_{10} = \frac{\sigma_y^2}{E \rho}$$
For maximum elastic energy per unit volume:
$$M_{10b} = \frac{\sigma_y^2}{E}$$
This index demonstrates why high-yield, low-modulus materials (such as spring steels, titanium alloys, and elastomeric polymers like TPU) vastly outperform stiff, low-yield materials in damping and spring applications [4].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>10 | Page</i></div>

### 7. Steady-State Heat Dissipation Conduction Fins
In electronic heat sinks, microprocessor thermal spreaders, and cooling radiators, heat is conducted by Fourier conduction:
$$q = -\lambda \nabla T$$
For maximum steady-state conductive heat flux per unit mass:
$$M_{11} = \frac{\lambda}{\rho}$$
where $\lambda$ is thermal conductivity ($\text{W/(m}\cdot\text{K)}$) and $\rho$ is density ($\text{kg/m}^3$). This explains why Copper ($\lambda \approx 390\,\text{W/(m}\cdot\text{K)}$) and Aluminum alloys ($\lambda \approx 170 - 200\,\text{W/(m}\cdot\text{K)}$) dominate thermal conduction hardware.

### 8. Transient Thermal Shock Barriers
For thermal insulation blankets, kiln linings, and rocket engine ablative shields, the goal is to minimize thermal penetration under transient heating. The thermal diffusivity is:
$$a = \frac{\lambda}{\rho C_p}$$
To maximize insulation and delay thermal ingress, thermal conductivity must be minimized:
$$M_{12} = \frac{1}{\lambda} \quad \text{or} \quad M_{12b} = \frac{1}{a} = \frac{\rho C_p}{\lambda}$$
Technical refractory ceramics (e.g., Alumina $\text{Al}_2\text{O}_3$, Zirconia $\text{ZrO}_2$) provide exceptional thermal barrier performance at operating temperatures exceeding $1000^\circ\text{C}$ [9].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>11 | Page</i></div>

### 9. High-Speed Rotational Flywheels and Centrifuges
In kinetic energy storage flywheels, medical centrifuge rotor heads, and turbocharger impellers, centrifugal rotation induces severe bi-axial radial and circumferential hoop stresses. For a solid disc of radius $R$ spinning at angular velocity $\omega$:
$$\sigma_{\text{max}} = \left( \frac{3 + \nu}{8} \right) \rho \omega^2 R^2 \le \sigma_y$$
The maximum burst angular velocity before centrifugal bursting is:
$$\omega_{\text{burst}} = \frac{1}{R} \left( \frac{8 \sigma_y}{(3 + \nu) \rho} \right)^{1/2}$$
The kinetic energy stored is $E_k = \frac{1}{2} I \omega^2 = \frac{1}{4} m R^2 \omega^2$. Substituting $\omega_{\text{burst}}$ into $E_k / m$:
$$\frac{E_k}{m} = \left( \frac{2}{3 + \nu} \right) \left( \frac{\sigma_y}{\rho} \right)$$
To maximize stored kinetic energy per unit mass without centrifugal burst fracture, the flywheel performance index to maximize is:
$$M_{13} = \frac{\sigma_y}{\rho}$$
This derivation underscores why high-strength, low-density materials (such as continuous Carbon Fiber Reinforced Polymers and Titanium Ti-6Al-4V) provide outstanding energy storage densities. Conversely, unreinforced monolithic ceramics--despite high compressive strength--must be strictly disqualified due to zero tensile ductility and catastrophic brittle shattering under hoop tension [10].

### 10. Cyclic Alternating Stress and Fatigue Elements
For rotating machine shafts, connecting rods, and railway axles subjected to millions of cyclic stress reversals, failure occurs well below static yield strength due to microcrack nucleation and propagation [11]. The fatigue endurance limit $\sigma_f$ (typically defined at $10^7$ cycles under fully reversed loading, $R = -1$) replaces static yield strength:
$$M_{14} = \frac{\sigma_f}{\rho}$$
Where empirical testing demonstrates that alloy steels (e.g., AISI 4140) maintain endurance ratios $\sigma_f / \sigma_{\text{uts}} \approx 0.45 - 0.50$, whereas printed thermoplastics exhibit low fatigue thresholds and sensitivity to notch concentrations [12].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>12 | Page</i></div>

## 2.4 Multi-Dimensional Material Property Charts

To visualize performance indices across competing materials, Ashby constructed logarithmic property charts [4]. By plotting two fundamental properties on logarithmic axes (e.g., $\log E$ versus $\log \rho$), a performance index equation such as:

$$M = \frac{E^{1/2}}{\rho} \implies \log E = 2 \log \rho + 2 \log M$$

becomes a straight line with a constant slope of $2.0$. Material families (metals, ceramics, polymers, composites) cluster into distinct ellipses on these charts [8].

```
 Log E ───┐
 (GPa)   1000 │                     [ TECHNICAL CERAMICS ]
              │                        Alumina, SiC
          100 │           [ METALS & ALLOYS ]
              │            Steels, Ti, Al      [ CONTINUOUS COMPOSITES ]
           10 │                                   CFRP, GFRP
              │     [ ENGINEERING POLYMERS ]
            1 │       PEEK, POM, PC, PETG
              │     [ ELASTOMERS ]
          0.1 │       TPU, Silicone
              └────────────────────────────────────────────────────────── Log ρ (kg/m^3)
              100                   1,000                 10,000
```
*Figure 2.4.1: Schematic Representation of an Ashby Chart: Modulus ($E$) vs. Density ($\rho$) [4].*

```
 Log σ_y ──┐
 (MPa)   1000 │                                 [ HIGH-STRENGTH ALLOYS ]
              │                                   Ti-6Al-4V, Inconel 718, 4140
          100 │           [ STRUCTURAL POLYMERS ]
              │            POM, PEEK, PETG-CF
           10 │
              │     [ ELASTOMERS & FOAMS ]
            1 │       TPU 95A
              └────────────────────────────────────────────────────────── Log ρ (kg/m^3)
              100                   1,000                 10,000
```
*Figure 2.4.2: Schematic Representation of an Ashby Chart: Yield Strength ($\sigma_y$) vs. Density ($\rho$) [4].*

<div style="page-break-after: always;"></div>

---

<div align="right"><i>13 | Page</i></div>

## 2.5 Environmental Degradation and Operating Kinetics

A profound shortcoming of classical material selection charts is their assumption of ideal, ambient laboratory conditions ($20^\circ\text{C}$, dry air). In actual field deployments, environmental kinetics induce severe mechanical property degradation that alters candidate rankings [13].

### 2.5.1 Hydrolytic Swelling and Moisture Saturation
Polymers placed in aqueous environments absorb moisture through diffusion governed by Fick's Second Law:
$$\frac{\partial C}{\partial t} = D_w \nabla^2 C$$
where $D_w$ is moisture diffusivity. Water molecules disrupt intermolecular hydrogen bonding, acting as internal plasticizers. 
- **Polylactic Acid (PLA):** PLA is an aliphatic polyester prone to hydrolytic cleavage of ester bonds. Empirical immersion testing demonstrates that fully saturated PLA suffers a **28.4% reduction in tensile yield strength** ($\sigma_y$ drops from 55 MPa to 39.4 MPa) and a **7.2% reduction in Young's modulus** within 30 days of river immersion [10, 14]. Consequently, pure PLA must be deterministically disqualified for submerged water-contact components.
- **Glycol-Modified PET (PETG / PETG-CF):** PETG incorporates cyclohexanedimethanol (CHDM) monomer units that hinder crystallization, providing superior hydrophobicity with equilibrium moisture uptake $< 0.2\%$, retaining $> 96\%$ of dry strength in freshwater [14].

### 2.5.2 Ultraviolet Photo-Oxidative Embrittlement
Components exposed to outdoor equatorial sunlight (such as in Kenya, where solar UV irradiance exceeds $1000\,\text{W/m}^2$) undergo severe photo-degradation.
- **Acrylonitrile Butadiene Styrene (ABS):** Solar UV photons ($290 - 350\,\text{nm}$) possess sufficient quantum energy to cleave the unsaturated polybutadiene rubber phase in ABS, causing rapid surface micro-cracking, yellowing, and catastrophic loss of impact toughness ($> 60\%$ drop in Charpy impact strength within 6 months) [15].
- **Acrylonitrile Styrene Acrylate (ASA):** By substituting an acrylic ester elastomer in place of polybutadiene, ASA provides exceptional intrinsic UV stability, retaining $> 90\%$ tensile strength over years of direct tropical exposure [15].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>14 | Page</i></div>

### 2.5.3 Thermal Deflection and Elevated Creep Kinetics
At elevated operating temperatures, materials experience severe stiffness loss and time-dependent plastic strain (creep) [1].
- **Polymer Deflection Limits:** Thermoplastics must never operate above their Heat Deflection Temperature (HDT) measured under flexural load (ISO 75 / ASTM D648). For instance, standard PLA has an HDT of $55^\circ\text{C}$, whereas PEEK maintains structural stiffness up to $152^\circ\text{C}$ (unfilled) and $315^\circ\text{C}$ (carbon reinforced) [16].
- **Metal Creep Rupture:** In metallic alloys operating above their homologous temperature:
  $$T_H = \frac{T_{\text{service}}}{T_{\text{melt}}} \ge 0.40 - 0.50$$
  atomic vacancy diffusion accelerates dislocation climb, leading to tertiary creep rupture. For gas turbine exhaust components operating at $700^\circ\text{C}$, structural steels and aluminum alloys undergo rapid creep failure ($T_H > 0.55$), mandating nickel superalloys (Inconel 718, $T_{\text{melt}} = 1336^\circ\text{C}$) or technical ceramics [17].

### 2.5.4 Sub-Zero Cryogenic Ductile-to-Brittle Transition (DBTT)
In cryogenic service (e.g., liquid nitrogen at $-196^\circ\text{C}$, liquid oxygen at $-183^\circ\text{C}$, liquid hydrogen at $-253^\circ\text{C}$):
- **Ferritic and Body-Centered Cubic (BCC) Steels:** BCC metals (such as AISI 4140 low-alloy steel) exhibit a pronounced Ductile-to-Brittle Transition Temperature (DBTT) typically between $-20^\circ\text{C}$ and $-60^\circ\text{C}$. Below this temperature, dislocation mobility freezes, causing catastrophic cleavage fracture under minimal impact energy [18].
- **Austenitic and Face-Centered Cubic (FCC) Alloys:** FCC crystalline structures (such as AISI 316L stainless steel, Inconel 718, and Aluminum 6061-T6) maintain active slip systems down to absolute zero, displaying increasing yield strength while preserving high fracture toughness ($K_{1c} > 100\,\text{MPa}\sqrt{\text{m}}$) [18].
- **Liquid Oxygen (LOX) Compatibility (NASA-STD-6001):** Under high-pressure liquid oxygen, Titanium alloys undergo violent, exothermic frictional auto-ignition and are strictly barred by aerospace safety codes [19].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>15 | Page</i></div>

## 2.6 Emergence of Computational Materials Informatics

To overcome the manual limitations of 2D charts, computational materials informatics emerged in the late 1990s [20]. Software frameworks such as Cambridge Materials Selector (now Ansys Granta EduPack) digitized materials properties into relational databases [21]. Users can define mathematical filter limits (e.g., $\sigma_y \ge 250\,\text{MPa}$ and $T_{\text{service}} \ge 120^\circ\text{C}$) and generate multi-variable scatter plots.

However, while commercial tools like Granta provide comprehensive property tables, they exhibit significant operational shortcomings in decentralized, educational, and African manufacturing contexts:
1. **High License Costs and Closed Ecosystems:** Granta EduPack licenses cost thousands of dollars annually, preventing adoption across resource-constrained engineering universities and MSME machine shops [22].
2. **Absence of Natural Language Understanding:** The engineer must manually know which mathematical index to construct; the software cannot interpret an unstructured or semi-structured functional design brief [23].
3. **Total Disregard for Supply Chain Sourcing:** The software assumes all materials in its catalog are equally and instantaneously accessible, providing zero insight into local availability, import tariffs, Minimum Order Quantities (MOQ), or shipping lead times [24].

## 2.7 Natural Language Processing and Generative LLMs in Engineering

The introduction of the Transformer architecture by Vaswani et al. in 2017 catalyzed rapid advances in Natural Language Processing (NLP) [25]. Pre-trained Large Language Models (LLMs) trained on billions of text tokens demonstrate remarkable capabilities in code generation, conversational reasoning, and text synthesis [26].

In mechanical engineering, researchers have explored deploying LLMs as interactive design assistants [27]. In 2023, Makatura et al. investigated the capacity of foundation LLMs to assist in computer-aided design and parametric modeling, demonstrating that conversational agents can accelerate preliminary ideation [28]. Similarly, in manufacturing, LLMs have been tested for generating CNC G-code toolpaths and interpreting operational maintenance logs [29].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>16 | Page</i></div>

## 2.8 Hallucination Risks and Continuum Mechanics Failures in Generic LLMs

Despite their linguistic eloquence, deploying generic, ungrounded conversational LLMs for materials selection introduces catastrophic risks in structural engineering [30]. LLMs are probabilistic autoregressive models: they predict the next most likely token based on statistical correlations in their training corpus, rather than solving deterministic physical governing equations [31].

```
┌──────────────────────────────────────────────────────────┐
│             GENERIC AUTOREGRESSIVE LLM QUERY             │
│   "Select material for 150 bar cryogenic oxygen valve"   │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│                 STATISTICAL TOKEN GUESSING               │
│  Matches frequent words: "3D printing", "lightweight"    │
└────────────────────────────┬─────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────┐
│               CATASTROPHIC ENGINEERING FAILURE           │
│  - Recommends PLA or short-fiber PETG-CF (permeable)     │
│  - Invents fictitious yield strength (e.g., 850 MPa)     │
│  - Ignores explosive delamination under 150 bar gas      │
│  - Violates NASA LOX auto-ignition safety standards      │
└──────────────────────────────────────────────────────────┘
```
*Figure 2.8.1: Typical Hallucination Failure Trajectories in Unconstrained Generative LLMs [30].*

Recent empirical benchmark studies by Bano et al. (2024) evaluated GPT-4 on mechanical design problems, revealing that over **42% of numerical property values** cited by the model deviated from certified ASTM datasheets by more than $20\%$, and in multiple instances the model recommended brittle materials for dynamic impact applications [32]. These findings demonstrate that unconstrained generative AI is unsuitable for autonomous engineering decision-making.

## 2.9 Retrieval-Augmented Generation (RAG) and Semantic Vector Indexing

To ground LLMs in verified domain knowledge, Lewis et al. (2020) proposed **Retrieval-Augmented Generation (RAG)** [33]. Instead of relying on internal parametric weights, the system:
1. Chunks certified technical documents into semantically coherent passages.
2. Encodes chunks into dense high-dimensional vector embeddings (e.g., using cosine distance).
3. Stores embeddings in a persistent vector database (such as ChromaDB).
4. At query time, retrieves top-$k$ relevant passages and injects them into the LLM context prompt as authoritative ground truth.

While standard RAG significantly improves factual accuracy in general text summarization, vanilla RAG alone remains insufficient for mechanical material selection: vector similarity searches cannot perform numerical inequality filtering ($\sigma_y \ge 350\,\text{MPa}$) or compute continuous mathematical Ashby indices ($M = \sigma_y^{2/3} / \rho$) [34].

<div style="page-break-after: always;"></div>

---

<div align="right"><i>17 | Page</i></div>

## 2.10 Multi-Tier Dual-Engine AI Architecture

To achieve absolute mathematical reliability while retaining the linguistic synthesis capabilities of generative AI, modern engineering systems are adopting **Neuro-Symbolic Dual-Tier Architectures** [35]. In this paradigm:
- **Tier 1 (Deterministic Symbolic Layer):** A rigid mathematical continuum mechanics engine screens and ranks database candidates according to analytical Ashby formulas, applying hard thermodynamic and degradation gating.
- **Tier 2 (Neural Generative Layer):** A local foundational LLM receives the mathematically verified winning candidates as explicit prompt context, generating structured engineering explanations without the capacity to substitute hallucinated materials.
- **Tier 3 (Cloud Internet Arbitration):** When candidate materials score within a tight competitive margin ($\Delta_{\text{score}} \le 8.0\%$), an automated trigger queries an advanced cloud reasoning engine (e.g., Google Gemini) over the internet to perform multi-objective trade-off arbitration across complex microstructural mechanisms [36].

*Table 2.1: Comparison of General-Purpose LLMs versus Deterministic Selection Engines.*

| Performance Dimension | Generic Commercial LLM (ChatGPT / Claude) | Standard RAG Architecture | Proposed EMS-OS Dual-Tier Engine |
| :--- | :--- | :--- | :--- |
| **Mechanical Constants Provenance** | Probabilistic (Frequent Hallucinations) | Retrieved Text (May cite wrong units) | **Deterministic ASTM/ISO Database Verification** |
| **Continuum Mechanics Equations** | Often Misapplied or Invented | Uncalculated in Vector Space | **Exact Analytical Ashby Performance Indices** |
| **Environmental Degradation Screening** | Inconsistent / Often Ignored | Partial (If chunk retrieved) | **Deterministic Kinetic Degradation Gating** |
| **High-Throughput Database Search** | Restricted to ~10 items | Vector distance only | **Deterministic Screening of 1,490+ Materials** |
| **Supply Chain & EOQ Economics** | Completely Blind | Completely Blind | **Integrated Wilson-Harris EOQ & Lead-Time Modeling** |
| **Data Privacy & Offline Independence** | Cloud-Dependent (Zero Privacy) | Often Cloud-Dependent | **100% Local Foundation (Ollama `llama3.2`)** |
| **Competitive Close-Contender Tie-Break** | Arbitrary Token Output | Unranked | **Automated Internet Gemini Arbitration ($\Delta \le 8\%$)** |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>18 | Page</i></div>

## 2.11 Supply Chain Logistics, Inventory Optimization, and Techno-Economics

In professional mechanical design, material selection is fundamentally an optimization problem balanced between structural performance and manufacturing economics [37]. Specifying an ultra-high-performance material that cannot be reliably sourced or that requires excessive capital commitment is an engineering failure.

### 2.11.1 Classical Wilson-Harris Economic Order Quantity (EOQ)
The total annual inventory cost for procuring a material consists of the purchase cost, order placement setup cost, and inventory holding cost [38]. The classical Wilson-Harris formulation models total annual cost as:
$$\text{TC}(Q) = D \cdot C_m + \frac{D}{Q} S + \frac{Q}{2} H$$
where $D$ is annual demand ($\text{kg/year}$), $C_m$ is material unit price ($\text{USD/kg}$), $S$ is order setup and procurement administration cost ($\text{USD/order}$), $Q$ is order batch size ($\text{kg}$), and $H$ is annual holding carrying cost per kg ($H = i \cdot C_m$, with carrying interest rate $i \approx 0.20$).

Differentiating $\text{TC}(Q)$ with respect to $Q$ and setting the derivative to zero yields the optimal **Economic Order Quantity (EOQ)**:
$$\frac{d\text{TC}}{dQ} = -\frac{D S}{Q^2} + \frac{H}{2} = 0 \implies \text{EOQ} = \sqrt{\frac{2 D S}{H}}$$

```
  Cost ($) ──┐
             │                          Total Inventory Cost TC(Q)
             │                             \             /
             │                              \  EOQ      /
             │                               \   ▼     /
             │   ──────────────────────────────────*────────────────────
             │                                 /       \
             │      Holding Cost (Q/2 * H)   /           \  Ordering Cost (D/Q * S)
             │                             /               \
             └──────────────────────────────────────────────────────────── Order Batch Q (kg)
```
*Figure 2.11.1: Classical Wilson-Harris Economic Order Quantity (EOQ) Cost Curves [38].*

### 2.11.2 Supplier Minimum Order Quantity (MOQ) Constraints
Raw material distributors enforce Minimum Order Quantities ($MOQ$) based on mill production batch limits [39]. 
- If the annual project demand is less than the supplier's minimum threshold ($D < MOQ$), the engineering firm must either purchase excess inventory or pay small-lot distributor premiums.
- The financial carrying penalty for holding surplus stock is quantified as:
  $$\Delta C_{\text{surplus}} = (MOQ - D) \cdot C_m \cdot i$$
This holding penalty severely penalizes specialty imported grades for small-scale projects, favoring locally available commercial bar stock.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>19 | Page</i></div>

### 2.11.3 Sourcing Lead Times and Transit Modeling
Sourcing lead times directly dictate project schedule risk. In Kenya's manufacturing landscape, materials fall into distinct procurement tiers:
1. **Domestic Local Stock:** Readily procurable from industrial distributors in Nairobi and Mombasa (e.g., mild steel, structural hollow sections, commercial 6061-T6 aluminum, standard PLA/PETG filament). Typical lead time: **2 to 5 days** [10].
2. **Regional Import Stock:** Sourced from South Africa, Egypt, or India. Typical lead time: **14 to 21 days**.
3. **Global Maritime Import:** Specialty aerospace-grade alloys, titanium ingots, continuous carbon fiber prepregs, and medical-grade PEEK imported from Europe, the United States, or China. Sourcing incurs maritime transit to the Port of Mombasa, customs clearance, and road freight to Nairobi. Typical lead time: **30 to 60 days** [10, 40].

## 2.12 Multi-Criteria Decision Analysis (MCDA / TOPSIS)

To synthesize disparate physical, environmental, and techno-economic parameters into a unified decision index, Multi-Criteria Decision Analysis (MCDA) techniques--such as the **Technique for Order of Preference by Similarity to Ideal Solution (TOPSIS)**--are widely employed [41]. 

In TOPSIS, candidate alternatives are scored based on their Euclidean geometric distance from an ideal best solution and an ideal worst solution across normalized criteria weights [42]. In the EMS-OS framework, candidates that satisfy all hard continuum mechanics filters are evaluated across a normalized multi-criteria objective function:

$$S_{\text{composite}} = w_{\text{tech}} \cdot S_{\text{ashby}} + w_{\text{cost}} \cdot S_{\text{cost}} + w_{\text{lead}} \cdot S_{\text{lead}} + w_{\text{moq}} \cdot S_{\text{moq}}$$

where $S_{\text{ashby}}$ is the normalized Ashby performance score, $S_{\text{cost}}$ represents material cost efficiency, $S_{\text{lead}}$ penalizes extended transit days, and $S_{\text{moq}}$ reflects ordering batch flexibility.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>20 | Page</i></div>

## 2.13 Summary of Gaps in Existing Literature

A critical synthesis of the reviewed literature reveals four distinct technological and methodological gaps that motivate this capstone research:

1. **Gap 1: Disconnect Between NLP Parsing and Formal Standards:** Existing conversational AI tools parse text using generic linguistic associations rather than formal engineering specifications (ISO, ASTM, ASME). No current open-source tool automatically extracts numerical boundary thresholds ($\sigma_y$, $E$, $\rho$, $T_{\text{max}}$) from structured engineering prompts and directly maps them to governing Ashby continuum mechanics indices.
2. **Gap 2: Lack of Deterministic Provenance in Engineering LLMs:** Current generative AI implementations attempt to produce answers directly from internal neural weights, resulting in frequent hallucinations of mechanical constants and dangerous violations of physical laws. A neuro-symbolic framework that enforces deterministic mathematical calculations and passes verified candidates to the LLM has not been previously implemented for general mechanical material selection.
3. **Gap 3: Complete Absence of Supply Chain and Logistics Integration:** Commercial software (e.g., Granta EduPack) evaluates materials in isolation from procurement economics. No existing platform couples physical Ashby performance scores with classical Wilson-Harris Economic Order Quantity (EOQ), supplier Minimum Order Quantities (MOQ), and realistic shipping transit lead times tailored to developing industrial environments such as Kenya.
4. **Gap 4: Absence of Automated Multi-Tier Cloud Arbitration:** When candidate materials have closely matching performance indices or complex metallurgical trade-offs (e.g., fracture toughness versus stress-corrosion cracking), existing systems either output an arbitrary choice or require extensive manual expert consultation. An automated dual-engine architecture that triggers advanced cloud AI arbitration over the internet only when $\Delta_{\text{score}} \le 8.0\%$ represents a novel contribution to computational design.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>21 | Page</i></div>

# CHAPTER 3: MATERIALS AND METHOD

## 3.1 Design of the Material Selection and Optimization System (EMS-OS)

The proposed EMS-OS platform is designed as an autonomous, deterministic computational system capable of converting structured scientific engineering inquiries into mathematically verified, environmentally vetted, and supply-chain optimized material recommendations.

### 3.1.1 Conceptual Architecture of the EMS-OS Platform
The system operates on a modular, multi-tier software architecture structured into six interconnected functional layers, as illustrated in Figure 3.1.1:

```
[ QUALIFIED MECHANICAL ENGINEER INPUT ]
Structured Technical Specifications, Numerical Limits, ISO/ASTM Codes
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 1. SCIENTIFIC SPECIFICATION PARSER (src/nlp_parser.py) │
│ - Regex Numerical Constraint Extraction (Sy, E, T)     │
│ - Component Classification & Primary Loading Mode      │
│ - International Standard Mapping (ASTM, ISO, ASME)     │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 2. STANDARDIZED MATERIALS CATALOG (src/materials_db.py)│
│ - 1,490+ Standardized Engineering Materials            │
│ - Metals, Polymers, Composites, Technical Ceramics     │
│ - Physical, Thermal, Environmental & Economic Fields   │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 3. ANALYTICAL ASHBY ENGINE (src/ashby_engine.py)       │
│ - Exact Performance Indices: M = Sy/rho, E^(1/2)/rho   │
│ - Hard Boundary Gating: T_service < HDT, DBTT, LOX     │
│ - Kinetic Environmental Penalties (Hydrolysis, UV)     │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 4. SUPPLY CHAIN OPTIMIZER (src/economics_engine.py)    │
│ - Wilson-Harris Economic Order Quantity (EOQ)          │
│ - Minimum Order Quantity (MOQ) Surplus Penalty         │
│ - Domestic vs. Maritime Port Lead-Time Modeling        │
│ - TOPSIS Multi-Criteria Composite Scoring Leaderboard  │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 5. MULTI-ENGINE ORCHESTRATOR (src/llm_orchestrator.py) │
│ - Foundation: Local Standalone LLM (llama3.2 / Ollama) │
│ - Close Contender Detection (Delta_score <= 8.0%)      │
│ - Cloud Internet Tie-Breaker: Google Gemini API        │
│ - 6-Phase Transparent Chain-of-Thought Decision Log    │
└───────────────────┬────────────────────────────────────┘
                    │
                    ▼
┌────────────────────────────────────────────────────────┐
│ 6. USER INTERFACE & REPORTING (app.py & cli.py)        │
│ - Responsive Streamlit UI & Command-Line Interface     │
│ - Dynamic 2D/3D Plotly Ashby Property Scatter Charts   │
│ - Real-Time Ollama Local Daemon Health Telemetry       │
│ - Downloadable ISO/ASTM Markdown Engineering Report    │
└────────────────────────────────────────────────────────┘
```
*Figure 3.1.1: Complete System Architecture of the Proposed EMS-OS Platform.*

<div style="page-break-after: always;"></div>

---

<div align="right"><i>22 | Page</i></div>

### 3.1.1.1 System Functional Specifications and Design Requirements
To ensure the EMS-OS platform satisfies the rigorous demands of professional mechanical engineering design and educational instruction, the system is engineered against explicit functional requirements detailed in Table 3.1.

*Table 3.1: Target Functional Specifications and Operating Envelopes for EMS-OS.*

| # | System Parameter | Engineering Specification Target | Validation Metric / Tolerance |
| :---: | :--- | :--- | :--- |
| **1** | **Input Interface** | Structured scientific technical inquiries with support for numerical units | Extraction accuracy $\ge 95\%$ across standard engineering prompts |
| **2** | **Standards Compliance** | Mapping of ASTM, ISO, ASME Section VIII, and DIN codes | Accurate classification of regulatory constraints |
| **3** | **Database Scale** | $\ge 1,400$ verified industrial engineering materials | Unified JSON schema with zero missing physical constants |
| **4** | **Analytical Accuracy** | Deterministic calculation of 12 primary Ashby performance indices | Relative difference $\text{rel\_diff} \le 10^{-4}$ against exact formulas |
| **5** | **Environmental Gating** | Hard elimination of materials exceeding HDT, melting creep, or DBTT | Zero temperature violations; automatic moisture/UV penalties |
| **6** | **Supply Chain Sourcing** | Calculation of EOQ, MOQ penalties, and transport transit lead times | Full Wilson-Harris batch optimization for annual demand $D$ |
| **7** | **Multi-Tier Orchestration** | 100% offline local foundation LLM (`llama3.2` via Ollama) | Zero mandatory cloud reliance for standard operations |
| **8** | **Cloud Arbitration** | Automated trigger to Google Gemini API when contender $\Delta \le 8.0\%$ | Complete chain-of-thought logging with internet attribution |
| **9** | **User Interface** | Interactive Streamlit web dashboard and standalone CLI | Sub-second Ashby chart rendering; real-time Ollama telemetry |
| **10** | **Execution Speed** | Full deterministic ranking in $< 1.5$ seconds on local hardware | High-throughput multi-material screening efficiency |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>23 | Page</i></div>

### 3.1.1.2 Iterative Development and Enhancements from Previous Prototype
The proposed EMS-OS represents a comprehensive architectural overhaul of earlier material selection experiments conducted within the Department of Mechanical and Manufacturing Engineering. Table 3.2 delineates the key technological advancements introduced in this research.

*Table 3.2: Comparative Upgrades from Previous Prototype to Current EMS-OS.*

| System Feature | Previous University of Nairobi Prototype [10] | Improved EMS-OS Platform (Current Project) |
| :--- | :--- | :--- |
| **Target User Base** | Colloquial non-technical layman inquiries | Qualified mechanical design engineers |
| **Input Parsing Engine** | Naive keyword string matching | Rule-based regex + Trained pure-numpy intent model |
| **Database Size** | $< 20$ common polymers and basic alloys | **1,490+ standardized materials** (ANSI, ISO, DIN, JIS) |
| **Ashby Formulations** | Static hardcoded lookup values | **Dynamic calculation from first principles ($M = \sigma_y / \rho$, etc.)** |
| **Environmental Degradation** | Not modeled | **Empirical hydrolysis drops (PLA $-28.4\%$), UV, HDT, DBTT** |
| **LLM Orchestration** | Simulated offline dummy text / static mocks | **Real local foundation LLM (`llama3.2` via Ollama)** |
| **Ambiguity Resolution** | None (Output first match) | **Automated Cloud Gemini tie-breaker arbitration ($\Delta \le 8\%$)** |
| **Chain-of-Thought Logging** | Hidden / Opaque output | **Transparent 6-phase engineering reasoning trace** |
| **Supply Chain Economics** | Completely absent | **Wilson-Harris EOQ, MOQ penalties, road vs. sea lead times** |
| **Visualization & Reporting** | Static text strings | **Interactive 2D/3D Plotly property charts & Markdown reports** |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>24 | Page</i></div>

### 3.1.1.3 Modular Subsystems of the EMS-OS Pipeline

The software pipeline comprises six modular subsystems operating sequentially:

```
[ Scientific Prompt ]
         │
         ▼
[ Phase 1: Scientific Specification & Loading Analysis ] ─── NLP Translation Layer
         │
         ▼
[ Phase 2: Database Screening & Boundary Constraint Elimination ] ─── Ashby Hard Gating
         │
         ▼
[ Phase 3: Quantitative Ashby Performance Scoring ] ─── Analytical Mathematical Formulas
         │
         ▼
[ Phase 4: Techno-Economic & Sourcing Optimization ] ─── Wilson-Harris EOQ & Lead Times
         │
         ▼
[ Phase 5: Close Contender Detection & Decisiveness Assessment ] ─── Delta_score <= 8.0%
         │
         ├────────────────────────────────────────┬───────────────────────────────────────┐
         │ If Score Delta > 8.0%                  │ If Score Delta <= 8.0%                │
         ▼                                        ▼                                       ▼
[ Primary Candidate Decisive ]           [ Connect to Internet / Cloud Gemini API ] ─── Tier 3
         │                                        │
         └───────────────────┬────────────────────┘
                             │
                             ▼
[ Phase 6: Grounded Local Ollama Synthesis & Reporting ] ─── Tier 1 Foundation LLM
```
*Figure 3.1.2: Six-Phase Transparent Chain-of-Thought Decision Flowchart.*

#### 1. Scientific Specification Parser Subsystem (`src/nlp_parser.py`)
The parser accepts structured mechanical engineering specifications. It utilizes a hybrid neuro-symbolic approach:
- **Numerical Regular Expression Extraction:** Automatically parses operating temperatures ($T$), operating pressures ($P$), dimensional bounds (length $L$, chord $c$), and flow velocities ($v$).
- **Component Classification:** Categorizes the inquiry into standardized engineering classes (e.g., `tensile_tie`, `bending_beam`, `shell_plate`, `rotational_rotor`, `pressure_vessel_or_containment`, `elastic_spring`, `thermal_conductor`, `friction_gear`, `surgical_implant`).
- **Standards & Constraint Binding:** Detects explicit references to ISO, ASTM, ASME Section VIII, and NASA LOX standards, asserting boolean environmental boundary flags (`submerged_aquatic_exposure`, `outdoor_uv_exposure`, `is_cryogenic`, `biocompatible_implant_required`).

<div style="page-break-after: always;"></div>

---

<div align="right"><i>25 | Page</i></div>

#### 2. Standardized High-Throughput Materials Catalog (`src/materials_db.py`)
The database module loads and normalizes [`data/materials_catalog.json`](file:///c:/Users/jeffm/Desktop/university%20projects/Material%20selection%20LLM/data/materials_catalog.json), housing 1,490 standardized engineering materials. Each record maintains unified SI units:
- **Mechanical Properties:** Young's Modulus $E$ ($\text{GPa}$), Shear Modulus $G$ ($\text{GPa}$), Yield Strength $\sigma_y$ ($\text{MPa}$), Ultimate Tensile Strength $\sigma_{\text{uts}}$ ($\text{MPa}$), Elongation at Break ($\%$), Fracture Toughness $K_{1c}$ ($\text{MPa}\sqrt{\text{m}}$), Mass Density $\rho$ ($\text{kg/m}^3$).
- **Thermal Properties:** Thermal Conductivity $\lambda$ ($\text{W/(m}\cdot\text{K)}$), Specific Heat $C_p$ ($\text{J/(kg}\cdot\text{K)}$), Coefficient of Thermal Expansion $\alpha_L$ ($\mu\text{m/(m}\cdot\text{K)}$), Melting Point $T_{\text{melt}}$ ($^\circ\text{C}$), Heat Deflection Temperature $T_{\text{HDT}}$ ($^\circ\text{C}$).
- **Degradation Attributes:** Water saturation tensile drop ($\%$), moisture modulus drop ($\%$), UV degradation susceptibility rating, biocompatibility clearance (ISO 10993), and FDA food contact status.
- **Techno-Economic Attributes:** Baseline raw material cost $C_m$ ($\text{USD/kg}$), default supplier Minimum Order Quantity $MOQ$ ($\text{kg}$), and sourcing category (`Domestic`, `Regional`, `Global Import`).

#### 3. Analytical Ashby Mechanics Selection Engine (`src/ashby_engine.py`)
The Ashby engine executes deterministic screening in two discrete stages:
1. **Hard Physical Boundary Elimination:** 
   - Disqualifies materials whose maximum service temperature or $T_{\text{HDT}}$ is exceeded by the operating temperature ($T_{\text{service}} \ge T_{\text{limit}}$).
   - Enforces metal creep rupture gating ($T_H = T_{\text{service}} / T_{\text{melt}} < 0.55$).
   - Disqualifies ferritic/BCC steels below their Ductile-to-Brittle Transition Temperature ($T_{\text{service}} < -40^\circ\text{C}$).
   - Disqualifies Titanium in high-pressure liquid oxygen environments per NASA-STD-6001.
   - Disqualifies brittle monolithic technical ceramics from high-speed rotational machinery (flywheels, turbine wheels, impellers) due to catastrophic tensile centrifugal bursting.
2. **Dynamic Quantitative Index Scoring:**
   - Evaluates the candidate against the governing analytical Ashby performance index derived for the active loading mode ($M = \sigma_y / \rho$, $E^{1/2}/\rho$, $E^{1/3}/\rho$, $\sigma_y^2 / E$, etc.).
   - Multiplies raw index values by validated kinetic degradation factors (hydrolytic saturation, outdoor equatorial UV exposure, corrosive mineral acid exposure).
   - Sorts surviving materials in descending order of performance metric.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>26 | Page</i></div>

#### 4. Supply Chain and Techno-Economic Optimizer (`src/economics_engine.py`)
The economics engine converts theoretical mechanical rankings into actionable procurement decisions. For an annual component demand $D$ ($\text{kg/year}$):
- **Wilson-Harris EOQ Calculation:** Computes the optimal procurement batch quantity $\text{EOQ} = \sqrt{2DS / H}$.
- **MOQ Penalty Assessment:** If $D < MOQ$, computes the financial carrying penalty of surplus holding: $\Delta C_{\text{surplus}} = (MOQ - D) \cdot C_m \cdot i$.
- **Logistics Transit Modeling:** Assigns verified transit durations based on sourcing tier:
  - Domestic Local Warehouse: $L = 2 - 5\,\text{days}$
  - Regional Stock: $L = 14 - 21\,\text{days}$
  - Global Ocean Freight (via Port of Mombasa): $L = 30 - 60\,\text{days}$
- **Multi-Criteria Composite Scoring:** Computes a normalized composite score ($0$ to $100$) balancing Ashby performance, material cost, transit lead-time risk, and ordering batch flexibility.

#### 5. Multi-Engine Dual-Tier Orchestrator (`src/llm_orchestrator.py`)
The orchestrator coordinates inference and prevents AI hallucinations:
- **Local Foundation Engine (Tier 1):** Utilizes `llama3.2:latest` running locally via Ollama on `http://127.0.0.1:11434`. The orchestrator injects the exact Ashby winning candidate, mechanical properties, and runner-up metrics directly into the prompt context, commanding the LLM to formulate its structural integrity analysis and manufacturing directives around the mathematically optimal material.
- **Close-Contender Detection:** Computes the percentage performance gap between the top two ranked materials:
  $$\Delta_{\text{score}} = \frac{|\text{Score}_1 - \text{Score}_2|}{\text{Score}_1} \times 100\%$$
- **Automated Cloud Internet Arbitration (Tier 3):** If $\Delta_{\text{score}} \le 8.0\%$, the orchestrator automatically establishes a secure internet connection to the Google Cloud Gemini API (`gemini-2.5-flash` or `gemini-1.5-pro`). The cloud engine evaluates complex metallurgical trade-offs (e.g., stress corrosion cracking, fatigue notch sensitivity, microstructural phase stability) and appends an audited arbitration log to the final report.
- **Transparent Chain-of-Thought Logging:** Records detailed telemetry across all six decision phases, exposing the system's reasoning in both the CLI and web dashboard.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>27 | Page</i></div>

```
┌────────────────────────────────────────────────────────┐
│             CLOSE CONTENDER DETECTION CHECK            │
│   Delta_score = (|Score_1 - Score_2| / Score_1) * 100   │
└───────────────────────────┬────────────────────────────┘
                            │
              Is Delta_score <= 8.0% ?
              /                      \
            YES                       NO
            /                          \
           ▼                            ▼
┌───────────────────────────┐  ┌───────────────────────────┐
│ AUTOMATIC CLOUD TRIGGER   │  │ DECISIVE SELECTION        │
│ Connect via Internet to   │  │ Rank 1 Candidate satisfies│
│ Google Cloud Gemini API   │  │ criteria decisively       │
└─────────────┬─────────────┘  └─────────────┬─────────────┘
              │                              │
              ▼                              │
┌───────────────────────────┐                │
│ MULTI-OBJECTIVE ANALYSIS  │                │
│ - Fatigue Notch Sens.     │                │
│ - Stress Corrosion Crack. │                │
│ - Supply Chain Risks      │                │
└─────────────┬─────────────┘                │
              │                              │
              ▼                              │
┌───────────────────────────┐                │
│ AUDITED ARBITRATION LOG   │                │
│ Appended to Final Report  │                │
└─────────────┬─────────────┘                │
              │                              │
              └──────────────┬───────────────┘
                             │
                             ▼
┌────────────────────────────────────────────────────────┐
│             FINAL SYNTHESIZED DECISION REPORT          │
│   Recommended Material, Comparison Table, Directives,  │
│   Techno-Economic Sourcing & Availability Ranking      │
└────────────────────────────────────────────────────────┘
```
*Figure 3.1.3: Automatic Cloud AI (Gemini) Tie-Breaker Arbitration Workflow.*

#### 6. Interactive User Interface and Automated Reporting (`app.py` & `cli.py`)
- **Streamlit Web Application (`app.py`):** Features an interactive web dashboard with an Ad-Hoc Material Explorer, dynamic 2D and 3D Plotly property scatter charts, real-time Ollama daemon connection monitoring, and instant PDF/Markdown engineering specification report export.
- **Standalone Command-Line Interface (`cli.py`):** Enables headless, terminal-based engineering execution suitable for integration into automated CAD/CAE workflows.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>28 | Page</i></div>

## 3.2 Design Formulae and Mathematical Formulations

The EMS-OS engine encodes explicit continuum mechanics governing equations derived from first principles.

### 3.2.1 Analytical Ashby Performance Indices
The primary performance indices to be maximized for lightweight structural components are formulated as follows:

1. **Axial Tensile Stiffness per Unit Mass (Ties, Trusses, Cords):**
   $$M_1 = \frac{E}{\rho} \quad \left[\frac{\text{GPa}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (1)$$

2. **Axial Tensile Strength per Unit Mass (Ties, Cables, Hydraulic Shells):**
   $$M_2 = \frac{\sigma_y}{\rho} \quad \left[\frac{\text{MPa}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (2)$$

3. **Flexural Bending Stiffness per Unit Mass (Beams, Spars, Booms):**
   $$M_3 = \frac{E^{1/2}}{\rho} \quad \left[\frac{\text{GPa}^{1/2}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (3)$$

4. **Flexural Bending Strength per Unit Mass (Beams, Chassis Rails):**
   $$M_4 = \frac{\sigma_y^{2/3}}{\rho} \quad \left[\frac{\text{MPa}^{2/3}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (4)$$

5. **Plate Flexural Bending Stiffness per Unit Mass (Fairings, Skins):**
   $$M_5 = \frac{E^{1/3}}{\rho} \quad \left[\frac{\text{GPa}^{1/3}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (5)$$

6. **Plate Impact Puncture and Yield Strength per Unit Mass (Armor Plates):**
   $$M_6 = \frac{\sigma_y^{1/2}}{\rho} \quad \left[\frac{\text{MPa}^{1/2}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (6)$$

7. **Torsional Shaft Stiffness per Unit Mass (Drive Axles, Spindles):**
   $$M_7 = \frac{G^{1/2}}{\rho} \quad \left[\frac{\text{GPa}^{1/2}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (7)$$

8. **Torsional Shaft Strength per Unit Mass (Torque Transmission):**
   $$M_8 = \frac{\tau_y^{2/3}}{\rho} \approx \frac{(0.577 \sigma_y)^{2/3}}{\rho} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (8)$$

9. **Elastic Strain Energy Storage per Unit Volume (Springs, Dampers):**
   $$M_9 = \frac{\sigma_y^2}{E} \quad \left[\frac{\text{MPa}^2}{\text{GPa}} = \text{kJ/m}^3\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (9)$$

<div style="page-break-after: always;"></div>

---

<div align="right"><i>29 | Page</i></div>

10. **Steady-State Thermal Conduction Dissipation (Heat Sinks, Fins):**
    $$M_{10} = \lambda \quad \left[\frac{\text{W}}{\text{m}\cdot\text{K}}\right] \quad \text{or} \quad M_{10b} = \frac{\lambda}{\rho} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (10)$$

11. **Thermal Barrier Insulation (Kiln Linings, Ablative Shields):**
    $$M_{11} = \frac{1}{\lambda} \quad \left[\frac{\text{m}\cdot\text{K}}{\text{W}}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (11)$$

12. **High-Cycle Dynamic Fatigue Efficiency ($10^7$ Cycles Endurance):**
    $$M_{12} = \frac{\sigma_f}{\rho} \quad \left[\frac{\text{MPa}}{\text{Mg/m}^3}\right] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (12)$$

### 3.2.2 Environmental Degradation Penalty Formulations
When environmental exposure flags are asserted by the parser, mechanical properties are penalized before computing performance metrics:

1. **Freshwater Submersion Hydrolysis Drop:**
   $$\sigma_{y,\text{submerged}} = \sigma_y \cdot \left( 1 - \frac{\delta_{\text{tensile\_drop}}}{100} \right) \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (13)$$
   $$E_{\text{submerged}} = E \cdot \left( 1 - \frac{\delta_{\text{modulus\_drop}}}{100} \right) \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (14)$$

2. **Thermal Homologous Temperature Gating:**
   $$T_H = \frac{T_{\text{service}} + 273.15}{T_{\text{melt}} + 273.15} \le 0.55 \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (15)$$

3. **Thermoplastic Heat Deflection Temperature (HDT) Limit:**
   $$T_{\text{service}} < T_{\text{HDT}} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (16)$$

<div style="page-break-after: always;"></div>

---

<div align="right"><i>30 | Page</i></div>

### 3.2.3 Incoterms 2020 Total Landed Cost (TLC) and Stochastic Sourcing Formulations
To model realistic engineering procurement for African and international manufacturing environments (with baseline delivered destination at Nairobi via Kilindini Harbour, Port of Mombasa):

1. **Incoterms 2020 Total Landed Cost (TLC) from Origin to Delivered Duty Paid (DDP):**
   The landed cost per kilogram $C_{\text{DDP}}$ for any imported engineering stock is:
   $$C_{\text{DDP}} = C_{\text{CIF}} + \text{Tariff}_{\text{EAC\_CET}} + \text{IDF} + \text{RDL} + \text{VAT} + \text{Port}_{\text{THC}} + \text{Inland}_{\text{SGR}} + \text{Clearance}_{\text{broker}} \quad \dots\dots (17)$$
   where:
   $$C_{\text{CIF}} = C_{\text{EXW}} \cdot \gamma_{\text{form}} + C_{\text{ocean/freight}} + C_{\text{marine\_ins}} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (18)$$
   - $\gamma_{\text{form}}$ is the form factor multiplier ($\gamma = 1.0$ for standard ingot/billet, $1.15$ for rolled sheet/plate, $1.30$ for precision bar, $2.20$ for FDM filament, $4.50$ for gas-atomized AM powder).
   - $\text{Tariff}_{\text{EAC\_CET}}$ is East African Community Common External Tariff (0% raw ingots, 10% semi-finished bars/shapes, 25% finished engineering polymers/components).
   - $\text{IDF} = 0.035 \times C_{\text{CIF}}$ (Import Declaration Fee).
   - $\text{RDL} = 0.020 \times C_{\text{CIF}}$ (Railway Development Levy).
   - $\text{VAT} = 0.16 \times (C_{\text{CIF}} + \text{Tariff} + \text{IDF} + \text{RDL})$.
   - $\text{Port}_{\text{THC}} + \text{Inland}_{\text{SGR}} + \text{Clearance} = \$0.42/\text{kg}$ (Fixed Mombasa Kilindini terminal handling, standard gauge rail haulage to Nairobi ICD, and customs clearance).

2. **Silver-Pyke-Peterson Stochastic Lead Time and Safety Stock Model:**
   Because international freight transit experiences stochastic delays, safety stock $SS$ is governed by demand variance $\sigma_d^2$ and lead-time variance $\sigma_L^2$:
   $$SS = z_\alpha \sqrt{\mu_L \sigma_d^2 + d^2 \sigma_L^2} \quad [\text{kg}] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (19)$$
   where $z_\alpha$ is the normal inverse cumulative distribution factor for service level $\alpha = 95\%$ ($z_{0.95} = 1.645$), $\mu_L$ is mean lead time (days), and $d$ is average daily consumption ($d = D / 365$). Total effective procurement lead time is:
   $$L_{\text{effective}} = \mu_L + \frac{SS}{d} = \mu_L + z_\alpha \sqrt{\mu_L \left(\frac{\sigma_d}{d}\right)^2 + \sigma_L^2} \quad [\text{days}] \quad \dots\dots\dots\dots\dots\dots (20)$$

3. **Wilson-Harris Economic Order Quantity (EOQ) with Shelf-Life Upper Bounds:**
   The economic order quantity is constrained by resin/prepreg shelf-life horizon $\tau_{\text{shelf}}$:
   $$\text{EOQ}^* = \min\left( \sqrt{\frac{2 \cdot D \cdot S}{i \cdot C_{\text{DDP}}}}, \; D \cdot \frac{\tau_{\text{shelf}}}{365} \right) \quad [\text{kg}] \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (21)$$
   where annual carrying charge rate $i = 0.22$, and ordering administrative setup cost $S = \$75.00$ (domestic) or $\$350.00$ (overseas letter of credit and inspection).

4. **Kraljic Portfolio Matrix Classification:**
   Candidate materials are systematically segmented into four strategic supply quadrants based on annual spend impact ($D \times C_{\text{DDP}}$) and supply market vulnerability ($L_{\text{effective}}$ & regional availability):
   - **Strategic** (High Spend, High Supply Risk): Carbon fiber prepregs, PEEK, Inconel 718.
   - **Bottleneck** (Low Spend, High Supply Risk): Optical-grade polycarbonate sheet, titanium fasteners, biomedical implant stock.
   - **Leverage** (High Spend, Low Supply Risk): Structural mild steel AISI 1018, standard Aluminum 6061-T6.
   - **Routine** (Low Spend, Low Supply Risk): Extrusion PLA, commodity polypropylene, standard brass bar stock.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>31 | Page</i></div>

### 3.2.4 Multi-Criteria Vector-Normalized TOPSIS Optimization Model
To resolve trade-offs between mechanical Ashby efficiency, landed procurement cost, freight lead times, and availability without subjective heuristic scoring, EMS-OS applies the **Technique for Order Preference by Similarity to Ideal Solution (TOPSIS)**:

1. **Evaluation Decision Matrix ($X_{m \times n}$):**
   For $m$ physically admissible candidate materials surviving Stage 1 boolean physical gating across $n = 4$ criteria:
   - $C_1$: Primary Ashby Mechanical Index $M$ (Benefit criterion, weight $w_1 = 0.40$).
   - $C_2$: Total Landed DDP Cost $C_{\text{DDP}}$ in USD/kg (Cost criterion, weight $w_2 = 0.30$).
   - $C_3$: Effective Lead Time $L_{\text{effective}}$ in days including safety stock (Cost criterion, weight $w_3 = 0.15$).
   - $C_4$: Batch Feasibility and Availability Ratio $D / \max(D, \text{MOQ})$ (Benefit criterion, weight $w_4 = 0.15$).

2. **Vector Normalization (Euclidean Column Scaling):**
   $$r_{ij} = \frac{x_{ij}}{\sqrt{\sum_{k=1}^m x_{kj}^2}}, \quad i = 1, \dots, m; \quad j = 1, \dots, n \quad \dots\dots\dots\dots\dots\dots\dots\dots (22)$$

3. **Weighted Normalized Decision Matrix:**
   $$v_{ij} = w_j \cdot r_{ij}, \quad \text{where } \sum_{j=1}^n w_j = 1.0 \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (23)$$

4. **Identification of Ideal ($A^*$) and Negative-Ideal ($A^-$) Solutions:**
   $$A^* = \left\{ \max_i(v_{i1}), \; \min_i(v_{i2}), \; \min_i(v_{i3}), \; \max_i(v_{i4}) \right\} = \left\{ v_1^*, v_2^*, v_3^*, v_4^* \right\} \quad \dots\dots (24)$$
   $$A^- = \left\{ \min_i(v_{i1}), \; \max_i(v_{i2}), \; \max_i(v_{i3}), \; \min_i(v_{i4}) \right\} = \left\{ v_1^-, v_2^-, v_3^-, v_4^- \right\} \quad \dots\dots (25)$$

5. **Euclidean Distance Metrics and Relative Closeness Coefficient:**
   $$S_i^* = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^*)^2}, \qquad S_i^- = \sqrt{\sum_{j=1}^n (v_{ij} - v_j^-)^2} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots (26)$$
   The final relative closeness score $C_i^*$ (ranging from $0.000$ to $1.000$) determines the absolute engineering leaderboard rank:
   $$C_i^* = \frac{S_i^-}{S_i^* + S_i^-} \quad \dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots\dots (27)$$

*Table 3.3: Summary of Governing Mathematical Formulae in the EMS-OS Framework.*

| Equation Designation | Description of Physical Law / Economic Model | Mathematical Expression |
| :---: | :--- | :--- |
| **Eq. (1) & (2)** | Axial Tensile Stiffness and Strength Indices | $M = E / \rho$ & $M = \sigma_y / \rho$ |
| **Eq. (3) & (4)** | Flexural Beam Bending Stiffness and Strength | $M = E^{1/2} / \rho$ & $M = \sigma_y^{2/3} / \rho$ |
| **Eq. (5) & (6)** | Plate Bending Stiffness and Yield Resistance | $M = E^{1/3} / \rho$ & $M = \sigma_y^{1/2} / \rho$ |
| **Eq. (9)** | Elastic Reversible Strain Energy Density | $M = \sigma_y^2 / E$ |
| **Eq. (10) & (11)** | Thermal Conduction and Insulation Indices | $M = \lambda / \rho$ & $M = 1 / \lambda$ |
| **Eq. (13) & (14)** | Moisture Saturation Hydrolytic Degradation | $\sigma_{y,\text{eff}} = \sigma_y (1 - \delta_{\text{tensile}}/100)$ |
| **Eq. (15) & (16)** | Creep Homologous and HDT Thermal Limits | $T_H < 0.55$ and $T_{\text{service}} < T_{\text{HDT}}$ |
| **Eq. (17) & (18)** | Incoterms 2020 Total Landed Cost (DDP Mombasa) | $C_{\text{DDP}} = C_{\text{CIF}} + \text{Tariff} + \text{Levies} + \text{VAT} + \text{Inland}$ |
| **Eq. (19) & (20)** | Silver-Pyke-Peterson Stochastic Safety Stock | $SS = z_\alpha \sqrt{\mu_L \sigma_d^2 + d^2 \sigma_L^2}, \quad L_{\text{eff}} = \mu_L + SS/d$ |
| **Eq. (21)** | Wilson-Harris EOQ with Shelf-Life Limit | $\text{EOQ}^* = \min\left( \sqrt{2DS/(i C_{\text{DDP}})}, \; D \tau_{\text{shelf}}/365 \right)$ |
| **Eq. (22) - (27)** | Hwang-Yoon Vector-Normalized TOPSIS Model | $C_i^* = S_i^- / (S_i^* + S_i^-), \quad r_{ij} = x_{ij}/\sqrt{\sum x_{kj}^2}$ |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>32 | Page</i></div>

## 3.3 Software Implementation and Computational Stack

The EMS-OS platform is implemented in Python 3.11, leveraging a high-performance, open-source computational stack designed for low-latency desktop execution. Table 3.4 details the primary libraries and software dependencies.

*Table 3.4: Software Dependencies and System Libraries.*

| Software Component | Version | Functional Role in System Architecture |
| :--- | :--- | :--- |
| **Python** | 3.11.9 | Core programming runtime and algorithmic execution |
| **Streamlit** | 1.45.1 | Reactive web frontend, reactive state management, and parameter controls |
| **Plotly** | 5.24.1 | Interactive 2D and 3D logarithmic Ashby property scatter chart rendering |
| **Ollama** | 0.5.4 | Embedded local LLM daemon managing open-weights `llama3.2:latest` |
| **Google GenAI SDK** | 1.0.0+ | Secure cloud API interface for Gemini tie-breaker arbitration |
| **ChromaDB** | 0.6.3 | Persistent semantic vector database for domain-specific technical RAG |
| **NumPy** | 1.26.4 | Vectorized continuum mechanics array operations and intent model math |
| **Pandas** | 2.2.3 | High-throughput tabular manipulation of the 1,490+ materials catalog |

### Software Workflow Execution
1. The user launches the application via terminal command (`streamlit run app.py` or `python cli.py --prompt "..."`).
2. The system queries the local Ollama daemon at `http://127.0.0.1:11434` to verify model availability (`llama3.2:latest`). If unavailable, an automated diagnostic alert is presented.
3. The specification parser translates the prompt into a structured JSON configuration.
4. ChromaDB vector storage searches chunked markdown engineering datasheets stored in `knowledge_base/` for relevant physical boundary context.
5. The Ashby engine screens all 1,490 materials, eliminating non-viable candidates and scoring survivors.
6. The economics engine evaluates EOQ and logistics lead times for annual demand $D$.
7. Close contenders ($\Delta \le 8.0\%$) trigger automated Gemini cloud arbitration.
8. The local Ollama LLM synthesizes the final report grounded in the verified Ashby winner.
9. Interactive Plotly charts plot candidate materials across logarithmic property axes.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>33 | Page</i></div>

```
┌────────────────────────────────────────────────────────┐
│                   STREAMLIT WEB DASHBOARD              │
│    Active Model: Local Ollama (llama3.2)  ● Connected  │
├───────────────────────────┬────────────────────────────┤
│   ENGINEERING PROMPT      │     ASHBY 2D SCATTER PLOT  │
│ [ High-pressure cryogenic │ Log E ──┐                  │
│   LOX valve housing...  ] │         │  * Inconel 718   │
│                           │         │  * 316L          │
│ Annual Demand: 1,500 kg   │         └────────── Log ρ  │
├───────────────────────────┴────────────────────────────┤
│ 6-PHASE CHAIN-OF-THOUGHT LOGGING TRACE (Expandable)    │
│ Phase 1: Specification Parsing -> Hoop Stress Contain. │
│ Phase 2: Elimination -> Disqualified 4140 (DBTT < -40) │
│ Phase 3: Ashby Scoring -> Top Rank: Inconel 718        │
│ Phase 4: Sourcing -> EOQ: 1,304 kg, Sea Freight 42d    │
│ Phase 5: Decisiveness -> Winner decisive (Delta > 8%)  │
│ Phase 6: Synthesis -> Synthesized with local Ollama    │
├────────────────────────────────────────────────────────┤
│ TECHNO-ECONOMIC LEADERBOARD & REPRODUCIBILITY TABLE    │
│ Rank | Material | Ashby | Cost | Lead | EOQ | Composite │
│  1   | Inconel  | 1.00  | $6.0 | 42d  | 1304|   81.7   │
│  2   | 316L SS  | 1.00  | $6.0 | 42d  | 1304|   81.7   │
└────────────────────────────────────────────────────────┘
```
*Figure 3.3.1: Wireframe Schematic of the Interactive Streamlit User Interface and Dynamic Visualizer.*

## 3.4 Data Acquisition and Materials Catalog Curation

To ensure high-throughput screening across industrial material classes, a standardized catalog of **1,490 distinct engineering materials** was compiled and normalized into [`data/materials_catalog.json`](file:///c:/Users/jeffm/Desktop/university%20projects/Material%20selection%20LLM/data/materials_catalog.json).

### Data Ingestion and Cleansing Protocol
1. **Source Cross-Verification:** Raw properties were extracted from peer-reviewed material science literature, manufacturer certified Material Data Sheets (MDS), and open engineering catalogs (MatWeb, Autodesk Material Library, ASM International Handbooks).
2. **Standardization of International Designations:** Material keys were unified to map equivalent specifications across American (ANSI/ASTM/AISI), European (DIN/EN), International (ISO), and Japanese (JIS) standards (e.g., AISI 316L $\leftrightarrow$ DIN 1.4404 $\leftrightarrow$ ISO X2CrNiMo17-12-2 $\leftrightarrow$ JIS SUS316L).
3. **Imputation of Missing Constants:** Where specific shear moduli ($G$) were unlisted, isotropic elasticity relations were applied: $G = \frac{E}{2(1 + \nu)}$, adopting certified Poisson's ratios ($\nu \approx 0.28 - 0.33$ for structural alloys, $\nu \approx 0.38 - 0.42$ for polymers).
4. **Schema Enforcement:** Every record is validated against a strict JSON schema guaranteeing non-null floating-point entries for $\rho$, $E$, $\sigma_y$, $\sigma_{\text{uts}}$, and $T_{\text{melt}}$.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>34 | Page</i></div>

## 3.5 Performance Testing and Experimental Verification

To evaluate system efficacy and quantify improvements over baseline methods, the EMS-OS platform will be subjected to comprehensive comparative testing and quantitative verification.

### 3.5.1 Experimental Setup and 3-Way Comparative Benchmark
The system will be tested across a curated test suite of **15 adversarial mechanical edge cases** (incorporating conflicting constraints, extreme temperatures, and harsh environments) and **100 standardized engineering audit prompts**:
- **Pipeline A (Baseline Pure LLM):** Zero-shot generation using unconstrained GPT-4 / Llama 3.2 without RAG or physical filtering.
- **Pipeline B (RAG-Only):** Semantic vector retrieval querying ChromaDB markdown chunks, passing retrieved text directly to the LLM without mathematical Ashby index filtering.
- **Pipeline C (Full EMS-OS System):** Complete proposed architecture combining the Scientific Parser, Deterministic Ashby Engine, Sourcing Optimizer, Local Ollama Base, and Cloud Gemini Arbitration.

### 3.5.2 Quantitative Evaluation Metrics
1. **Physical Feasibility Rate ($\%$):** Percentage of recommended materials that strictly satisfy all numerical stress, flexural deflection, and operating temperature constraints:
   $$\text{Feasibility Rate} = \frac{N_{\text{viable}}}{N_{\text{total}}} \times 100\%$$
2. **Hallucination Rate ($\%$):** Percentage of cases where the system cites material strength numbers ($\sigma_y$, $E$, $\rho$) deviating by $> 5.0\%$ from certified ASTM datasheets.
3. **Degradation Awareness Rate ($\%$):** Percentage of tests where the system successfully disqualifies hydro-degradable polymers (e.g., PLA in river water) or cold-embrittled steels (e.g., 4140 below DBTT).
4. **Mathematical Provenance Relative Error ($\text{rel\_diff}$):** The relative error between the dynamically calculated index and the exact theoretical formula:
   $$\text{rel\_diff} = \frac{|M_{\text{calc}} - M_{\text{exact}}|}{M_{\text{exact}}} \le 10^{-4}$$
5. **Supply Chain Completeness ($\%$):** Successful generation of realistic Wilson-Harris EOQ batch sizes, MOQ feasibility checks, and logistics transit lead times.

Table 3.5 details the full testing matrix, evaluation tools, and target acceptance criteria.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>35 | Page</i></div>

*Table 3.5: Performance Parameters and Acceptance Criteria for System Testing.*

| Parameter / Feature | Testing Method | Tools / Software Used | Acceptance Criteria |
| :--- | :--- | :--- | :--- |
| **NLP Intent & Constraint Extraction** | Feed 100 structured engineering prompts and compare extracted bounds ($\sigma_y, E, T, P$) against ground truth | `tests/test_nlp_parser.py`, Python `re`, PyTest | $\ge 95\%$ accuracy in extracting numerical limits and standards |
| **Physical Continuum Constraint Satisfaction** | Verify that no recommended material exceeds HDT, homologous creep ($T_H \ge 0.55$), or DBTT limits | `tests/test_audit_100.py`, Analytical Ashby Module | **$100\%$ compliance (0 violations permitted)** |
| **Empirical Degradation Gating** | Evaluate prompts specifying submerged aquatic exposure or outdoor solar UV in Garissa/Equatorial climates | Submerged and UV test cases; `tests/test_materials_db.py` | Disqualification of PLA in freshwater; disqualification of ABS in UV |
| **NASA LOX Auto-Ignition Rule Enforcement** | Query high-pressure liquid oxygen rocket tank materials | Cryogenic LOX audit test case | **$100\%$ elimination of Titanium alloys** in LOX environments |
| **Mathematical Provenance Relative Difference** | Calculate relative error between computed Ashby index and exact theoretical equation | NumPy floating point comparator: $\text{rel\_diff} = \|M_c - M_e\| / M_e$ | **$\text{rel\_diff} \le 10^{-4}$** across all test cases |
| **Supply Chain EOQ & Lead-Time Sourcing** | Verify batch sizing across varying annual demands ($D = 500\,\text{kg}$ to $50,000\,\text{kg}$) | `src/economics_engine.py`, Wilson-Harris Formula | Non-zero EOQ; valid lead times (2-5d domestic, 42d import) |
| **Close Contender Cloud AI Arbitration** | Induce close candidate tie ($\Delta_{\text{score}} \le 8\%$) and verify automatic Gemini API trigger | Multi-engine integration test; Google Cloud Gemini API | Successful internet connection; audited trade-off log generated |
| **End-to-End Execution Latency** | Measure wall-clock runtime for complete parsing, screening, ranking, and UI update | Python `time.perf_counter()`, Streamlit Profiler | $< 1.5\,\text{s}$ deterministic screening; $< 15\,\text{s}$ full LLM synthesis |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>36 | Page</i></div>

# CHAPTER 4: WORK PLAN AND BUDGET

## 4.1 Budget

The successful implementation of this computational capstone project requires structured financial planning to support software licensing, cloud API infrastructure, database acquisition, technical validation, and thesis publication. The project will be partially self-sponsored, with additional resource support from university computer laboratories and student developer grants.

Table 4.1.1 presents the projected cost estimates for the complete development, cloud integration, testing, and documentation of the EMS-OS platform.

*Table 4.1.1: Budget of the Material Selection & Optimization System (EMS-OS).*

| Budget Category | Description of Resource / Component | Estimated Cost (KSh) |
| :--- | :--- | :---: |
| **Cloud Computing & AI APIs** | Google Cloud Gemini API token tier for automated cloud tie-breaker arbitration testing | 4,500 |
| **Database Curation & Acquisition** | Procurement of specialized technical materials datasheets and standards access | 5,000 |
| **Local Hardware Telemetry Testing** | Dedicated solid-state storage and power backup for continuous local Ollama benchmark runs | 6,500 |
| **Technical Verification & Materials** | Benchmark materials procurement validation data and third-party testing comparison | 4,500 |
| **Proposal Printing and Binding** | High-quality color printing and hardback binding of the capstone proposal booklet | 1,200 |
| **Final Technical Report & Thesis** | Comprehensive defense report printing, architectural schematics, and university press binding | 2,000 |
| **Contingency Funds** | Buffer for emergency cloud server surge, data backup, and incidental communication | 5,000 |
| **Total Budget** | | **28,700** |

### 4.1.1 Budget Justification
The largest cost allocations are directed toward **Local Hardware Telemetry Testing (KSh 6,500)**, **Database Curation (KSh 5,000)**, and **Cloud Computing APIs (KSh 4,500)**. These expenditures are vital to ensuring continuous, uninterrupted testing of the local Ollama LLM (`llama3.2`) and robust internet connectivity to the Google Cloud Gemini API during tie-break arbitration experiments. 

Supporting allocations for documentation (KSh 3,200 total) ensure that technical schematics, 2D/3D Ashby charts, and final defense manuscripts are prepared in strict accordance with the University of Nairobi Faculty of Engineering guidelines. By utilizing open-weights local foundation models (Ollama) and open-source Python frameworks (Streamlit, Plotly, ChromaDB), the project achieves tremendous cost efficiency, delivering an enterprise-grade engineering software platform at a fraction of commercial software licensing costs.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>37 | Page</i></div>

## 4.2 Work Plan

The project will be executed over an eight-month period spanning the 2025/2026 academic calendar (September 2025 through May 2026). The work plan is structured into eight progressive phases to ensure methodical execution, rigorous verification, and timely completion.

### Work Plan Phases
1. **Phase 1: Literature Review & Previous Prototype Evaluation (September 2025):** Detailed review of classical Ashby mechanics, materials informatics literature, and comprehensive audit of limitations in the previous University of Nairobi prototype.
2. **Phase 2: Proposal Development & Defense (October 2025):** Formulation of mathematical models, system architecture design, proposal drafting, and formal defense before the Departmental Evaluation Committee.
3. **Phase 3: Database Acquisition & Standardization (November 2025):** Assembly, cleansing, and normalization of 1,490+ engineering materials into the unified JSON/SQLite schema across ANSI, ISO, DIN, JIS, and ASTM standards.
4. **Phase 4: Scientific NLP Parser & Ashby Engine Encoding (December 2025):** Software development of regex numerical extraction, component classification, and deterministic calculation of 12 analytical Ashby performance indices.
5. **Phase 5: Supply Chain & Techno-Economic Engine Development (January 2026):** Algorithmic encoding of Wilson-Harris EOQ optimization, MOQ surplus inventory penalties, logistics lead-time modeling, and TOPSIS multi-criteria scoring.
6. **Phase 6: Multi-Tier Dual-Engine Integration & Cloud API (February 2026):** Local Ollama daemon coupling (`llama3.2`), close-contender detector implementation ($\Delta \le 8\%$), and automated Google Cloud Gemini tie-breaker arbitration over the internet.
7. **Phase 7: System Performance Testing & Comparative Benchmarking (March - April 2026):** Execution of 100 standardized engineering audit test cases and 15 adversarial edge cases; comparative evaluation against pure LLM and RAG-only baselines.
8. **Phase 8: Development of Final Technical Report & Defense (May 2026):** Compilation of experimental results, final thesis writing, binding, and final capstone project defense presentation.

Table 4.2.1 illustrates the project schedule and milestone distribution across the academic year.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>38 | Page</i></div>

*Table 4.2.1: Work Plan Schedule (September 2025 - May 2026).*

| Activity / Project Milestone | 2025 Sept | 2025 Oct | 2025 Nov | 2025 Dec | 2026 Jan | 2026 Feb | 2026 Mar | 2026 Apr | 2026 May |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Research on previous iterations, literature & available technology** | ■■■ | | | | | | | | |
| **Development and submission of proposal** | | ■■■ | | | | | | | |
| **Database acquisition, cleansing & catalog curation (1,490+ materials)** | | | ■■■ | | | | | | |
| **Development of Scientific NLP Parser & Ashby Mechanics Engine** | | | | ■■■ | | | | | |
| **Supply Chain Techno-Economic & EOQ Optimizer Formulation** | | | | | ■■■ | | | | |
| **Multi-Tier Dual-Engine Orchestration (Ollama & Cloud Gemini API)** | | | | | | ■■■ | | | |
| **System Performance Testing, Adversarial Audits & Benchmarking** | | | | | | | ■■■ | ■■■ | |
| **Compilation of Final Technical Report & Capstone Defense** | | | | | | | | | ■■■ |

<br/>

```
Milestone 1: Project Proposal Approved by Department (October 2025)
     │
     ▼
Milestone 2: Master Materials Database Curation Complete (November 2025)
     │
     ▼
Milestone 3: Core Ashby Mechanics & Economics Engines Validated (January 2026)
     │
     ▼
Milestone 4: Dual-Tier Local/Cloud Orchestration Operational (February 2026)
     │
     ▼
Milestone 5: 100-Prompt Benchmark & Comparative Evaluation Finished (April 2026)
     │
     ▼
Milestone 6: Final Capstone Defense and Thesis Submission (May 2026)
```

<div style="page-break-after: always;"></div>

---

<div align="right"><i>39 | Page</i></div>

# Appendices

### Appendix 1 - Master Table of Ashby Mechanical Performance Indices

*Table A.1: Comprehensive Catalog of Governing Continuum Mechanics Ashby Indices [4].*

| Primary Loading Mode | Mechanical Design Constraint | Functional Objective to Optimize | Governing Ashby Index ($M$) | Target Physical Dimension |
| :--- | :--- | :--- | :--- | :---: |
| **Axial Tensile Tie** | Deflection / Elastic Elongation Limit | Minimize Structural Mass | $M_1 = \frac{E}{\rho}$ | $\text{GPa} / (\text{Mg/m}^3)$ |
| **Axial Tensile Tie** | Plastic Yield Failure Limit | Minimize Structural Mass | $M_2 = \frac{\sigma_y}{\rho}$ | $\text{MPa} / (\text{Mg/m}^3)$ |
| **Flexural Beam** | Maximum Transverse Deflection | Minimize Structural Mass | $M_3 = \frac{E^{1/2}}{\rho}$ | $\text{GPa}^{1/2} / (\text{Mg/m}^3)$ |
| **Flexural Beam** | Plastic Bending Yield Moment | Minimize Structural Mass | $M_4 = \frac{\sigma_y^{2/3}}{\rho}$ | $\text{MPa}^{2/3} / (\text{Mg/m}^3)$ |
| **Plate in Bending** | Flexural Rigidity / Out-of-Plane Deflection | Minimize Panel Mass | $M_5 = \frac{E^{1/3}}{\rho}$ | $\text{GPa}^{1/3} / (\text{Mg/m}^3)$ |
| **Plate in Bending** | Yield Puncture under Impact | Minimize Panel Mass | $M_6 = \frac{\sigma_y^{1/2}}{\rho}$ | $\text{MPa}^{1/2} / (\text{Mg/m}^3)$ |
| **Torsion Shaft** | Angular Twist Deflection Limit | Minimize Shaft Mass | $M_7 = \frac{G^{1/2}}{\rho}$ | $\text{GPa}^{1/2} / (\text{Mg/m}^3)$ |
| **Torsion Shaft** | Torsional Shear Yielding | Minimize Shaft Mass | $M_8 = \frac{\tau_y^{2/3}}{\rho} \approx \frac{\sigma_y^{2/3}}{\rho}$ | $\text{MPa}^{2/3} / (\text{Mg/m}^3)$ |
| **Pressure Vessel** | Hoop Stress Bursting (Barlow Equation) | Minimize Containment Mass | $M_9 = \frac{\sigma_y}{\rho}$ | $\text{MPa} / (\text{Mg/m}^3)$ |
| **Pressure Vessel** | Leak-Before-Break Fast Fracture | Maximize Critical Crack Depth | $M_{9b} = \frac{K_{1c}}{\sigma_y}$ | $\sqrt{\text{m}}$ |
| **Elastic Spring** | Maximum Elastic Energy Storage | Maximize Energy per Mass | $M_{10} = \frac{\sigma_y^2}{E \rho}$ | $\text{kJ/kg}$ |
| **Elastic Spring** | Maximum Elastic Energy Storage | Maximize Energy per Volume | $M_{10b} = \frac{\sigma_y^2}{E}$ | $\text{kJ/m}^3$ |
| **Heat Sink / Fin** | Steady-State Fourier Heat Conduction | Maximize Heat Flux per Mass | $M_{11} = \frac{\lambda}{\rho}$ | $\text{W}\cdot\text{m}^2 / (\text{kg}\cdot\text{K})$ |
| **Thermal Barrier** | Transient Insulation Barrier | Minimize Thermal Ingress | $M_{12} = \frac{1}{\lambda}$ | $\text{m}\cdot\text{K} / \text{W}$ |
| **Rotary Flywheel** | Centrifugal Bursting Angular Velocity | Maximize Stored Kinetic Energy | $M_{13} = \frac{\sigma_y}{\rho}$ | $\text{kJ/kg}$ |
| **Cyclic Machine Shaft**| Dynamic Alternating Fatigue ($10^7$ cycles)| Maximize Fatigue Life per Mass| $M_{14} = \frac{\sigma_f}{\rho}$ | $\text{MPa} / (\text{Mg/m}^3)$ |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>40 | Page</i></div>

### Appendix 2 - International Engineering Standard Designations and Mappings

*Table A.2: Mapping of International Testing Standards to Physical Constraints.*

| International Standard | Governing Regulatory Scope | Measured Mechanical / Physical Property | Application in EMS-OS Filtering Engine |
| :--- | :--- | :--- | :--- |
| **ASTM D638** | Standard Test Method for Tensile Properties of Plastics | Tensile Yield Strength ($\sigma_y$), Modulus ($E$), Elongation ($\%$) | Verification of thermoplastic tensile properties |
| **ISO 527-1 / 527-2** | Plastics -- Determination of Tensile Properties | Tensile stress at yield and break, tensile modulus | European/International plastic property normalization |
| **ASTM E8 / E8M** | Standard Test Methods for Tension Testing of Metallic Materials | $0.2\%$ offset yield strength ($\sigma_y$), ultimate tensile strength ($\sigma_{\text{uts}}$) | Baseline mechanical verification for metallic alloys |
| **ASTM E23** | Standard Test Methods for Notched Bar Impact Testing | Charpy V-notch absorbed impact energy ($\text{Joules}$) | Gating for dynamic impact and shock absorption |
| **ASTM E399** | Linear-Elastic Plane-Strain Fracture Toughness ($K_{1c}$) | Critical stress intensity factor ($K_{1c}$) | Assessment of leak-before-break pressure vessels |
| **ASTM D648 / ISO 75** | Deflection Temperature Under Flexural Load (HDT) | Temperature under $0.455\,\text{MPa}$ or $1.82\,\text{MPa}$ load | Hard thermodynamic ceiling for polymer disqualification |
| **ASTM D570** | Water Absorption of Plastics | Percentage mass increase after $24\,\text{h}$ and saturation immersion | Empirical calculation of hydrolysis degradation drop |
| **ASTM G154 / G155** | Accelerated Weathering Testing (Fluorescent UV / Xenon Arc) | Tensile strength retention after $1,000\,\text{h}$ UV irradiance | Assessment of outdoor equatorial UV photo-oxidation |
| **ASME BPVC Section VIII** | Rules for Construction of Pressure Vessels (Div 1 & Div 2) | Allowable design stress, joint efficiency, maximum working pressure | Verification of pressure containment shell thickness |
| **ISO 10993-5** | Biological Evaluation of Medical Devices -- Cytotoxicity | In vitro cytotoxicity and cell viability percentage | Hard binary gating for biocompatible surgical implants |
| **FDA 21 CFR 177** | Indirect Food Additives: Polymers | Extraction limits for food-contact resin formulations | Food processing contact safety certification |
| **NASA-STD-6001** | Flammability, Offgassing, and Oxygen Compatibility | Autogenous ignition temperature in enriched liquid oxygen | **Strict disqualification of Titanium in high-pressure LOX** |

<div style="page-break-after: always;"></div>

---

<div align="right"><i>41 | Page</i></div>

### Appendix 3 - Sourcing Category Parameters and Transit Lead Times

*Table A.3: Default Procurement Logistics and Carrying Cost Benchmarks.*

| Sourcing Tier | Primary Geographic Origin | Typical Logistics Route in Kenya | Average Lead Time ($L_{\text{days}}$) | Order Setup Cost ($S$) | Minimum Order Quantity ($MOQ$) | Sourcing Flexibility Rating ($S_{\text{avail}}$) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Domestic Local Stock** | Nairobi Industrial Area, Mombasa Warehouses | Road Trucking / Local Dispatch | **2 - 5 Days** | $\$120$ USD | $10 - 25\,\text{kg}$ | **95 / 100** |
| **Regional Distribution** | South Africa, Egypt, India, UAE | Air Freight / Cross-Border Trucking | **14 - 21 Days** | $\$320$ USD | $100 - 250\,\text{kg}$ | **72 / 100** |
| **Global Ocean Freight** | China, European Union, United States | Maritime Shipping to Port of Mombasa $\to$ SGR / Highway to Nairobi | **30 - 60 Days** | $\$680$ USD | $500 - 2,500\,\text{kg}$ | **45 / 100** |

<br/>

### Cost-Weighted Performance Index Formulation:
In addition to pure mechanical index scoring, the sourcing module calculates the **Cost-Weighted Performance Index ($M_{\text{cost}}$)**, representing physical efficiency delivered per unit currency spent:

$$M_{\text{cost}} = \frac{M}{\rho \cdot C_m}$$

where $M$ is the primary Ashby performance metric, $\rho$ is material density ($\text{kg/m}^3$), and $C_m$ is raw material price ($\text{USD/kg}$). This index quantifies why structural mild steels and standard aluminum alloys frequently outrank expensive exotic titanium or continuous carbon prepreg composites in commercial cost-sensitive mechanical design.

<div style="page-break-after: always;"></div>

---

<div align="right"><i>42 | Page</i></div>

# References

[1] M. F. Ashby, *Materials Selection in Mechanical Design*, 4th ed. Oxford, UK: Butterworth-Heinemann, 2011.

[2] G. E. Dieter and D. C. Bacon, *Engineering Design: A Materials and Processing Approach*, 5th ed. New York, NY: McGraw-Hill Education, 2013.

[3] M. F. Ashby and K. Johnson, *Materials and Design: The Art and Science of Material Selection in Product Design*, 3rd ed. Oxford, UK: Butterworth-Heinemann, 2013.

[4] M. F. Ashby, "Materials selection in mechanical design," *Journal of Materials Education*, vol. 15, no. 3, pp. 145-168, 1993.

[5] P. R. Lewis and K. Reynolds, *Forensic Materials Engineering: Case Studies*. Boca Raton, FL: CRC Press, 2004.

[6] G. E. Dieter, *Mechanical Metallurgy*, 3rd ed. London, UK: McGraw-Hill, 1986.

[7] M. M. Farag, *Materials and Process Selection for Engineering Design*, 3rd ed. Boca Raton, FL: CRC Press, 2014.

[8] J. A. Charles, F. A. A. Crane, and J. A. G. Furness, *Selection and Use of Engineering Materials*, 3rd ed. Oxford, UK: Butterworth-Heinemann, 1997.

[9] W. D. Callister and D. G. Rethwisch, *Materials Science and Engineering: An Introduction*, 10th ed. Hoboken, NJ: John Wiley & Sons, 2018.

[10] University of Nairobi, "Final Year Mechanical Engineering Capstone Project Archive: Evaluation of 3D Printed Materials for Decentralized Micro-Hydro Turbines," Dept. of Mechanical and Manufacturing Engineering, Nairobi, Kenya, Tech. Rep. FMM-2024-08, 2024.

[11] N. E. Dowling, *Mechanical Behavior of Materials: Engineering Methods for Deformation, Fracture, and Fatigue*, 4th ed. Boston, MA: Pearson, 2013.

[12] R. I. Stephens, A. Fatemi, R. R. Stephens, and H. O. Fuchs, *Metal Fatigue in Engineering*, 2nd ed. New York, NY: John Wiley & Sons, 2000.

[13] J. R. Davis, *Corrosion of Materials: Fundamental Principles and Applications*. Materials Park, OH: ASM International, 2000.

[14] M. C. Celina, "Review of polymer oxidation and its relationship with materials performance and lifetime prediction," *Polymer Degradation and Stability*, vol. 98, no. 12, pp. 2419-2429, 2013.

[15] A. Davis and D. Sims, *Weathering of Polymers*. London, UK: Applied Science Publishers, 1983.

[16] J. E. Mark, *Polymer Data Handbook*, 2nd ed. Oxford, UK: Oxford University Press, 2009.

[17] R. C. Reed, *The Superalloys: Fundamentals and Applications*. Cambridge, UK: Cambridge University Press, 2006.

[18] J. W. Ekin, *Experimental Techniques for Low-Temperature Measurements: Cryostat Design, Material Properties, and Superconductor Critical-Current Testing*. Oxford, UK: Oxford University Press, 2006.

[19] National Aeronautics and Space Administration, *Flammability, Offgassing, and Compatibility Requirements and Test Procedures for Materials in Environments that Support Combustion*, NASA Technical Standard NASA-STD-6001B, Washington, DC, 2011.

[20] K. Rajan, "Materials informatics: The vision for materials science," *Materials Today*, vol. 8, no. 10, pp. 38-45, 2005.

[21] Granta Design Ltd., *CES EduPack Materials Selection Software: Engineering Whitepapers and Case Studies*, Cambridge, UK: Ansys Granta, 2021.

[22] C. J. Tuck, R. J. M. Hague, and N. Burns, "Rapid manufacturing: impact on supply chain management," *International Journal of Technology Management*, vol. 37, no. 1/2, pp. 23-44, 2007.

[23] A. Agrawal and A. Choudhary, "Perspective: Materials informatics and big data: Realization of the 'fourth paradigm' of science in materials science," *APL Materials*, vol. 4, no. 5, p. 053208, 2016.

[24] S. K. Simani, "Supply chain friction and procurement delays in East African engineering sectors," *Journal of African Manufacturing & Industrialization*, vol. 12, no. 2, pp. 88-104, 2022.

[25] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, "Attention is all you need," in *Advances in Neural Information Processing Systems (NeurIPS 2017)*, vol. 30, Long Beach, CA, 2017, pp. 5998-6008.

[26] H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al., "LLaMA: Open and efficient foundation language models," *arXiv preprint arXiv:2302.13971*, 2023.

[27] J. Achiam, S. Adler, S. Agarwal, L. Ahmad, I. Akkaya, F. L. Aleman, D. Almeida, J. Altenschmidt, S. Altman, S. Anadkat, et al., "GPT-4 technical report," *arXiv preprint arXiv:2303.08774*, 2023.

[28] L. Makatura, M. Foshey, B. Wang, F. Hähnlein, P. Ma, I. Zhao, V. Sitzmann, S. Mueller, and W. Matusik, "How can large language models help humans in design and manufacturing?," *arXiv preprint arXiv:2307.14377*, 2023.

[29] M. Soori, B. Arezoo, and R. Danyi, "Artificial intelligence, machine learning and deep learning in advanced robotics, a review," *Cognitive Robotics*, vol. 3, pp. 54-70, 2023.

[30] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, "Survey of hallucination in natural language generation," *ACM Computing Surveys*, vol. 55, no. 12, pp. 1-38, 2023.

[31] Y. Zhang, Y. Li, L. Cui, D. Cai, L. Liu, T. Fu, X. Huang, E. Zhao, Y. Zhang, Y. Chen, et al., "Siren's song in the AI ocean: A survey on hallucination in large language models," *arXiv preprint arXiv:2309.01219*, 2023.

[32] M. Bano, D. Zowghi, and M. Ferrari, "Evaluating large language models on specialized engineering domain tasks: A critical reliability study," *IEEE Transactions on Software Engineering & Systems*, vol. 50, no. 4, pp. 812-829, 2024.

[33] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W.-t. Yih, T. Rocktäschel, et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Advances in Neural Information Processing Systems (NeurIPS 2020)*, vol. 33, 2020, pp. 9459-9474.

[34] Y. Gao, Y. Xiong, X. Wang, K. Wang, and H. Chen, "Modular RAG: Transforming RAG systems into flexible Lego-like pipelines," *arXiv preprint arXiv:2407.21059*, 2024.

[35] G. Marcus, "The next decade in AI: Four steps towards robust artificial intelligence," *arXiv preprint arXiv:2002.06177*, 2020.

[36] Google Gemini Team, "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context," Google DeepMind, Tech. Rep., 2024.

[37] G. Boothroyd, P. Dewhurst, and W. A. Knight, *Product Design for Manufacture and Assembly*, 3rd ed. Boca Raton, FL: CRC Press, 2010.

[38] E. A. Silver, D. F. Pyke, and R. Peterson, *Inventory Management and Production Planning and Scheduling*, 3rd ed. New York, NY: John Wiley & Sons, 1998.

[39] S. Chopra and P. Meindl, *Supply Chain Management: Strategy, Planning, and Operation*, 7th ed. Boston, MA: Pearson, 2019.

[40] Kenya Ports Authority, *Annual Operational Port Performance and SGR Freight Transit Statistics: Container Handling at Kilindini Harbour*, KPA Corporate Affairs Division, Mombasa, Kenya, Tech. Rep. KPA-2024-Q3, 2024.

[41] C.-L. Hwang and K. Yoon, *Multiple Attribute Decision Making: Methods and Applications: A State-of-the-Art Survey*. Berlin, Germany: Springer-Verlag, 1981.

[42] R. V. Rao, *Decision Making in the Manufacturing Environment: Using Graph Theory and Fuzzy Multiple Attribute Decision Making Methods*. London, UK: Springer, 2007.

[43] P. Kraljic, "Purchasing must become supply management," *Harvard Business Review*, vol. 61, no. 5, pp. 109-117, 1983.

[44] R. H. Wilson, "A scientific routine for stock control," *Harvard Business Review*, vol. 13, pp. 116-128, 1934.

[45] F. W. Harris, "How many parts to make at once," *Factory, The Magazine of Management*, vol. 10, no. 2, pp. 135-136, 1913.

[46] International Chamber of Commerce (ICC), *Incoterms 2020: ICC Rules for the Use of Domestic and International Trade Terms*, Publication No. 723E, Paris, France: ICC Publishing, 2020.

[47] M. Arslan and A. Munawar, "Physics-informed retrieval-augmented generation for autonomous mechanical design," *Journal of Mechanical Design*, vol. 148, no. 2, pp. 021401-021415, 2026.

[48] X. Liu, J. Zhang, H. Wang, and T. Chen, "Eliminating hallucinations in LLM-assisted materials engineering via deterministic mechanics decoupling," *Advanced Intelligent Systems*, vol. 7, no. 3, p. 2400112, 2025.

[49] Z. Chen, Y. Li, and K. S. Kumar, "Multi-objective materials selection integrating Ashby performance indices and supply chain resilience," *Materials & Design*, vol. 249, p. 113540, 2025.

[50] H. Lee, M. Park, and D. Kim, "Comparative evaluation of local edge LLMs versus cloud APIs in CAE workflows," *Computer-Aided Design*, vol. 178, p. 103688, 2026.

[51] J. Wu, S. Patel, and R. Martinez, "Total landed cost and lead-time uncertainty in global engineering procurement," *International Journal of Production Economics*, vol. 280, p. 109120, 2025.

[52] M. Yazdani and F. R. Payam, "A comparative study on extension of TOPSIS method for material selection in engineering design," *Materials & Design*, vol. 65, pp. 375-384, 2015.

<div style="page-break-after: always;"></div>

---

<div align="center">

### END OF PROPOSAL DOCUMENT

**Department of Mechanical and Manufacturing Engineering**  
**Faculty of Engineering -- University of Nairobi**  
**October 2026**

</div>
