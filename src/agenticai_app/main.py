from agenticai.planning.planning_agent import PlanningAgent
from agenticai.workflow.workflow_agent import WorkflowAgent
from agenticai.tools import SearchTool, DefinitionTool, SummarizerTool


def main():
    print("Phase 2 AgenticAI CLI. Type 'exit' to quit.")

    tools = {
        "search": SearchTool(),
        "define": DefinitionTool(),
        "summarize": SummarizerTool(),
    }

    planner = PlanningAgent(tool_registry=tools)
    workflow = WorkflowAgent(tools=tools)

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Pass raw text directly into create_plan()
        plan = planner.create_plan(user_input, user_input=user_input)

        # Execute the plan (correct method)
        result = workflow.execute(plan)

        print(f"Result: {result}")


if __name__ == "__main__":
    main()