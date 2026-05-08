# Large-Scale SEIR Disease Simulation
An agent-based SEIR (Susceptible-Exposed-Infected-Recovered) modeling framework for simulating the co-circulation and spread of diseases across a realistic social contact network.

The rules of this model are relatively simple, where we utilize a susceptible, exposed, infected and recovered (SEIR) model along with introducing a hypothetical disease with a basic reproductive number (i.e., R0). Two infected agents are initialized in one census tract within Western New York to start the simulation. The day in the simulation is broken into three, eight-hour periods characterized as being at home (i.e., either sleeping or getting up), at work (i.e., at work or educational site) and at home (i.e., back at home from work or educational site). 

The agents interact with their social networks, so say a worker becomes exposed to another infected worker, they have a probability of becoming infected. The worker then could then go home and spread the disease to their family network. Furthermore, if in the family network there are children, they could infect others in their school network and so on. Through these interactions one can explore the spread of the disease over days as shown in the figure below. This figure shows how the number of cases spreads outward, reflecting intra-county commuters (for example, between Niagara and Erie counties in New York) as well as longer trips, such as between Buffalo and Rochester.


![A simple example of a disease spread model, stylized on Western, NY.
](disease.png "A simple example of a disease spread model, stylized on Western, NY.")

In addtion the model has the ability to simulate  multiple diseases with independent SEIR progression parameters



## 📋 Project Overview
This repository provides a complete, reproducible workflow for:
1. Building realistic social contact networks for population modeling
2. Simulating single or multiple diseases with independent SEIR progression parameters
3. Running repeated validation experiments to ensure result robustness
4. Visualizing and analyzing simulation outputs with Jupyter Notebooks

The framework is optimized for large-scale populations and provides traceable, structured output results for further academic or applied research.

## 📁 Project Directory Structure

 ```
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
```
