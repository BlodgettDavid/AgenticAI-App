import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake refinement tool
# ---------------------------------------------------------

def summary_tool(action, target, raw_text, context):
    # Fake summary that gets shorter each time
    prev = context.get("step_1", "X" * 500)
    return prev[: len(prev) // 2]


# ---------------------------------------------------------
# Pytest: Refinement Behavior
# ---------------------------------------------------------

def test_workflow_agent_refinement_loop():
    tools = {"tool": summary_tool}

    steps = [
        Step(
            step_number=1,
            action="summarize",
            target="text",
            raw_text="summarize text",
            tool="tool",
            refine_until='len(context["step_1"]) < 50',
            max_refinements=5,
        )
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    assert isinstance(result, str)
    assert len(result) < 50
    assert len(result) < 500
    assert len(result) >= 15