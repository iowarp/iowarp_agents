# IOWarp Agents

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai/code)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-orange)](https://opencode.ai/)
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

# Example: Install warpio agents for Claude Code
uvx iowarp-agents install warpio-executor claude local
uvx iowarp-agents install warpio-jarvis-deployment-planner claude local

# Example: Install warpio agents for OpenCode (specialized versions)
uvx iowarp-agents install warpio-executor opencode local
uvx iowarp-agents install warpio-jarvis-deployment-planner opencode local
```

## Available Agents

### Claude Code Agents (Primary Platform)

<div align="center">

| 🤖 **Agent** | ⚙️ **Specialization** | 📋 **Description** | ⚡ **Install Command** |
|:---|:---:|:---|:---|
| **`data-io-expert`** | Data I/O | Scientific data formats & I/O operations | `uvx iowarp-agents install data-io-expert claude local` |
| **`analysis-viz-expert`** | Analysis | Data analysis & visualization workflows | `uvx iowarp-agents install analysis-viz-expert claude local` |
| **`hpc-performance-expert`** | HPC | High-performance computing & optimization | `uvx iowarp-agents install hpc-performance-expert claude local` |
| **`research-doc-expert`** | Research | Literature search & documentation | `uvx iowarp-agents install research-doc-expert claude local` |
| **`workflow-orchestrator`** | Workflow | Pipeline creation & environment management | `uvx iowarp-agents install workflow-orchestrator claude local` |

</div>

### Warpio Agents (Deployment Orchestration)

**Warpio** agents specialize in deployment orchestration and MCP-based execution workflows. They are **platform-specific** with dedicated versions for Claude Code and OpenCode environments, each optimized for their respective platforms.

<div align="center">

| 🤖 **Agent** | ⚙️ **Specialization** | 📋 **Description** | 🎯 **Platform & Install Command** |
|:---|:---:|:---|:---|
| **`warpio-executor`** | MCP Execution | Universal executor for MCP-based plans | **Claude Code:** `uvx iowarp-agents install warpio-executor claude local`<br>**OpenCode:** `uvx iowarp-agents install warpio-executor opencode local` |
| **`warpio-jarvis-deployment-planner`** | Deployment Planning | Jarvis-CD deployment planning | **Claude Code:** `uvx iowarp-agents install warpio-jarvis-deployment-planner claude local`<br>**OpenCode:** `uvx iowarp-agents install warpio-jarvis-deployment-planner opencode local` |

</div>

**📁 Location**: [`agents/warpio-agents/`](agents/warpio-agents/) - [View README](agents/warpio-agents/README.md)

## Usage

### Claude Code Agents

Once installed, agents are automatically available in Claude Code:

```
/agents
```

Or use natural language:
- "Use the data-io-expert to help me convert this HDF5 file"
- "I need the hpc-performance-expert to optimize my SLURM job"
- "Use the warpio-executor to run this MCP deployment plan"
- "I need warpio-jarvis-deployment-planner for Jarvis-CD deployment"

### OpenCode Agents (Warpio Agents)

Once installed, agents are automatically available in OpenCode:

```
/agents
```

#### Usage in OpenCode
- **Tab key**: Switch between primary agents (jarvis-deployment-planner)
- **@mention**: Invoke subagents manually (`@executor run this plan`)
- **Auto-invoke**: Primary agents automatically call subagents when needed
- **Navigation**: Use Ctrl+Right/Left to switch between parent/child sessions

**Example Workflow**:
1. Use `jarvis-deployment-planner` for creating MCP-based deployment plans
2. Planner automatically invokes `@executor` to run the plan
3. Monitor execution progress and handle errors
4. Navigate between planning and execution sessions

## Integration with IOWarp MCPs

These agents work seamlessly with [IOWarp MCPs](https://github.com/iowarp/iowarp-mcps):

```bash
# Install MCPs for enhanced agent capabilities
uvx iowarp-mcps pandas  # Used by analysis-viz-expert
uvx iowarp-mcps slurm   # Used by hpc-performance-expert
uvx iowarp-mcps jarvis  # Used by warpio agents for deployment
```

#### Manual Installation
```bash
# Global installation (Claude Code)
mkdir -p ~/.claude/agents
cp agents/warpio-agents/claude/executor.md ~/.claude/agents/
cp agents/warpio-agents/claude/jarvis-deployment-planner.md ~/.claude/agents/

# Global installation (OpenCode) 
mkdir -p ~/.config/opencode/agent
cp agents/warpio-agents/opencode/executor.md ~/.config/opencode/agent/warpio-executor.md
cp agents/warpio-agents/opencode/jarvis-deployment-planner.md ~/.config/opencode/agent/warpio-jarvis-deployment-planner.md

# Project-specific installation (Claude Code)
mkdir -p .claude/agents
cp agents/warpio-agents/claude/*.md .claude/agents/

# Project-specific installation (OpenCode)
mkdir -p .opencode/agent
cp agents/warpio-agents/opencode/executor.md .opencode/agent/warpio-executor.md
cp agents/warpio-agents/opencode/jarvis-deployment-planner.md .opencode/agent/warpio-jarvis-deployment-planner.md
```

### Configuration Features

The OpenCode versions (in `opencode/` folder) include:
- **Advanced YAML frontmatter** with mode, model, temperature, tools, and permissions
- **Optimized for OpenCode** with specific model recommendations (Claude 3.5 Sonnet, LMStudio)
- **Detailed permission controls** for enhanced security
- **MCP-focused execution** with restricted tool access for executor
- **Research capabilities** for deployment planner with WebFetch integration

The Claude Code versions (in `claude/` folder) include:
- **Simplified YAML frontmatter** optimized for Claude Code compatibility
- **Streamlined configuration** with basic name, description, and tools
- **Focus on usability** within Claude's agent ecosystem

See [`agents/warpio-agents/README.md`](agents/warpio-agents/README.md) for detailed configuration examples and platform-specific optimizations.

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