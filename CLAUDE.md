# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

RapidChiplet is a framework for designing and evaluating chiplet-based systems with a focus on Network-on-Chip (NoC) performance analysis. It combines high-level design space exploration with cycle-accurate simulation using BookSim2 and supports real network traces via Netrace.

## Setup and Dependencies

### Initial Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build BookSim2 simulator (required for cycle-accurate simulation):**
   ```bash
   cd booksim2/src
   make
   cd ../../
   ```

3. **Build Netrace trace tools (required for real network traces):**
   ```bash
   cd netrace
   gcc export_trace.c netrace.c -o export_trace
   cd ../
   ```

### Core Dependencies

- Python 3.x
- matplotlib==3.8.4
- networkx==3.3
- numpy==2.1.1
- BookSim2 (C++ simulator)
- Netrace (C trace processing tools)

## Architecture Overview

### Core Modules

- **`rapidchiplet.py`**: Main orchestrator that coordinates all analysis components and handles different metric computations
- **`helpers.py`**: Utility functions for data processing, JSON encoding/decoding, and chiplet transformations
- **`validation.py`**: Input validation system that checks design constraints and reports errors
- **`booksim_wrapper.py`**: Interface between RapidChiplet and BookSim2 cycle-accurate simulator
- **`visualizer.py`**: Chip and network visualization tools
- **`generate_*.py` modules**: Various input generation utilities for routing, traffic, topology, etc.

### Input System Architecture

RapidChiplet uses a modular input system where designs are specified through JSON files in the `inputs/` directory:

- **`designs/`**: Master design files that reference all other inputs
- **`chiplets/`**: Individual chiplet specifications with dimensions, power, and PHY configurations
- **`placements/`**: Physical placement of chiplets and interposer routers
- **`topologies/`**: Network connectivity definitions
- **`routing_tables/`**: Pre-computed routing tables for different algorithms
- **`technologies/`**: Process technology parameters
- **`packagings/`**: Packaging and interposer specifications
- **`traffic_by_*/`**: Traffic patterns (by chiplet or by unit)
- **`traces/`**: Real network traces in RapidChiplet format

### Analysis Pipeline

1. **Input Loading**: Design files are parsed and validated through `validation.py`
2. **Intermediate Computation**: Link lengths, routing tables, and other derived parameters are calculated
3. **Metric Computation**: Various analysis modules compute area, power, latency, throughput, etc.
4. **Simulation**: Optional BookSim2 cycle-accurate simulation for detailed performance analysis
5. **Visualization**: Results can be visualized through `visualizer.py` and `create_plots.py`

## Common Development Tasks

### Running Basic Analysis

```bash
# Analyze a design with basic metrics
python3 rapidchiplet.py -df inputs/designs/<design_file> -rf <results_file> -as -ps -ls -c

# Include latency and throughput analysis
python3 rapidchiplet.py -df inputs/designs/<design_file> -rf <results_file> -as -ps -ls -c -l -t

# Run BookSim2 cycle-accurate simulation
python3 rapidchiplet.py -df inputs/designs/<design_file> -rf <results_file> -bs
```

### Generating Inputs

```bash
# Generate routing tables
python3 generate_routing.py -df inputs/designs/<design_file> -rtf <routing_table_file> -ra splif

# Generate synthetic traffic patterns
python3 generate_traffic.py -df inputs/designs/<design_file> -tf <traffic_file> -tp random_uniform -par "{'injection_rate': 0.1}"

# Parse Netrace traces
python3 parse_netrace_trace.py -df inputs/designs/<design_file> -if netrace/traces_out/<trace_name>.json -of <trace_name>.json
```

### Running Experiments

```bash
# Run automated design space exploration
python3 run_experiment.py -e experiments/<experiment_file>

# Reproduce paper results (runs for ~24 hours)
python3 reproduce_paper_results.py
```

### Visualization

```bash
# Visualize complete chip design
python3 visualizer.py -df inputs/designs/<design_name>

# Create performance plots
python3 create_plots.py -rf results/<results-file> -pt latency_vs_load
```

## Design Space Experiments

Experiments are defined in `experiments/` directory as JSON files specifying parameter ranges. The system automatically generates all combinations and runs analyses for each. Key experiment parameters include:

- `grid_scale`: Chip array dimensions (e.g., "4x4", "8x8")
- `topology`: Network topology types
- `traffic_pattern`: Synthetic traffic patterns
- `routing_algorithm`: Routing algorithms (splif, sptmr)
- `technology`: Process technology nodes
- `chiplets_can_relay`: Whether chiplets can forward traffic

## Routing Algorithms

- **SPLIF (Shortest Path Lowest ID First)**: Chooses shortest paths with deterministic tie-breaking
- **SPTMR (Shortest Path Turn Model Random)**: Shortest paths with random turn model selection for deadlock freedom

## File Organization Patterns

- Results are stored in `results/` directory
- Plots are generated in `plots/` directory
- Chip visualizations go to `images/` directory
- Input files follow a hierarchical referencing system where design files point to specific component files
- Intermediate files (routing tables, traffic patterns) are cached for reuse

## Validation System

The validation system (`validation.py`) checks:
- Chiplet dimensions and constraints
- Placement validity
- Topology connectivity
- Technology parameter consistency
- Design rule compliance

Validation can be disabled with `-validate false` flag for rapid prototyping.

## BookSim Integration

BookSim2 configurations are stored in `inputs/booksim_configs/` and automatically generated based on the RapidChiplet design. The wrapper handles:
- Topology translation
- Traffic pattern conversion
- Result collection and analysis
- Multi-simulation management for different traffic loads