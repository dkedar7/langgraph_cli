"""Tests for utility functions."""
import pytest
from langgraph_utils_cli.utils import (
    parse_interrupt_value,
    serialize_action_request,
    process_interrupt,
    extract_todos_from_content,
    serialize_tool_calls,
    prepare_agent_input,
)


class TestParseInterruptValue:
    """Tests for parse_interrupt_value function."""

    def test_tuple_format_two_elements(self):
        """Test parsing two-element tuple format."""
        action_requests = [{"tool": "test_tool", "args": {}}]
        review_configs = [{"allowed_decisions": ["approve", "reject"]}]
        interrupt_value = (action_requests, review_configs)

        actions, configs = parse_interrupt_value(interrupt_value)

        assert actions == action_requests
        assert configs == review_configs

    def test_tuple_format_single_element_with_dict(self):
        """Test parsing single-element tuple with dict value."""

        class MockInterrupt:
            def __init__(self):
                self.value = {
                    "action_requests": [{"tool": "test"}],
                    "review_configs": [{"allowed_decisions": ["approve"]}],
                }

        interrupt_value = (MockInterrupt(),)
        actions, configs = parse_interrupt_value(interrupt_value)

        assert len(actions) == 1
        assert actions[0]["tool"] == "test"
        assert len(configs) == 1


class TestSerializeActionRequest:
    """Tests for serialize_action_request function."""

    def test_dict_format(self):
        """Test serializing dict format action."""
        action = {
            "tool": "test_tool",
            "tool_call_id": "call_123",
            "args": {"param": "value"},
            "description": "Test action",
        }

        result = serialize_action_request(action, index=0)

        assert result["tool"] == "test_tool"
        assert result["tool_call_id"] == "call_123"
        assert result["args"] == {"param": "value"}
        assert result["description"] == "Test action"

    def test_object_format(self):
        """Test serializing object format action."""

        class MockAction:
            tool = "test_tool"
            tool_call_id = "call_123"
            args = {"param": "value"}
            description = "Test action"

        result = serialize_action_request(MockAction(), index=0)

        assert result["tool"] == "test_tool"
        assert result["tool_call_id"] == "call_123"

    def test_fallback_tool_call_id(self):
        """Test fallback tool_call_id generation."""
        action = {"tool": "test_tool", "args": {}}

        result = serialize_action_request(action, index=5)

        assert result["tool_call_id"] == "call_5"


class TestExtractTodosFromContent:
    """Tests for extract_todos_from_content function."""

    def test_string_with_array(self):
        """Test extracting from string with array."""
        content = "Updated todo list to [{'content': 'Task 1', 'status': 'pending'}]"

        result = extract_todos_from_content(content)

        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["content"] == "Task 1"

    def test_dict_format(self):
        """Test extracting from dict format."""
        content = {"todos": [{"content": "Task 1", "status": "pending"}]}

        result = extract_todos_from_content(content)

        assert isinstance(result, list)
        assert len(result) == 1

    def test_list_format(self):
        """Test extracting from direct list."""
        content = [{"content": "Task 1", "status": "pending"}]

        result = extract_todos_from_content(content)

        assert result == content


class TestSerializeToolCalls:
    """Tests for serialize_tool_calls function."""

    def test_basic_serialization(self):
        """Test basic tool call serialization."""

        class MockToolCall:
            id = "call_123"
            name = "test_tool"
            args = {"param": "value"}

        tool_calls = [MockToolCall()]
        result = serialize_tool_calls(tool_calls)

        assert len(result) == 1
        assert result[0]["id"] == "call_123"
        assert result[0]["name"] == "test_tool"

    def test_skip_tools(self):
        """Test skipping specified tools."""

        class MockToolCall:
            def __init__(self, name):
                self.id = f"call_{name}"
                self.name = name
                self.args = {}

        tool_calls = [
            MockToolCall("think_tool"),
            MockToolCall("execute_tool"),
            MockToolCall("write_todos"),
        ]

        result = serialize_tool_calls(tool_calls, skip_tools=["think_tool", "write_todos"])

        assert len(result) == 1
        assert result[0]["name"] == "execute_tool"


class TestPrepareAgentInput:
    """Tests for prepare_agent_input function."""

    def test_message_input(self):
        """Test preparing message input."""
        result = prepare_agent_input(message="Hello, agent!")

        assert "messages" in result
        assert result["messages"][0]["role"] == "user"
        assert result["messages"][0]["content"] == "Hello, agent!"

    def test_decisions_input(self):
        """Test preparing decisions input."""
        decisions = [{"type": "approve"}]

        result = prepare_agent_input(decisions=decisions)

        # Should return a Command object
        assert hasattr(result, "resume")

    def test_raw_input(self):
        """Test preparing raw input."""
        raw = {"custom": "data"}

        result = prepare_agent_input(raw_input=raw)

        assert result == raw

    def test_no_input_raises_error(self):
        """Test that no input raises ValueError."""
        with pytest.raises(ValueError, match="Must provide one of"):
            prepare_agent_input()

    def test_multiple_inputs_raises_error(self):
        """Test that multiple inputs raise ValueError."""
        with pytest.raises(ValueError, match="Can only provide one of"):
            prepare_agent_input(message="Hello", decisions=[])


class TestProcessInterrupt:
    """Tests for process_interrupt function."""

    def test_full_interrupt_processing(self):
        """Test complete interrupt processing."""
        action_requests = [
            {"tool": "test_tool", "tool_call_id": "call_1", "args": {"param": "value"}}
        ]
        review_configs = [{"allowed_decisions": ["approve", "reject"]}]
        interrupt_value = (action_requests, review_configs)

        result = process_interrupt(interrupt_value)

        assert "action_requests" in result
        assert "review_configs" in result
        assert len(result["action_requests"]) == 1
        assert result["action_requests"][0]["tool"] == "test_tool"
        assert len(result["review_configs"]) == 1
