# IOWarp Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai/code)

Specialized AI subagents for scientific computing workflows. Built for Claude Code, designed to be adaptable as other systems develop similar capabilities.

## Overview

IOWarp Agents are task-specific AI assistants that enhance your scientific computing workflow. Each agent specializes in a particular domain, providing expert guidance and leveraging the IOWarp MCP ecosystem when available.

## Available Agents

| Agent | Specialization | Key Features |
|-------|----------------|--------------|
| **data-io-expert** | Scientific data formats & I/O | HDF5, ADIOS, Parquet, compression |
| **analysis-viz-expert** | Data analysis & visualization | Statistical analysis, plotting, pandas operations |
| **hpc-performance-expert** | HPC & performance optimization | Job scheduling, profiling, resource management |
| **research-doc-expert** | Research & documentation | Literature search, experiment tracking, technical writing |
| **workflow-orchestrator** | Workflow & environment management | Pipeline creation, reproducibility, automation |

## Quick Start

### 🚀 Easy Installation (Recommended)

Use our beautiful CLI tool for the best experience:

```bash
# Install and use with uvx (recommended)
uvx iowarp-agents install

# Or install the CLI globally
pip install iowarp-agents
iowarp-agents install
```

**Interactive Installation Example:**
```bash
$ uvx iowarp-agents install

🤖 IOWarp Agents CLI

Select an agent to install:

1) 💾 Data Io Expert       Scientific data formats and I/O operations
2) 📊 Analysis Viz Expert  Data analysis and visualization  
3) 🚀 Hpc Performance Expert  HPC and performance optimization
4) 📚 Research Doc Expert  Research literature and documentation
5) ⚙️ Workflow Orchestrator  Workflow and environment management

Enter your choice [1]: 2

Select target platform:
1) Claude Code  Claude Code AI assistant with subagent support

Select installation scope:
1) Local project      Install in current project only
2) Global installation Install for all projects

✅ Installation Successful!
```

### 📋 CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `list` | List all available agents | `uvx iowarp-agents list --detailed` |
| `install` | Install an agent interactively | `uvx iowarp-agents install` |
| `install <agent> <platform> <scope>` | Direct installation | `uvx iowarp-agents install workflow-orchestrator claude local` |

### 📦 Manual Installation

If you prefer manual installation:

1. **Project-specific agents** (recommended):
```bash
# Clone this repository
git clone https://github.com/iowarp/iowarp-agents.git

# Copy agents to your project
mkdir -p .claude/agents
cp iowarp-agents/agents/*.md .claude/agents/
```

2. **Global agents** (for all projects):
```bash
# Copy to user-level directory
mkdir -p ~/.claude/agents
cp iowarp-agents/agents/*.md ~/.claude/agents/
```

### Usage in Claude Code

Once installed, agents are automatically available. Invoke them using:

```
/agents
```

Or use natural language:
- "Use the data-io-expert to help me convert this HDF5 file to Parquet"
- "I need the hpc-performance-expert to optimize my SLURM job"

## Agent Capabilities

### Data I/O Expert
- Format conversion (HDF5, ADIOS, Parquet, NetCDF)
- Compression optimization
- I/O performance tuning
- Metadata management

### Analysis & Visualization Expert
- Statistical analysis
- Data exploration
- Publication-quality plots
- Time series analysis

### HPC Performance Expert
- SLURM job optimization
- Performance profiling
- Resource estimation
- Parallel computing guidance

### Research Documentation Expert
- Literature search and organization
- Experiment tracking
- Technical documentation
- Reproducibility standards

### Workflow Orchestrator
- Pipeline design and automation
- Environment management (Lmod, Conda)
- Workflow tools (Snakemake, Nextflow)
- Reproducible workflows

## Integration with IOWarp MCPs

These agents are designed to work seamlessly with [IOWarp MCPs](https://github.com/iowarp/iowarp-mcps) when available in your project:

```bash
# Install IOWarp MCPs
pip install iowarp-mcps

# Agents will automatically utilize available MCPs
uvx iowarp-mcps pandas  # Used by analysis-viz-expert
uvx iowarp-mcps slurm   # Used by hpc-performance-expert
```

## Creating Custom Agents

Create your own agents by following this template:

```markdown
---
name: your-agent-name
description: Brief description of when to use this agent
tools: Bash, Read, Write, Edit, Grep, Glob, LS, Task
---

You are a [Role] Expert specialized in [domain].

## Core Expertise
[List key areas of expertise]

## Best Practices
[Key principles and guidelines]

## Common Workflows
[Typical tasks and how to approach them]
```

Save as `.claude/agents/your-agent-name.md` in your project.

## Contributing

We welcome contributions! Please:
1. Fork the repository
2. Create your agent following our template
3. Submit a pull request with a clear description

## Future Compatibility

While currently optimized for Claude Code, these agents are designed with portability in mind. As other AI systems develop similar subagent capabilities, we'll update this repository to ensure compatibility.

## Support

- **Issues**: [GitHub Issues](https://github.com/iowarp/iowarp-agents/issues)
- **Discussions**: [IOWarp Community](https://grc.zulipchat.com/#narrow/channel/518574-iowarp-mcps)

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

*Part of the [IOWarp](https://github.com/iowarp) ecosystem for scientific computing*
