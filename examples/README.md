# Examples

This directory contains example LangGraph agents demonstrating different features of `langgraph-utils-cli`.

## Examples

### 1. Simple Chatbot (`simple_chatbot.py`)

Basic echo bot demonstrating the simplest possible usage.

```bash
langgraph-cli examples/simple_chatbot.py -m "Hello, how are you?"
```

### 2. Tool Calling Agent (`tool_calling_agent.py`)

Agent that simulates tool calling based on keywords in the message.

```bash
# Triggers weather tool
langgraph-cli examples/tool_calling_agent.py -m "What's the weather like?"

# Triggers time tool
langgraph-cli examples/tool_calling_agent.py -m "What time is it?"

# Regular response
langgraph-cli examples/tool_calling_agent.py -m "Hello!"
```

### 3. Interrupt Agent (`interrupt_agent.py`)

Agent that interrupts for human approval when detecting dangerous actions.

```bash
# Interactive mode (prompts for approval)
langgraph-cli examples/interrupt_agent.py -m "Execute the dangerous action"

# Non-interactive mode (auto-approves)
langgraph-cli examples/interrupt_agent.py --no-interactive -m "Execute the dangerous action"

# Safe action (no interrupt)
langgraph-cli examples/interrupt_agent.py -m "Show me the status"
```

### 4. Async Agent (`async_agent.py`)

Async agent demonstrating async streaming support.

```bash
# Must use --async-mode
langgraph-cli examples/async_agent.py --async-mode -m "Hello!"

# Won't work without async mode
langgraph-cli examples/async_agent.py -m "Hello!"  # Error!
```

## Common Options

All examples support these options:

```bash
# Verbose mode (show node names)
langgraph-cli examples/simple_chatbot.py -v -m "Hello!"

# Custom configuration
langgraph-cli examples/simple_chatbot.py -m "Hello!" -c '{"configurable": {"thread_id": "1"}}'

# Custom graph variable name (if your graph is named differently)
langgraph-cli examples/simple_chatbot.py -g my_graph -m "Hello!"
```

## Running Examples Programmatically

You can also import and use these graphs in Python:

```python
from examples.simple_chatbot import graph

# Invoke directly
result = graph.invoke({
    "messages": [{"role": "user", "content": "Hello!"}]
})
print(result["messages"][-1].content)

# Or use the streaming utilities
from langgraph_utils_cli import stream_graph_updates, prepare_agent_input

input_data = prepare_agent_input(message="Hello!")
for chunk in stream_graph_updates(graph, input_data):
    if chunk.get("chunk"):
        print(chunk["chunk"], end="")
```

## Creating Your Own Agent

To create your own agent compatible with the CLI:

1. Create a Python file (e.g., `my_agent.py`)
2. Define your graph using LangGraph
3. Compile it and assign to a variable (default: `graph`)
4. Run with `langgraph-cli my_agent.py -m "Your message"`

Example template:

```python
from langgraph.graph import StateGraph, MessagesState, START, END

def my_node(state: MessagesState):
    # Your logic here
    return {"messages": [{"role": "assistant", "content": "Response"}]}

# Build graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("my_node", my_node)
graph_builder.add_edge(START, "my_node")
graph_builder.add_edge("my_node", END)

# IMPORTANT: Must compile to a variable
graph = graph_builder.compile()
```

That's it! The CLI will automatically load and run your graph.
