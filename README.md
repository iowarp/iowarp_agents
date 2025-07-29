# IOWarp Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai/code)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)

Specialized AI subagents for scientific computing workflows. Built for Claude Code, designed to be adaptable as other systems develop similar capabilities.

**More info at**: [https://iowarp.github.io/iowarp-agents/](https://iowarp.github.io/iowarp-agents/)

## Quick Installation

### Simple Command

```bash
# Install agents interactively
uvx iowarp-agents install
```

### List All Agents

```bash
# See all available agents
uvx iowarp-agents list
```

### Get Started with a Simple Command

```bash
# Example: Install workflow orchestrator for Claude Code locally
uvx iowarp-agents install workflow-orchestrator claude local

# Example: Install data-io expert globally
uvx iowarp-agents install data-io-expert claude global
```

## Available Agents

<div align="center">

| 🤖 **Agent** | ⚙️ **Specialization** | 📋 **Description** | ⚡ **Install Command** |
|:---|:---:|:---|:---|
| **`data-io-expert`** | Data I/O | Scientific data formats & I/O operations | `uvx iowarp-agents install data-io-expert claude local` |
| **`analysis-viz-expert`** | Analysis | Data analysis & visualization workflows | `uvx iowarp-agents install analysis-viz-expert claude local` |
| **`hpc-performance-expert`** | HPC | High-performance computing & optimization | `uvx iowarp-agents install hpc-performance-expert claude local` |
| **`research-doc-expert`** | Research | Literature search & documentation | `uvx iowarp-agents install research-doc-expert claude local` |
| **`workflow-orchestrator`** | Workflow | Pipeline creation & environment management | `uvx iowarp-agents install workflow-orchestrator claude local` |

</div>

## Usage

Once installed, agents are automatically available in Claude Code:

```
/agents
```

Or use natural language:
- "Use the data-io-expert to help me convert this HDF5 file"
- "I need the hpc-performance-expert to optimize my SLURM job"

## Integration with IOWarp MCPs

These agents work seamlessly with [IOWarp MCPs](https://github.com/iowarp/iowarp-mcps):

```bash
# Install MCPs for enhanced agent capabilities
uvx iowarp-mcps pandas  # Used by analysis-viz-expert
uvx iowarp-mcps slurm   # Used by hpc-performance-expert
```

## Contributing

We welcome contributions in any form!

### Ways to Contribute:

- **Submit Issues**: Report any problems or bugs you encounter
- **Request Features**: Submit an issue requesting a new agent or functionality  
- **Develop**: Try your hand at developing new agents

Find our comprehensive **development guide** [here](https://github.com/iowarp/iowarp-agents/wiki).

### Get Help & Connect

**Reach out to us on Zulip**: [IOWarp Community Chat](https://grc.zulipchat.com/#narrow/channel/518574-iowarp-mcps)

---