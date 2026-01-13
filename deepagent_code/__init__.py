"""
deepagent_code - A Claude Code-style CLI for running LangGraph agents.

This package provides utilities for streaming from LangGraph agents,
handling interrupts, and running agents from the command line.
"""

from deepagent_code.utils import (
    parse_interrupt_value,
    serialize_action_request,
    serialize_review_config,
    process_interrupt,
    extract_todos_from_content,
    extract_reflection_from_content,
    serialize_tool_calls,
    clean_content_from_tool_dicts,
    process_message_content,
    process_tool_message,
    process_ai_message,
    prepare_agent_input,
    stream_graph_updates,
    resume_graph_from_interrupt,
    astream_graph_updates,
    aresume_graph_from_interrupt,
)

__version__ = "0.1.0"

__all__ = [
    "parse_interrupt_value",
    "serialize_action_request",
    "serialize_review_config",
    "process_interrupt",
    "extract_todos_from_content",
    "extract_reflection_from_content",
    "serialize_tool_calls",
    "clean_content_from_tool_dicts",
    "process_message_content",
    "process_tool_message",
    "process_ai_message",
    "prepare_agent_input",
    "stream_graph_updates",
    "resume_graph_from_interrupt",
    "astream_graph_updates",
    "aresume_graph_from_interrupt",
]
