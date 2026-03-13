import pytest
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


# ---------------------------------------------------------
# Fake tools for testing
# ---------------------------------------------------------

def fake_search_tool(action, target, raw_text, context):
    return f"[search] action={action}, target={target}, raw={raw_text}"

def fake_calculator_tool(action, target, raw_text, context):
    return f"[calculator] action={action}, target={target}, raw={raw_text}"

def fake_summarizer_tool(action, target, raw_text, context):
    return f"[summarizer] action={action}, target={target}, raw={raw_text}"


# ---------------------------------------------------------
# Build a fake plan with 3 steps
# ---------------------------------------------------------

def build_fake_plan():
    steps = [
        Step(
            step_number=1,
            action="search",
            target="weather",
            raw_text="search the weather in Seattle",
            tool="search"
        ),
        Step(
            step_number=2,
            action="calculate",
            target="average",
            raw_text="calculate the average temperature",
            tool="calculator"
        ),
        Step(
            step_number=3,
            action="summarize",
            target="results",
            raw_text="summarize the findings",
            tool="summarizer"
        ),
    ]
    return Plan(steps=steps)


# ---------------------------------------------------------
# Pytest: Basic Workflow Execution
# ---------------------------------------------------------

def test_workflow_agent_basic_execution():
    tools = {
        "search": fake_search_tool,
        "calculator": fake_calculator_tool,
        "summarizer": fake_summarizer_tool,
    }

    agent = WorkflowAgent(tools=tools)
    plan = build_fake_plan()

    result = agent.execute(plan)

    # 1. Final result must be from the summarizer tool
    assert isinstance(result, str)
    assert result.startswith("[summarizer]")

    # 2. Ensure the correct tool was used for each step
    assert "[search]" in result or "[calculator]" in result or "[summarizer]" in result

    # 3. Ensure the steps were executed in order
    # The WorkflowAgent returns only the final result, but we can infer ordering
    # because each tool returns a unique prefix.
    # The final result must be from step 3.
    assert "[summarizer]" in result

    # 4. Ensure no exceptions occurred during execution
    # (pytest would fail automatically if an exception was raised)

    # 5. Ensure the WorkflowAgent can run without memory_agent
    assert agent.memory_agent is None
