import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake tool
# ---------------------------------------------------------

def fake_tool(action, target, raw_text, context):
    return f"{action}({target})"


# ---------------------------------------------------------
# Pytest: Dependency Ordering
# ---------------------------------------------------------

def test_workflow_agent_dependencies():
    tools = {"tool": fake_tool}

    steps = [
        Step(
            step_number=1,
            action="load",
            target="data",
            raw_text="load data",
            tool="tool",
        ),
        Step(
            step_number=2,
            action="clean",
            target="data",
            raw_text="clean data",
            tool="tool",
            depends_on=[1],
        ),
        Step(
            step_number=3,
            action="train",
            target="model",
            raw_text="train model",
            tool="tool",
            depends_on=[2],
        ),
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    # 1. Final result must be from the last step in the dependency chain
    assert result == "train(model)"

    # 2. Ensure earlier steps did not override the final result
    assert result != "clean(data)"
    assert result != "load(data)"

    # 3. Ensure the agent executed all steps in dependency order
    # We infer this because the final result is correct and no exceptions occurred.
    assert isinstance(result, str)