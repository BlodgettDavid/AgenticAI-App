from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step

def summary_tool(action, target, raw_text, context):
    # Fake summary that gets shorter each time
    prev = context.get("step_1", "X" * 500)
    return prev[: len(prev) // 2]

if __name__ == "__main__":
    tools = {"tool": summary_tool}

    steps = [
        Step(
            step_number=1,
            action="summarize",
            target="text",
            raw_text="summarize text",
            tool="tool",
            refine_until="len(step_1) < 50",
            max_refinements=5,
        )
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    print("\n=== REFINEMENT TEST ===")
    result = agent.execute(plan)
    print("Final result length:", len(result))
    print("Final result:", result)