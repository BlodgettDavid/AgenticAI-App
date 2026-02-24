import time
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


def slow_tool(action, target, raw_text, context):
    time.sleep(1)
    return f"{action}({target})"

if __name__ == "__main__":
    tools = {"tool": slow_tool}

    steps = [
        Step(step_number=1, action="load", target="A", raw_text="", tool="tool"),
        Step(step_number=2, action="load", target="B", raw_text="", tool="tool"),
        Step(step_number=3, action="combine", target="C", raw_text="", tool="tool", depends_on=[1, 2]),
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    print("\n=== PARALLEL EXECUTION TEST ===")
    start = time.time()
    result = agent.execute(plan)
    end = time.time()

    print("\nFinal result:", result)
    print("Elapsed time:", end - start)