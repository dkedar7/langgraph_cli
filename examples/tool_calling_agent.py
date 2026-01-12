"""
Tool calling agent example.

This demonstrates an agent that can call tools (simulated without requiring API keys).

Run with:
    langgraph-cli examples/tool_calling_agent.py -m "What's the weather like?"
"""
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END


def simple_agent(state: MessagesState):
    """
    Agent that simulates tool calling based on keywords.

    In a real implementation, this would use an LLM with tool calling.
    """
    messages = state["messages"]
    last_message = messages[-1]
    content = last_message.content.lower()

    # Simulate tool call detection
    if "weather" in content:
        # Simulate calling a weather tool
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_weather_001",
                            "name": "get_weather",
                            "args": {"location": "San Francisco"}
                        }
                    ]
                }
            ]
        }
    elif "time" in content:
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": [
                        {
                            "id": "call_time_001",
                            "name": "get_current_time",
                            "args": {"timezone": "UTC"}
                        }
                    ]
                }
            ]
        }
    else:
        # Regular response
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "I'm a simple agent. Try asking about weather or time!"
                }
            ]
        }


# Build the graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("agent", simple_agent)
graph_builder.add_edge(START, "agent")
graph_builder.add_edge("agent", END)

# Compile
graph = graph_builder.compile()


if __name__ == "__main__":
    # Test locally
    result = graph.invoke({
        "messages": [{"role": "user", "content": "What's the weather like?"}]
    })
    print("Tool calls:", result["messages"][-1].tool_calls)
