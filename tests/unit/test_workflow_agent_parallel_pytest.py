import time
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.planning.plan import Plan, Step


def slow_tool(action, target, raw_text, context):
    time.sleep(1)
    return f"{action}({target})"


def test_workflow_agent_parallel_execution():
    tools = {"tool": slow_tool}

    steps = [
        Step(step_number=1, action="load", target="A", raw_text="", tool="tool"),
        Step(step_number=2, action="load", target="B", raw_text="", tool="tool"),
        Step(step_number=3, action="combine", target="C", raw_text="", tool="tool", depends_on=[1, 2]),
    ]

    plan = Plan(steps=steps)
    agent = WorkflowAgent(tools=tools)

    start = time.time()
    result = agent.execute(plan)
    end = time.time()
    elapsed = end - start

    # Final result must come from the last step
    assert result == "combine(C)"

    # Parallelism check:
    # Steps 1 and 2 each sleep 1 second → should run in parallel
    # Step 3 sleeps 1 second → total should be ~2 seconds if sequential
    # With correct batching, total should be ~1 + epsilon
    assert elapsed < 2.0, f"Execution took too long ({elapsed}s), parallelism may be broken"
    assert elapsed > 1.0, f"Execution was too fast ({elapsed}s), step 3 may not have waited"
