# tests/test_workflow_agent_while.py

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
# Build a plan with a single looping step
# ---------------------------------------------------------

def build_loop_plan():
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
    return Plan(steps=steps)


# ---------------------------------------------------------
# Run the WorkflowAgent
# ---------------------------------------------------------

if __name__ == "__main__":
    tools = {
        "counter": fake_counter_tool,
    }

    agent = WorkflowAgent(tools=tools)
    plan = build_loop_plan()

    print("\n=== EXECUTING WORKFLOW AGENT (WHILE LOOP TEST) ===")
    result = agent.execute(plan)

    print("\nFinal result:")
    print(result)