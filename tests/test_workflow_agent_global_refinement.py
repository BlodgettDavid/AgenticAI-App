from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step

def improve_tool(action, target, raw_text, context):
    prev = context.get("final_output", "X" * 500)
    return prev[: len(prev) // 2]

if __name__ == "__main__":
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

    print("\n=== GLOBAL REFINEMENT TEST ===")
    result = agent.execute(plan)
    print("Final result length:", len(result))
    print("Final result:", result)
