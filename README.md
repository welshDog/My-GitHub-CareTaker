![CI](https://github.com/welshDog/My-GitHub-CareTaker/actions/workflows/ci.yml/badge.svg)
![Hosted on IPFS](https://img.shields.io/badge/Hosted_on-IPFS-65c2cb?logo=ipfs)
![Web3 Enabled](https://img.shields.io/badge/Web3-Enabled-FF3E00?logo=ethereum)

# GitHub CareTaker

![CI](https://github.com/welshDog/GitHub-Hyper-Agent-BROski/actions/workflows/ci.yml/badge.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![HyperCode: Active](https://img.shields.io/badge/HyperCode-Active-blueviolet)

The ultimate autonomous agent suite designed to optimize, clean, and visualize your GitHub ecosystem. Built with a neurodivergent-first approach, Caretaker automates the boring stuff so you can stay in the zone.

## 🚀 Key Features

- **HyperCode Duplicate Merge**: Intelligent analysis and consolidation of redundant code and repositories.
- **Neurodivergent UX**: Features like Hyperfocus Mode and 3D constellation visualizations.
- **Agent Swarm**: Multi-agent architecture for specialized tasks (Cleanup, Documentation, Security).
- **Automated Infrastructure**: Built-in CI/CD, security auditing, and performance metrics.
- **Auto Architecture Mapping**: Scans your repo and generates interactive `architecture_map.html` and detailed `architecture_map.json`, capturing modules, routes, and agent boundaries.

## 🗺 Architecture Map

This repo includes an auto-generated architecture explorer:

- `architecture_map.html` – interactive dependency + API map
- `architecture_map.json` – machine-readable graph for agents

Regenerate anytime:

```bash
python caretaker_cli.py explore --owner welshDog
```

### System Overview
The v2.0 architecture features a clear separation between the Core logic and Plugin Agents:
- **Core Layer**: `caretaker.core` handles configuration, GitHub API client, and reporting.
- **Plugin Layer**: `caretaker.plugins` contains specialized agents (Monitor, Repo Explorer, Link Recovery).
- **Hybrid Stack**: Seamless integration between Python backend (Flask) and JavaScript frontend (Express/React).

## 🧠 Self-Aware Architecture

CareTaker isn't just a collection of scripts; it understands its own structure.

Run the explorer to generate a live map of the system:

```bash
python caretaker_cli.py explore --owner welshDog --output latest_arch.json
```

This generates:

- `latest_arch.json`: Full dependency + call graph of the running agents.
- `architecture_report.md`: Principal-engineer style review (risks, refactors, security notes).

This architectural self-awareness allows agents to:
1.  **Monitor themselves**: The MonitorAgent checks the health of other plugins.
2.  **Optimize performance**: Lazy-loading ensures only required agents are active.
3.  **Heal configuration**: The system can detect missing dependencies and alert the user.

## 🌟 Pinned Repositories

These links are live projects in my ecosystem – CareTaker doesn’t own them, it helps **orchestrate and maintain** them.

Here are the top projects currently in the Hyperfocus Constellation:

1.  **[GitHub-Hyper-Agent-BROski](https://github.com/welshDog/GitHub-Hyper-Agent-BROski)**
    *The autonomous agent framework driving this ecosystem. Features self-healing infrastructure, agent swarms, and neurodivergent-friendly tools.*

2.  **[-Hyperfocus-3D-Constellation](https://github.com/welshDog/-Hyperfocus-3D-Constellation)**
    *The world's most advanced 3D repository visualization designed for neurodivergent minds.*

3.  **[hyperfocus-constellation](https://github.com/welshDog/hyperfocus-constellation)**
    *A star map of all the hyperfocus zone repos, visualizing the connections between your projects.*

4.  **[hyperfocus-constellation-paper](https://github.com/welshDog/hyperfocus-constellation-paper)**
    *Revolutionary 3D interactive research paper on vibe coding and hyperfocus superpowers.*

5.  **[Caretaker-CLI](https://github.com/welshDog/caretaker-cli)**
    *The command-line interface for the Caretaker suite, enabling quick local management of your repo ecosystem.*

6.  **[Caretaker-Core](https://github.com/welshDog/caretaker-core)**
    *The foundational logic powering the Caretaker agents, with plugin support for custom workflows.*

## 🛠️ HyperCode Operations

### Duplicate Merge Status
**Status:** ✅ Executed
**Report:** `reports/duplicates.json`

The HyperCode engine has scanned the codebase for redundancies. Redundant JavaScript test files have been consolidated into TypeScript equivalents to improve maintainability and type safety.

## 📦 Installation & Usage

### 1. Clone this repo

```bash
git clone https://github.com/welshDog/My-GitHub-CareTaker.git
cd My-GitHub-CareTaker
```

### 2. Start the web UI (JS server)

```bash
cd caretaker-js/server
npm install
npm start
```

### 3. (Optional) Run the Python CLI

```bash
cd ../..
pip install -r requirements.txt
python caretaker_cli.py --username welshDog
```
