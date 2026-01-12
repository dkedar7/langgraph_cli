"""
Agent with interrupts example.

This demonstrates an agent that interrupts for human approval.

Run with:
    langgraph-cli examples/interrupt_agent.py -m "Execute the dangerous action"

Or non-interactive:
    langgraph-cli examples/interrupt_agent.py --no-interactive -m "Execute the dangerous action"
"""
from typing import Literal
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.types import interrupt


def check_action(state: MessagesState):
    """Check if action needs approval."""
    messages = state["messages"]
    last_message = messages[-1]
    content = last_message.content.lower()

    if "dangerous" in content or "delete" in content:
        # Request approval
        action_request = {
            "tool": "execute_dangerous_action",
            "tool_call_id": "call_danger_001",
            "args": {"action": "delete_database"},
            "description": "This will delete the production database!"
        }

        review_config = {
            "allowed_decisions": ["approve", "reject"]
        }

        # Trigger interrupt
        interrupt_value = ([action_request], [review_config])
        interrupt(interrupt_value)

        # This will only execute if approved
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "Action approved and executed!"
                }
            ]
        }
    else:
        # Safe action, no approval needed
        return {
            "messages": [
                {
                    "role": "assistant",
                    "content": "Safe action executed without approval."
                }
            ]
        }


# Build the graph
graph_builder = StateGraph(MessagesState)
graph_builder.add_node("check_action", check_action)
graph_builder.add_edge(START, "check_action")
graph_builder.add_edge("check_action", END)

# Compile with interrupt support
graph = graph_builder.compile()


if __name__ == "__main__":
    # Test locally (will raise interrupt)
    try:
        result = graph.invoke({
            "messages": [{"role": "user", "content": "Execute the dangerous action"}]
        })
        print(result)
    except Exception as e:
        print(f"Interrupt triggered: {e}")
