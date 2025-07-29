---
sidebar_position: 1
---

# Getting Started

Welcome to **IOWarp Agents** - specialized AI subagents for scientific computing workflows!

## What are IOWarp Agents?

IOWarp Agents are task-specific AI assistants designed to enhance your scientific computing workflow. Each agent specializes in a particular domain of scientific computing, providing expert guidance and leveraging the IOWarp MCP ecosystem when available.

## Quick Installation

### Project-Specific Installation (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/iowarp/iowarp-agents.git
```

2. **Copy agents to your project:**
```bash
mkdir -p .claude/agents
cp iowarp-agents/agents/*.md .claude/agents/
```

### Global Installation

For use across all your projects:

```bash
# Copy to user-level directory
mkdir -p ~/.claude/agents
cp iowarp-agents/agents/*.md ~/.claude/agents/
```

## Usage in Claude Code

Once installed, agents are automatically available in Claude Code. You can invoke them in two ways:

### Using the /agents Command

```
/agents
```

This opens the agent selection interface where you can choose the appropriate agent for your task.

### Using Natural Language

Simply mention the agent in your request:

- "Use the **data-io-expert** to help me convert this HDF5 file to Parquet"
- "I need the **hpc-performance-expert** to optimize my SLURM job"
- "Ask the **analysis-viz-expert** to create a publication-quality plot"

## Available Agents

| Agent | Specialization | When to Use |
|-------|----------------|-------------|
| **data-io-expert** | Scientific data formats & I/O | Converting between HDF5, ADIOS, Parquet, handling compression |
| **analysis-viz-expert** | Data analysis & visualization | Statistical analysis, creating plots, pandas operations |
| **hpc-performance-expert** | HPC & performance optimization | SLURM jobs, performance profiling, resource optimization |
| **research-doc-expert** | Research & documentation | Literature search, experiment tracking, technical writing |
| **workflow-orchestrator** | Workflow & environment management | Pipeline creation, reproducibility, automation |

## Integration with IOWarp MCPs

These agents work seamlessly with [IOWarp MCPs](https://github.com/iowarp/iowarp-mcps) when available:

```bash
# Install IOWarp MCPs
pip install iowarp-mcps

# Agents will automatically utilize available MCPs
uvx iowarp-mcps pandas  # Used by analysis-viz-expert
uvx iowarp-mcps slurm   # Used by hpc-performance-expert
uvx iowarp-mcps hdf5    # Used by data-io-expert
```

## Example Workflow

Here's a typical scientific computing workflow using IOWarp Agents:

1. **Data Preparation**: Use `data-io-expert` to convert and compress your datasets
2. **Analysis**: Employ `analysis-viz-expert` for statistical analysis and visualization  
3. **High-Performance Computing**: Leverage `hpc-performance-expert` for job optimization
4. **Documentation**: Use `research-doc-expert` to document your methods and findings
5. **Workflow Automation**: Apply `workflow-orchestrator` to create reproducible pipelines

## Next Steps

- Browse all available agents on the [home page](/)
- Learn about creating custom agents
- Explore advanced usage patterns
- Check out example workflows

---

Need help? Check out our [GitHub Issues](https://github.com/iowarp/iowarp-agents/issues) or join the [community discussion](https://grc.zulipchat.com/#narrow/channel/518574-iowarp-mcps).
