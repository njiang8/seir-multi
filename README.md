# Large-Scale SEIR Multi-Disease Simulation
An agent-based SEIR (Susceptible-Exposed-Infected-Recovered) modeling framework for simulating the co-circulation and spread of multiple diseases across a realistic social contact network.

## 📋 Project Overview
This repository provides a complete, reproducible workflow for:
1. Building realistic social contact networks for population modeling
2. Simulating single or multiple diseases with independent SEIR progression parameters
3. Running repeated validation experiments to ensure result robustness
4. Visualizing and analyzing simulation outputs with Jupyter Notebooks

The framework is optimized for large-scale populations and provides traceable, structured output results for further academic or applied research.

## 📁 Project Directory Structure
 
large_scale_seir/
├── .venv/                # Virtual environment directory
├── data/                # Input data (e.g., population, disease parameters)
├── results/             # Output simulation results
├── src/                 # Core source code
│   ├── agent.py         # Defines individual agent behavior and states
│   ├── create_social_network.py  # Builds the social contact network
│   ├── seir.py          # Implements the SEIR disease progression logic
│   ├── setting_simulation_results_path.py  # Configures result output paths
│   ├── simulation.py    # Orchestrates the full simulation workflow
│   └── tools.py         # Helper functions and utilities
├── 1-seir-wny-single.py # Single-disease simulation for Western New York
├── 2-seir-wny-multi-disease.py # Multi-disease co-circulation simulation
├── 3-validation-multi-run.py # Validation with repeated simulation runs
├── 4-simulation_results_analysis.ipynb # Jupyter notebook for result analysis
├── data.zip             # Compressed input data
├── README.md            # This file
└── requirements.txt     # Python dependencies
