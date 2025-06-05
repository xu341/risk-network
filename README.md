# README

This repository provides a collection of Python scripts for network analysis and risk propagation simulation based on the SIR (Susceptible-Infected-Recovered) model. The simulations support evaluating the impact of various topological characteristics and model parameters on risk diffusion in directed networks.

---

## Installation Guide

### 1. **Install Python:**
- Visit the official Python website: [python.org](https://www.python.org/)
- Download the installer for your system (Windows, macOS, Linux)
- Follow installation instructions
  - On Windows, ensure you check the box to **"Add Python to PATH"**
- Confirm the installation by running:
  ```bash
  python --version
  ```

### 2. **Install Required Dependencies:**
Open your command line interface:
- **Windows:** Press `Win + R`, type `cmd`, and press `Enter`
- **macOS/Linux:** Open Terminal

Install the dependencies:
```bash
pip install pandas networkx matplotlib numpy scipy openpyxl jupyter
```

### 3. **Prepare Data File:**
Each script uses an absolute file path (e.g., `D:/paper/data.xlsx`) to locate the Excel data file.
Please ensure that the file exists at the specified location on your system.
If needed, modify the `file_path` variable in each script to match the actual path on your machine.

---

## Code Descriptions & Usage

### 1. Cumulative Degree Distribution
- **File:** `1 cumulative_degree_distribution.py`
- **Purpose:** Computes the cumulative degree distribution of a risk network and fits a power-law function
- **Usage:**
  - Open terminal and run:
    ```bash
    python 1 cumulative_degree_distribution.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "1 cumulative_degree_distribution.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 2. Network Efficiency under Different Interference Strategies
- **File:** `2 network_efficiency.py`
- **Purpose:** Analyzes how network efficiency changes when removing nodes based on different criteria
- **Usage:**
  - Open terminal and run:
    ```bash
    python 2 network_efficiency.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "2 network_efficiency.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 3. SIR Simulation - Initial Infection Nodes
- **File:** `3 initial_infection_node.py`
- **Purpose:** Simulates risk spread under different initial infected nodes
- **Usage:**
  - Open terminal and run:
    ```bash
    python 3 initial_infection_node.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "3 initial_infection_node.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 4. SIR Simulation - Intervention Timing
- **File:** `4 risk_intervention_step.py`
- **Purpose:** Simulates how different intervention timings affect spread outcomes
- **Usage:**
  - Open terminal and run:
    ```bash
    python 4 risk_intervention_step.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "4 risk_intervention_step.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 5. SIR Simulation - Infection Rates
- **File:** `5 risk_propagation_rate.py`
- **Purpose:** Simulates how different infection rates (β) impact the spread
- **Usage:**
  - Open terminal and run:
    ```bash
    python 5 risk_propagation_rate.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "5 risk_propagation_rate.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 6. SIR Simulation - Recovery Rates
- **File:** `6 risk_recovery_rate.py`
- **Purpose:** Simulates how different recovery rates (γ) affect network recovery
- **Usage:**
  - Open terminal and run:
    ```bash
    python 6 risk_recovery_rate.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "6 risk_recovery_rate.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

### 7. SIR Simulation - Control Node Strategies
- **File:** `7 initial_control_node.py`
- **Purpose:** Compares various fixed and random control node strategies to mitigate spread
- **Usage:**
  - Open terminal and run:
    ```bash
    python 7 initial_control_node.py
    ```
  - Or use in Jupyter Notebook:
    ```python
    %run "7 initial_control_node.py"
    ```
    Make sure to %cd into the directory where the script is located before using %run.
    You can also copy the script content into a Jupyter cell to modify and run interactively.

---

## Data File Format

- **File:** `data.xlsx`
- **Sheet name:** `Sheet1`
- **Content:** Adjacency matrix with node names as row/column headers
- **Values:** 1 (edge exists), 0 (no edge)

---

## Modifying Code
You can edit `.py` files using any text editor (e.g., VS Code, Notepad). Change simulation parameters such as infection rate (`beta`), recovery rate (`gamma`), intervention step, or number of iterations as needed.

---

## Results Output
All scripts will output simulation results in graphical form using Matplotlib. These figures will open in a pop-up window after each script is run.

---

## Repository Link
Access all files and data at:

```
https://github.com/<your-username>/<repository-name>
```

(Replace with the actual link after upload)
