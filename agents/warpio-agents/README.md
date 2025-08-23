# Warpio Agents

[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-orange)](https://opencode.ai)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blue)](https://claude.ai/code)
[![MCP](https://img.shields.io/badge/MCP-Enabled-green)](https://modelcontextprotocol.org)

Specialized deployment orchestration agents for the Jarvis-CD platform and universal MCP execution. These agents provide research-driven deployment planning and step-by-step execution capabilities optimized for both OpenCode and Claude Code environments.

## Directory Structure

```
warpio-agents/
├── claude/                          # Claude Code optimized agents
│   ├── executor.md
│   └── jarvis-deployment-planner.md
└── opencode/                        # OpenCode optimized agents
    ├── executor.md
    └── jarvis-deployment-planner.md
```

## Available Agents

<div align="center">

| 🤖 **Agent** | 🎯 **Platform** | � **Location** | �📋 **Description** | ⚡ **Install Command** |
|:---|:---:|:---:|:---|:---|
| **`executor`** | Claude Code | `claude/` | Universal MCP executor (Claude-optimized) | `uvx iowarp-agents install warpio-executor claude local` |
| **`jarvis-deployment-planner`** | Claude Code | `claude/` | Jarvis-CD deployment planning (Claude-optimized) | `uvx iowarp-agents install warpio-jarvis-deployment-planner claude local` |
| **`executor`** | OpenCode | `opencode/` | Universal MCP executor with advanced OpenCode configuration | `uvx iowarp-agents install warpio-executor opencode local` |
| **`jarvis-deployment-planner`** | OpenCode | `opencode/` | Advanced Jarvis-CD deployment planning with OpenCode features | `uvx iowarp-agents install warpio-jarvis-deployment-planner opencode local` |

</div>

## Agent Specifications

### Claude Code Agents (`claude/` folder)

**`claude/executor.md`** - Universal MCP Executor (Claude Code)
- **Format**: Simplified YAML frontmatter with `name` and basic `tools`
- **Tools**: Adaptive to available MCP tools
- **Purpose**: Execute MCP-based plans with error handling
- **Compatibility**: Optimized for Claude Code's agent system

**`claude/jarvis-deployment-planner.md`** - Jarvis Deployment Planner (Claude Code) 
- **Format**: Simplified YAML frontmatter with `name` and basic `tools`
- **Tools**: WebFetch enabled for documentation research
- **Purpose**: Create comprehensive Jarvis-CD deployment plans
- **Compatibility**: Optimized for Claude Code's agent system

### OpenCode Agents (`opencode/` folder)

**`opencode/executor.md`** - Universal MCP Executor (OpenCode)
- **Mode**: `subagent` (can be invoked by other agents)  
- **Model**: `lmstudio/devstral-small-2505` optimized
- **Temperature**: `0.2` for precise execution
- **Tools**: MCP tools only (all other tools disabled/denied)
- **Permissions**: Restricted execution environment
- **Purpose**: Execute any MCP-based plans step-by-step

**`opencode/jarvis-deployment-planner.md`** - Jarvis Deployment Planner (OpenCode)
- **Mode**: `primary` (direct user interaction)
- **Model**: `anthropic/claude-sonnet-4-20250514` for complex reasoning
- **Temperature**: `0.2` for balanced creativity/precision
- **Tools**: WebFetch, Read, Edit, Write enabled
- **Permissions**: WebFetch requires permission, Bash access denied
- **Purpose**: Research-driven Jarvis-CD deployment planning

## Platform-Specific Optimizations

### Why Separate Folders?

Each platform has different agent configuration requirements:

**Claude Code (`claude/` folder):**
- Simple YAML frontmatter with `name`, `description`, `tools`
- Tools specified as text strings
- Focus on compatibility with Claude's agent system
- Streamlined for ease of use

**OpenCode (`opencode/` folder):**
- Advanced YAML frontmatter with detailed configuration
- Granular tool permissions (`true`/`false`/`ask`/`allow`/`deny`)
- Agent modes (`primary`/`subagent`) for workflow orchestration
- Model specifications and temperature control
- Permission systems for security

### File Organization Benefits

1. **Clear Separation**: No confusion about which version to use
2. **Platform Optimization**: Each version fully optimized for its target platform
3. **Easy Maintenance**: Updates can be made per platform without affecting the other
4. **CLI Automation**: The IOWarp Agents CLI automatically detects and installs from the correct folder

## Key Features

### 🎯 **Deployment Planning Excellence**
- **Research-Driven**: Automatically researches documentation to understand any package or workflow
- **7-Phase Planning**: Systematic approach from environment prep to validation
- **MCP-Only Execution**: All deployment through standardized MCP tool calls
- **Command Synthesis**: Creates exact, executable Jarvis commands from documentation

### 🔄 **Universal Execution Capability**  
- **Any MCP Tools**: Adapts to whatever MCP tools are available (Jarvis, ADIOS, HDF5, etc.)
- **Error Handling**: Stops on failures with clear troubleshooting guidance
- **Progress Monitoring**: Real-time execution status and step-by-step reporting
- **Plan Interpretation**: Handles structured plans or natural language prompts

### 📚 **Comprehensive Jarvis Knowledge**
- **Pipeline Management**: Create, configure, and manage complex workflows
- **Package Types**: Services, applications, interceptors, custom packages
- **Resource Optimization**: System profiling and optimal placement strategies  
- **Multi-Node Deployments**: Cluster configuration and distributed execution

## Platform Integration

### OpenCode Integration
```bash
# Install OpenCode-optimized agents (from opencode/ folder)
uvx iowarp-agents install warpio-executor opencode local
uvx iowarp-agents install warpio-jarvis-deployment-planner opencode local

# Manual installation
mkdir -p ~/.config/opencode/agent
cp opencode/executor.md ~/.config/opencode/agent/warpio-executor.md
cp opencode/jarvis-deployment-planner.md ~/.config/opencode/agent/warpio-jarvis-deployment-planner.md

# Usage in OpenCode
# Primary agent: Use Tab to cycle to jarvis-deployment-planner
# Subagent: Automatically invoked by planner for execution
```

### Claude Code Integration  
```bash
# Install Claude Code-compatible agents (from claude/ folder)
uvx iowarp-agents install warpio-executor claude local
uvx iowarp-agents install warpio-jarvis-deployment-planner claude local

# Manual installation
mkdir -p ~/.claude/agents
cp claude/executor.md ~/.claude/agents/
cp claude/jarvis-deployment-planner.md ~/.claude/agents/

# Usage in Claude Code
/agents
# Select from available agents menu
```

## Workflow Examples

### Example 1: IOR Benchmark Deployment
```bash
User: "Deploy IOR benchmark with 8 processes using Jarvis"

Planner: Creates 7-phase deployment plan with MCP tool calls
Executor: Executes each step (config, pipeline, packages, run)
Result: Complete IOR deployment ready for execution
```

### Example 2: Hermes + Gray Scott Pipeline
```bash
User: "Set up Hermes storage with Gray Scott simulation"

Planner: Researches both packages, creates multi-package pipeline
Executor: Handles service + interceptor + application deployment  
Result: Complete data-centric workflow with storage optimization
```

## Advanced Features

### 📋 **Documentation Integration**
- Real-time research of official Jarvis documentation
- Command validation against current documentation
- Best practices enforcement
- Troubleshooting guidance

### 🛠️ **MCP Tool Discovery**
- Automatic detection of available MCP tools
- Adaptive execution based on environment capabilities
- Support for all IOWarp MCP implementations
- Extensible to any MCP-compliant tool

### ⚡ **Performance Optimization**
- Resource graph-based deployment planning
- Network topology-aware package placement
- Load balancing across cluster nodes
- Performance monitoring integration

## Integration with IOWarp MCPs

These agents work seamlessly with [IOWarp MCPs](https://github.com/iowarp/iowarp-mcps):

```bash
# Install Jarvis MCP for deployment execution
uvx iowarp-mcps jarvis

# Install additional MCPs for enhanced capabilities  
uvx iowarp-mcps adios     # For binary data operations
uvx iowarp-mcps hdf5      # For hierarchical data
uvx iowarp-mcps slurm     # For HPC job scheduling
```

## Configuration Examples

### OpenCode Agent Configuration (`opencode/` files)
The OpenCode versions include advanced YAML frontmatter:

```yaml
---
# opencode/jarvis-deployment-planner.md
description: "Advanced Jarvis-CD deployment planning..."
mode: primary
model: anthropic/claude-sonnet-4-20250514
temperature: 0.2
tools:
    write: true
    edit: true
    bash: false
    read: true
    webfetch: ask
permissions:
    edit: allow
    bash: deny
    webfetch: ask
---
```

```yaml
---
# opencode/executor.md  
description: "Execute any MCP-based plans..."
mode: subagent
model: lmstudio/devstral-small-2505
temperature: 0.2
tools:
    write: false
    edit: false
    bash: false
    read: false
permissions:
    edit: deny
    bash: deny
    webfetch: deny
---
```

### Claude Code Agent Configuration (`claude/` files)
The Claude Code versions use simplified frontmatter:

```yaml
---
# claude/jarvis-deployment-planner.md
name: warpio-jarvis-deployment-planner
description: "Use this agent when you need to plan deployments..."
tools: Read, Write, Edit, Glob, LS, WebFetch
---
```

```yaml
---
# claude/executor.md
name: warpio-executor
description: "Execute any MCP-based plans or prompts..."
tools: 
---
```

## Requirements

- **IOWarp Agents CLI**: `uvx iowarp-agents` 
- **MCP Support**: Model Context Protocol compatible environment
- **Jarvis-CD**: For deployment execution (via Jarvis MCP)
- **Platform**: OpenCode.ai or Claude Code

For more information about the broader IOWarp Agents ecosystem, see the [main repository](../../README.md).

---

**Ready to orchestrate your deployments?** Install the agents and start planning with research-driven precision!