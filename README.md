# Autonomous Mechanical Material Selection Engine

**Welcome!** If you have just landed on this repository and have no idea what this project is, you are in the right place. 

## 📖 What is this?
Imagine an AI assistant that behaves like a world-class Mechanical Engineer. 

Normally, if you ask a standard AI (like ChatGPT) to recommend a material to build a drone arm or a boat hull, it guesses based on internet text. This is dangerous in engineering. 
This project solves that problem. It is an **Autonomous LLM-Based Material Selection System** that forces the AI to use strict **physics** and **mathematical optimization** (known as Michael F. Ashby indices). 

When you type a non-technical request (e.g., *"I need a lightweight bracket for a racing car"*), the system:
1. Translates your words into strict physical boundaries (Yield strength, Young's modulus).
2. Searches a local, mathematically verified database (ChromaDB) of real Material Data Sheets.
3. Generates interactive Ashby engineering charts and a highly accurate material recommendation.

This project was built for a 5th-Year Mechanical Engineering Capstone.

---

## 🚀 How to Run this on Your Machine (Step-by-Step)

This application is designed to run 100% locally on your computer. You do not need any cloud servers. Follow these exact steps to fire it up successfully.

### Step 1: Prerequisites
Before you begin, ensure you have Python installed on your computer.
* Download and install Python (3.10 or newer) from [python.org](https://www.python.org/).
* *(When installing on Windows, make sure to check the box that says **"Add Python to PATH"**).*

### Step 2: Download the Project
If you are using Git, clone this repository. Otherwise, click the green **"Code"** button at the top of this page and click **"Download ZIP"**, then extract the folder on your computer.

### Step 3: Open Your Terminal
Open your computer's terminal (Command Prompt or PowerShell on Windows, Terminal on Mac/Linux) and navigate to the project folder:
```bash
cd path/to/Material-selection-LLM
```

### Step 4: Create a Virtual Environment (Recommended)
It is best practice to create a virtual environment to hold the project's dependencies.
* **On Windows:**
  ```bash
  python -m venv .venv
  .venv\Scripts\activate
  ```
* **On Mac/Linux:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```
*(You should now see `(.venv)` at the beginning of your terminal line).*

### Step 5: Install the Required Libraries
Now, tell Python to install all the necessary packages (like Streamlit, Plotly, and ChromaDB) to make the app work. Run this command:
```bash
pip install -r requirements.txt
```
*(This may take a few minutes to download everything).*

### Step 6: Launch the Application!
Once the installation finishes, run this command to start the user interface:
```bash
streamlit run app.py
```

### Step 7: View in Your Browser
The terminal will display a local network URL. Open your web browser and go to:
👉 **http://localhost:8501**

---

## 🎮 How to Test the System

Once the webpage loads, you can immediately test it out!

1. Look at the left sidebar and click **"➕ New Chat"**.
2. At the bottom of the screen, type a plain-English request. For example, copy and paste this:
   > *"I want to design a lightweight and stiff bicycle frame that won't flex under heavy rider pedaling."*
3. Press **Enter**.

**What to watch for:**
* You will see the system calculate the physical requirements.
* It will generate a dynamic, interactive **Ashby Property Chart** plotting the best materials.
* It will show you exactly which Engineering Data Sheets it used to verify its answer so you know it isn't hallucinating.
* You can click the **Download** button at the bottom of the response to save a formal Markdown engineering report.

Enjoy exploring the engine!
