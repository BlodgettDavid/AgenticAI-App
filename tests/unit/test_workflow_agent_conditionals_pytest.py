import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake tool
# ---------------------------------------------------------

def fake_tool(action, target, raw_text, context):
    return f"ran {action}"


# ---------------------------------------------------------
# Pytest: Conditional Execution
# ---------------------------------------------------------

def test_workflow_agent_conditionals():
    tools = {"tool": fake_tool}

    steps = [
        Step(
            step_number=1,
            action="first",
            target="x",
            raw_text="first step",
            tool="tool"
        ),
        Step(
            step_number=2,
            action="second",
            target="y",
            raw_text="second step",
            tool="tool",
            condition="'NOPE' in context['step_1']"
        ),
        Step(
            step_number=3,
            action="third",
            target="z",
            raw_text="third step",
            tool="tool",
            condition="'ran' in context['step_1']"
        ),
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    # Step 1 always runs
    step1_output = "ran first"
    assert result == "ran third"  # final result is from step 3

    # Step 2 should be skipped because condition is false
    # "'NOPE' in context['step_1']" → False
    # So step 2 result should NOT be "ran second"
    # We infer this because final result is from step 3, not step 2
    assert result != "ran second"

    # Step 3 should run because "'ran' in context['step_1']" → True
    assert result == "ran third"