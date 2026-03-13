import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake global refinement tool
# ---------------------------------------------------------

def improve_tool(action, target, raw_text, context):
    # Start with 500 chars if no previous final_output exists
    prev = context.get("final_output", "X" * 500)
    return prev[: len(prev) // 2]


# ---------------------------------------------------------
# Pytest: Global Refinement Behavior
# ---------------------------------------------------------

def test_workflow_agent_global_refinement():
    tools = {"tool": improve_tool}

    steps = [
        Step(
            step_number=1,
            action="improve",
            target="text",
            raw_text="improve text",
            tool="tool",
        )
    ]

    plan = Plan(
        steps=steps,
        global_refine_until="len(final_output) < 50",
        max_global_passes=5,
    )

    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    # Assertions
    assert isinstance(result, str)
    assert len(result) < 50          # global refinement condition
    assert len(result) < 500         # must shrink from initial size
    assert len(result) >= 15         # should not shrink too far (max passes)
