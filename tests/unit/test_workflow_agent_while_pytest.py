import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake tool for testing while-loop behavior
# ---------------------------------------------------------

def fake_counter_tool(action, target, raw_text, context):
    """
    Each time this tool is called, it increments a counter in the context.
    Returns a string like 'count=1', 'count=2', etc.
    """
    count = context.get("counter", 0) + 1
    context["counter"] = count
    return f"count={count}"


# ---------------------------------------------------------
# Pytest: While Loop Behavior
# ---------------------------------------------------------

def test_workflow_agent_while_loop():
    tools = {"counter": fake_counter_tool}

    steps = [
        Step(
            step_number=1,
            action="increment",
            target="counter",
            raw_text="increment counter",
            tool="counter",
            repeat_until="step_1 contains 'count=3'"
        )
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    # Assertions
    assert isinstance(result, str)
    assert result == "count=3"
