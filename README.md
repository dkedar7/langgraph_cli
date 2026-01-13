# deepagent-code

A Claude Code-style CLI for running LangGraph agents from the terminal.

## Installation

```bash
git clone https://github.com/dkedar7/deepagent-code.git
cd deepagent-code
pip install -e .
```

## Quick Start

To use the default agent:
```bash
export ANTHROPIC_API_KEY="your_anthropic_api_key_here"
deepagent-code
```

But the real power comes from specifying your own agent file:
```bash
deepagent-code path/to/your_agent.py:graph
```

Or specifying via environment variable:
```bash
export DEEPAGENT_AGENT_SPEC="path/to/your_agent.py:graph"
deepagent-code
```

This launches an interactive conversation loop with your agent.

## Usage

```bash
# Interactive mode (default)
deepagent-code my_agent.py

# With initial message
deepagent-code my_agent.py -m "Hello, agent!"

# Non-interactive (auto-approve interrupts)
deepagent-code my_agent.py --no-interactive
```

## Commands

In the interactive loop:
- `/q` or `/quit` - Exit
- `/c` - Clear conversation history
- `/h` or `/help` - Show help

## Environment Variables

```bash
# Agent location (path/to/file.py:variable_name)
export DEEPAGENT_AGENT_SPEC="my_agent.py:graph"
deepagent-code

# Working directory
export DEEPAGENT_WORKSPACE_ROOT="/path/to/workspace"

# Configuration
export DEEPAGENT_CONFIG='{"configurable": {"thread_id": "1"}}'
```

## CLI Options

```
Usage: deepagent-code [OPTIONS] [GRAPH_FILE]

Options:
  -g, --graph-name TEXT           Graph variable name (default: "graph")
  -m, --message TEXT              Initial message
  -c, --config TEXT               Config JSON or file path
  --interactive/--no-interactive  Handle interrupts (default: interactive)
  --async-mode/--sync-mode        Async streaming (default: sync)
  -v, --verbose                   Verbose output
```

## Programmatic Use

```python
from deepagent_code import stream_graph_updates, prepare_agent_input

input_data = prepare_agent_input(message="Hello!")

for chunk in stream_graph_updates(graph, input_data):
    if chunk.get("chunk"):
        print(chunk["chunk"], end="")
```

## License

MIT License - see LICENSE file for details.
