# tests/test_workflow_agent_basic.py
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
# Run the WorkflowAgent
# ---------------------------------------------------------

if __name__ == "__main__":
    tools = {
        "search": fake_search_tool,
        "calculator": fake_calculator_tool,
        "summarizer": fake_summarizer_tool,
    }

    agent = WorkflowAgent(tools=tools)
    plan = build_fake_plan()

    print("\n=== EXECUTING WORKFLOW AGENT ===")
    result = agent.execute(plan)

    print("\nFinal result:")
    print(result)