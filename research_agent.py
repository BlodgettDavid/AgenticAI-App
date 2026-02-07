class LLMClient:
    """
    Minimal LLM client wrapper.
    Replace the body of complete() with your actual LLM API call.
    """

    def complete(self, prompt: str) -> str:
        # TODO: Replace with real LLM call
        # For now, simulate a response
        return f"(LLM summary) {prompt[:200]}..."

class Message:
    def __init__(self, role: str, content: str):
        self.role = role
        self.content = content

    def __repr__(self):
        return f"{self.role}: {self.content}"

class Tool:
    name = "base_tool"
    description = "Base tool interface"

    def run(self, query: str) -> str:
        raise NotImplementedError("Tool subclasses must implement run().")

class DefinitionTool(Tool):
    name = "define"
    triggers = ["define", "what is", "explain"]

    def run(self, query: str) -> str:
        return f"[Definition of {query}]: This is a placeholder definition for '{query}'."

class SearchTool(Tool):
    name = "search"
    description = "Placeholder search tool"
    triggers = ["search", "look up", "find", "google"]

    def run(self, query: str) -> str:
        return f"[Search results for: {query}] (placeholder)"


class SummarizerTool(Tool):
    name = "summarizer"
    triggers = []  # no triggers; used internally

    def __init__(self, llm_client):
        self.llm = llm_client

    def run(self, text: str) -> str:
        prompt = (
            "Summarize the following content in a clear, concise paragraph.\n\n"
            f"CONTENT:\n{text}\n\nSUMMARY:"
        )
        return self.llm.complete(prompt)


class ResearchAgent:
    def __init__(self, tools=None):
        self.tools = tools or []
        self.history = []

    def add_message(self, role: str, content: str):
        msg = Message(role, content)
        self.history.append(msg)   

    def choose_tools(self, user_input: str):
        text = user_input.lower()
        matched = []

        for tool in self.tools:
            for trigger in getattr(tool, "triggers", []):
                if trigger in text:
                    matched.append(tool)
                    break

        return matched



    def extract_query(self, user_input: str, tool):
        text = user_input.lower()
        for trigger in tool.triggers:
            if trigger in text:
                return text.replace(trigger, "").strip()
        return user_input

    def run(self):
        print("ResearchAgent ready. Type 'exit' to quit.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            self.add_message("user", user_input)

            tools = self.reason_about_tools(user_input)


            if tools:
                results = []

                for tool in tools:
                    query = self.extract_query(user_input, tool)
                    result = tool.run(query)
                    results.append((tool, result))

                combined_text = "\n\n".join(r for _, r in results)

                summarizer = next((t for t in self.tools if t.name == "summarizer"), None)
                if summarizer:
                    final_answer = summarizer.run(combined_text)
                else:
                    final_answer = combined_text

                self.add_message("tool", final_answer)

                tool_names = ", ".join(t.name for t, _ in results)
                print(f"[Tools used: {tool_names}] {final_answer}")

            else:
                response = f"I received your message: '{user_input}'. No tool needed yet."
                self.add_message("assistant", response)
                print(response)


    def reason_about_tools(self, user_input: str):
        """
        Reasoning layer:
        - If tools match, use them.
        - BUT if the only tool matched is DefinitionTool AND the input is a question,
        override and use SearchTool instead.
        - If no tools match but the input is a question, use SearchTool.
        """
        tools = self.choose_tools(user_input)

        # If tools matched, check for override conditions
        if tools:
            # If the only tool is DefinitionTool AND the input is a question → override to SearchTool
            if (len(tools) == 1 
                and tools[0].name == "define"
                and user_input.strip().endswith("?")):

                search_tool = next((t for t in self.tools if t.name == "search"), None)
                if search_tool:
                    return [search_tool]

            # Otherwise, use the matched tools
            return tools

        # If no tools matched but the input is a question → use SearchTool
        if user_input.strip().endswith("?"):
            search_tool = next((t for t in self.tools if t.name == "search"), None)
            if search_tool:
                return [search_tool]

        # No tools
        return []


if __name__ == "__main__":
    llm = LLMClient()
    tools = [
        SearchTool(),
        DefinitionTool(),
        SummarizerTool(llm_client=llm)
    ]
    agent = ResearchAgent(tools=tools)
    agent.run()