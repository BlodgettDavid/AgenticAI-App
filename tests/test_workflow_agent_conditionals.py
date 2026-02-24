from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step

def fake_tool(action, target, raw_text, context):
    return f"ran {action}"

if __name__ == "__main__":
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
            condition="step_1 contains 'NOPE'"
        ),
        Step(
            step_number=3,
            action="third",
            target="z",
            raw_text="third step",
            tool="tool",
            condition="step_1 contains 'ran'"
        ),
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    print("\n=== EXECUTING CONDITIONAL TEST ===")
    result = agent.execute(plan)
    print("\nFinal result:")
    print(result)