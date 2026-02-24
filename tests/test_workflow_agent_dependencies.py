from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step

def fake_tool(action, target, raw_text, context):
    return f"{action}({target})"

if __name__ == "__main__":
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

    print("\n=== EXECUTING DEPENDENCY TEST ===")
    result = agent.execute(plan)
    print("\nFinal result:")
    print(result)
