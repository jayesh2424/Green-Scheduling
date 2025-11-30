# Green Scheduling Algorithm ♻️

Energy-aware task scheduling simulator built in Python for macOS (Apple Silicon).  
This project compares classic CPU scheduling algorithms against a custom “Green” scheduler that minimizes energy consumption and estimated CO₂ emissions using a simple power model and Indian grid emission factors.

---

## 🌍 Overview

Traditional schedulers optimize for performance metrics like throughput and latency, often ignoring energy and carbon impact. This project explores how different scheduling strategies affect:

- Total energy consumption (kWh)
- CO₂ emissions (kg CO₂e)
- Basic performance metrics (average wait time, average turnaround time)

It implements and compares:

- FCFS (First Come First Served)
- SJF (Shortest Job First)
- Priority-based scheduling
- Round Robin
- A custom **EnergyOptimized** scheduler that prefers low-CPU tasks and applies simple DVFS-style power scaling. [web:27][web:30]

---

## 🧱 Features

- **Multiple scheduling algorithms**
  - `FCFS`
  - `SJF`
  - `PriorityBased`
  - `RoundRobin`
  - `EnergyOptimized` (Green scheduler)
- **Energy & CO₂ estimation**
  - Linear power model between idle and max power (Watts)
  - Energy in kWh converted to CO₂ using a configurable emission factor (kg CO₂e/kWh), initialized for India. [web:32][web:39]
- **Metrics per algorithm**
  - Total energy (kWh)
  - CO₂ emissions (kg CO₂e)
  - Average wait time
  - Average turnaround time
- **Auto-generated outputs in `results/`**
  - `01_energy_comparison.png` – Energy vs algorithm
  - `02_co2_comparison.png` – CO₂ vs algorithm
  - `03_performance_metrics.png` – Wait & turnaround time
  - `04_results_summary.csv` – Tabular metrics
  - `simulation_results.json` – Raw JSON metrics


---

## 🚀 Getting Started (macOS – Apple Silicon)

### 1. Clone the repository
`git clone https://github.com/jayesh2424/Green-Scheduling.git
cd Green-Scheduling`

### 2. Create and activate a virtual environment

`python3 -m venv venv
source venv/bin/activate`

### 3. Install dependencies
`pip install numpy matplotlib pandas psutil`

### 4. Run the simulator

`python3 main.py`

After the run finishes, open the `results/` folder. You should see:

- `01_energy_comparison.png`
- `02_co2_comparison.png`
- `03_performance_metrics.png`
- `04_results_summary.csv`
- `simulation_results.json`


---

## 📊 Interpreting the Results

- **Energy Comparison (`01_energy_comparison.png`)**
  - Lower bar = less energy consumed by that algorithm.
- **CO₂ Comparison (`02_co2_comparison.png`)**
  - CO₂ is derived from energy using the emission factor set in `config.py`. [web:32][web:37]
- **Performance Metrics (`03_performance_metrics.png`)**
  - Trade-off between responsiveness (wait time) and total completion time (turnaround time).
- **CSV Summary (`04_results_summary.csv`)**
  - Ready to import into Excel, Google Sheets, or pandas for tables and additional plots.

Typical use in a report:

- Pick a couple of algorithms (e.g., FCFS vs EnergyOptimized).
- Compare both energy and performance.
- Discuss trade-offs: “green” vs “fast”.

---

## ⚙️ Configuration & Customization

All key parameters are in `config.py`:

- **System & power model**
  - `CPU_CORES`
  - `MAX_FREQUENCY_GHZ`
  - `BASE_POWER_WATTS`
  - `MAX_POWER_WATTS`
- **Tasks**
  - `NUM_TASKS`
  - `TASK_DURATION_MIN`
  - `TASK_DURATION_MAX`
- **Carbon & cost**
  - `EMISSION_FACTOR_KG_CO2_PER_KWH`
  - `POWER_COST_PER_KWH`
- **Algorithms**
  - `ALGORITHMS = ['FCFS', 'SJF', 'RoundRobin', 'PriorityBased', 'EnergyOptimized']`
- **Simulation**
  - `SIMULATION_TIME`
  - `SAMPLING_INTERVAL`

Feel free to:

- Increase `NUM_TASKS` for heavier workloads.
- Adjust `BASE_POWER_WATTS` / `MAX_POWER_WATTS` for different hardware.
- Change `EMISSION_FACTOR_KG_CO2_PER_KWH` if targeting a different grid mix. [web:34][web:39]

---

## 🎓 Academic / Mini-Project Use

This repository is suitable for:

- Green Computing / Sustainable IT mini-projects
- Energy-aware / Carbon-aware scheduling experiments
- Demonstrations of:
  - Relationship between CPU scheduling and energy use
  - Simple carbon budgeting based on kWh → CO₂ conversion [web:30][web:31]

You can directly reuse:

- Architecture overview (file structure, main components)
- Screenshots of charts from `results/`
- Tables from `04_results_summary.csv`
- Observations about which scheduler is most energy-efficient vs performance-oriented

---

## 🧑‍💻 Author

- **Author:** Jayesh (jayesh2424)  
- **GitHub:** [@jayesh2424](https://github.com/jayesh2424)

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [`LICENSE`](./LICENSE) file in this repository for the full license text.
