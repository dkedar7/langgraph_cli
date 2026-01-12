# langgraph-utils-cli

Universal CLI for running any LangGraph agent from the terminal. Framework-agnostic with robust interrupt handling.

## Installation

```bash
git clone https://github.com/yourusername/langgraph-utils-cli.git
cd langgraph-utils-cli
pip install -e .
```

## Quick Start

Create `my_agent.py`:

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def chatbot(state: MessagesState):
    return {"messages": [{"role": "assistant", "content": "Hello!"}]}

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

graph = graph_builder.compile()
```

Run it:

```bash
langgraph-cli my_agent.py -m "Hello!"
```

## Usage

```bash
# Basic
langgraph-cli my_agent.py -m "Your message"

# With config
langgraph-cli my_agent.py -m "Hello" -c '{"configurable": {"thread_id": "1"}}'

# Custom graph variable
langgraph-cli my_agent.py -g custom_graph -m "Hello"

# Async mode
langgraph-cli my_agent.py --async-mode -m "Hello"

# Non-interactive (auto-approve interrupts)
langgraph-cli my_agent.py --no-interactive -m "Hello"
```

## Environment Variables

Compatible with `deepagent-lab`:

```bash
# Agent location (path/to/file.py:variable_name)
export DEEPAGENT_AGENT_SPEC="my_agent.py:graph"
langgraph-cli -m "Hello!"

# Working directory
export DEEPAGENT_WORKSPACE_ROOT="/path/to/workspace"

# Configuration
export DEEPAGENT_CONFIG='{"configurable": {"thread_id": "1"}}'

# Stream mode (updates or values)
export DEEPAGENT_STREAM_MODE="values"
```

CLI arguments override environment variables.

## CLI Options

```
Usage: langgraph-cli [OPTIONS] [GRAPH_FILE]

Options:
  -g, --graph-name TEXT           Graph variable name (default: "graph")
  -m, --message TEXT              Input message
  -c, --config TEXT               Config JSON or file path
  --interactive/--no-interactive  Handle interrupts (default: interactive)
  --async-mode/--sync-mode        Async streaming (default: sync)
  --stream-mode TEXT              Stream mode (default: "updates")
  -v, --verbose                   Verbose output
```

## Programmatic Use

```python
from langgraph_utils_cli import stream_graph_updates, prepare_agent_input

input_data = prepare_agent_input(message="Hello!")

for chunk in stream_graph_updates(graph, input_data):
    if chunk.get("chunk"):
        print(chunk["chunk"], end="")
```

Async variant:

```python
from langgraph_utils_cli import astream_graph_updates

async for chunk in astream_graph_updates(graph, input_data):
    if chunk.get("chunk"):
        print(chunk["chunk"], end="")
```

## Examples

See `examples/` directory:
- `simple_chatbot.py` - Basic usage
- `tool_calling_agent.py` - Tool calls
- `interrupt_agent.py` - Human-in-the-loop
- `async_agent.py` - Async streaming

## License

MIT License - see LICENSE file for details.
