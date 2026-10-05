# Engineering Material Selection Engine with Local RAG-LLM Interface

**Final Year Mechanical Engineering Capstone Project**  
**Author:** Mutuku Geoffrey Mulu (F18/144332/2022)  
**Target Application:** Decentralized Additive Manufacturing & Mechanical Optimization  

---

## 🚀 Overview

This capstone project delivers a complete, production-grade **Autonomous LLM-Based Material Selection System** bridging materials science, mechanical design, fluid dynamics, and artificial intelligence. 

The tool empowers engineers and localized manufacturers to input natural language prompts (e.g., *"I need a lightweight bracket for a racing car that will experience vibration"*) and receive mathematically verified material recommendations, Ashby indices, and manufacturing directives.

### Key Innovations:
1. **NLP Translation Layer:** Translates colloquial requirements into formal boundary conditions (Yield strength, Young's modulus, UV resistance).
2. **Mathematical Ashby Engine:** Analytically derives and calculates Michael F. Ashby performance indices (e.g., $M = E^{1/2}/\rho$) dynamically from user input.
3. **Verified RAG Knowledge Base:** Powered by a persistent **ChromaDB** vector store to enforce strict data provenance and eliminate LLM hallucinations. Every numerical property recommended is cited directly from a Material Data Sheet.
4. **100% Autonomous Local Deployment:** Designed to run fully offline on edge hardware (laptops) for field deployment.

---

## 💻 Local Setup & Execution Guide

This system is built to run purely locally. You only need your terminal and a web browser.

### Step 1: Install Dependencies
If this is your first time setting up the project, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### Step 2: Configure Local LLM (Optional)
If you wish to use local Ollama inference, ensure Ollama is running and your `OLLAMA_BASE_URL` is set in `.env`. Alternatively, the system's **Autonomous Offline Expert Engine** will dynamically route and solve the equations deterministically without an LLM if one is not detected.

### Step 3: Run the Application
Open your terminal inside the project folder and start the Streamlit server:
```bash
streamlit run app.py
```

### Step 4: Access the UI
Once the server starts, open your browser and navigate to:
**http://localhost:8501**

From here, you can:
*   Start a **New Chat** in the sidebar.
*   Interact with the mathematical Ashby log-log charts.
*   View the RAG retrieval blocks (proving the data is grounded in engineering datasheets).
*   Download full Markdown engineering specification reports.

---

## 📂 Project Structure

*   `app.py`: The main Streamlit web application.
*   `cli.py`: A command-line interface version of the tool.
*   `src/`: Contains the core engineering logic (Ashby engine, RAG pipeline, NLP parsing).
*   `tests/`: Comprehensive test suite including 15 complex adversarial engineering edge cases.
*   `knowledge_base/` & `chroma_db_store/`: The localized vector database of material data sheets.
*   `results_comparison.csv`: The evaluation results demonstrating the RAG pipeline's resistance to hallucinations against a pure LLM.
*   `CAPSTONE_THESIS_REPORT.md`: Comprehensive academic breakdown of the algorithms used.
