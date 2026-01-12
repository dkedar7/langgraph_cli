"""
Async agent example.

This demonstrates an async agent that can be run with --async-mode.

Run with:
    langgraph-cli examples/async_agent.py --async-mode -m "Hello!"
"""
import asyncio
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END


async def async_chatbot(state: MessagesState):
    """Async chatbot that simulates async operations."""
    messages = state["messages"]
    last_message = messages[-1]

    # Simulate async operation (e.g., API call)
    await asyncio.sleep(0.1)

    response = f"[Async] You said: {last_message.content}"

    return {
        "messages": [
            {
                "role": "assistant",
                "content": response
            }
        ]
    }


# Build the graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("chatbot", async_chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile
graph = graph_builder.compile()


if __name__ == "__main__":
    # Test locally
    async def test():
        result = await graph.ainvoke({
            "messages": [{"role": "user", "content": "Hello!"}]
        })
        print(result["messages"][-1].content)

    asyncio.run(test())
