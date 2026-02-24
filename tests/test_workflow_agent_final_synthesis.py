from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step

def synth_tool(action, target, raw_text, context):
    return f"SYNTHESIZED:\n{raw_text}"

def step_tool(action, target, raw_text, context):
    return raw_text.upper()

if __name__ == "__main__":
    tools = {
        "step_tool": step_tool,
        "synth_tool": synth_tool,
    }

    steps = [
        Step(1, "process", "text", "hello", "step_tool"),
        Step(2, "process", "text", "world", "step_tool"),
    ]

    plan = Plan(
        steps=steps,
        final_synthesis="synth_tool"
    )

    agent = WorkflowAgent(tools=tools)

    print("\n=== FINAL SYNTHESIS TEST ===")
    result = agent.execute(plan)
    print(result)