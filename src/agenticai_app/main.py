from agenticai import (
    ResearchAgent,
    SearchTool,
    DefinitionTool,
    SummarizerTool,
    LLMClient,
)

def main():
    llm = LLMClient()
    tools = [
        SearchTool(),
        DefinitionTool(),
        SummarizerTool(llm_client=llm)
    ]

    agent = ResearchAgent(tools=tools)

    print("ResearchAgent ready. Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        result = agent.run(user_input)

        if result["type"] == "multi_step_detected":
            print("It looks like you're asking for a multi-step task.")
            print("\nRaw steps:")
            for i, step in enumerate(result["raw_steps"], 1):
                print(f"{i}. {step}")

            print("\nParsed steps:")
            for i, step in enumerate(result["parsed_steps"], 1):
                print(f"{i}. action={step['action']}, target={step['target']}, tool={step['tool']}")
            continue

        if result["type"] == "tool_result":
            tools_used = ", ".join(result["tools_used"])
            print(f"[Tools used: {tools_used}] {result['answer']}")
            continue

        if result["type"] == "assistant_response":
            print(result["answer"])

if __name__ == "__main__":
    main()