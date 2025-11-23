# CODEX.md

Guide for Codex agents working on the RapidChiplet repository.

## Project snapshot

- **Purpose**: Rapid design-space exploration for chiplet-based systems with optional cycle-accurate validation.
- **Core scripts**: `rapidchiplet.py` orchestrates analyses; helpers live in `helpers.py`, `validation.py`, `booksim_wrapper.py`, and `generate_*.py`.
- **Sim backends**: Mathematical analysis by default, BookSim2 for detailed timing, Netrace for trace-driven flows.

## Environment setup

1. **Install Python deps**
   ```bash
   pip install -r requirements.txt
   ```
2. **Build BookSim2**
   ```bash
   cd booksim2/src
   make
   ```
3. **Build Netrace tools**
   ```bash
   cd netrace
   gcc export_trace.c netrace.c -o export_trace
   ```

Keep `booksim2/src/Makefile` and `Makefile.vcpkg` in sync when adding flags for Linux vs Windows builds.

## Directory landmarks

| Path | Notes |
| --- | --- |
| `inputs/` | Hierarchical JSON inputs (designs reference chiplets, placements, routing tables, etc.). |
| `experiments/` | Batch exploration specs (see `case_study.json`). |
| `results/`, `plots/`, `images/` | Outputs for metrics, charts, and visualizations. |
| `booksim2/`, `netrace/` | External simulators that must compile before dependent workflows run. |

## High-frequency commands

Analyze a design with all standard metrics (area/power/layout/cache) plus latency & throughput:

```bash
python rapidchiplet.py -df inputs/designs/my_design.json -rf results.json -as -ps -ls -c -l -t
```

Other staples:

```bash
# BookSim2 validation
python rapidchiplet.py -df inputs/designs/my_design.json -rf results.json -bs

# Experiment sweep
python run_experiment.py -e experiments/<experiment.json>

# Visuals & plots
python visualizer.py -df inputs/designs/<design.json>
python create_plots.py -rf results/<results.json> -pt latency_vs_load
```

Generation utilities share a `-df` (design file) plus output flag convention, e.g.:

```bash
python generate_routing.py -df inputs/designs/<design.json> -rtf inputs/routing_tables/<name>.json -ra splif
```

## Workflow tips for Codex

- **Validate inputs early**: `validation.py` emits detailed diagnostics; skip with `-validate false` only when iterating.
- **Cache awareness**: Helpers cache length and link metrics; avoid deleting `__pycache__` during runs.
- **BookSim bridging**: When touching `booksim_wrapper.py`, mirror any new CLI flags inside `inputs/booksim_configs/`.
- **Trace handling**: `parse_netrace_trace.py` converts Netrace outputs into `inputs/traces/*.json`; large traces stay in `netrace/traces_out/`.
- **Docs parity**: Update both the English `.md` and localized variants (`RapidChiplet_*.md`) when changing user-facing behavior.

## Testing & verification

- **Python**: Use targeted script runs; no dedicated test harness today.
- **BookSim2**: Run `make clean && make` if modifying router models or headers such as `pipefifo.hpp`.
- **Netrace**: Rebuild `export_trace` after editing `netrace.c` or related headers.

## When editing

- Keep JSON references consistent (design files break if relative paths change).
- Prefer `rg` for searches; large repos make `grep` slow.
- Document complex logic with short comments; avoid narrating obvious assignments.
- Never revert user changes unless explicitly asked; repo may be intentionally dirty.

Stick to these guardrails and Codex agents can jump straight into performance analysis, experiment setup, or simulator maintenance with minimal rediscovery.
