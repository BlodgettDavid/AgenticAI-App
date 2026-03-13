import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


def fake_tool(action, target, raw_text, context):
    return f"{action}({target})"


def test_workflow_agent_dependencies_out_of_order():
    tools = {"tool": fake_tool}

    # Intentionally scrambled order
    steps = [
        Step(
            step_number=3,
            action="train",
            target="model",
            raw_text="train model",
            tool="tool",
            depends_on=[2],
        ),
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
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    result = agent.execute(plan)

    # The DAG should reorder steps into: 1 → 2 → 3
    assert result == "train(model)"

    # Ensure earlier steps did not override the final result
    assert result != "clean(data)"
    assert result != "load(data)"

    # Ensure the output is a string (sanity check)
    assert isinstance(result, str)
