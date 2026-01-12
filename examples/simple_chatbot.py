"""
Simple chatbot example for langgraph-utils-cli.

This demonstrates the most basic usage: a chatbot that responds to messages.

Run with:
    langgraph-cli examples/simple_chatbot.py -m "Hello, how are you?"
"""
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END


def chatbot(state: MessagesState):
    """Simple chatbot that echoes with a prefix."""
    messages = state["messages"]
    last_message = messages[-1]

    # Simple echo response
    response = f"You said: {last_message.content}. This is a simple echo bot!"

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
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile - this is what the CLI will load
graph = graph_builder.compile()


if __name__ == "__main__":
    # Test locally
    result = graph.invoke({
        "messages": [{"role": "user", "content": "Hello!"}]
    })
    print(result["messages"][-1].content)
