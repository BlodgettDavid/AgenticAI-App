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


class SearchTool(Tool):
    name = "search"
    description = "Placeholder search tool"

    def run(self, query: str) -> str:
        return f"[Search results for: {query}] (placeholder)"


class ResearchAgent:
    def __init__(self, tools=None):
        self.tools = tools or []
        self.history = []

    def add_message(self, role: str, content: str):
        msg = Message(role, content)
        self.history.append(msg)

    def choose_tool(self, user_input: str):
        # Very simple heuristic for now
        for tool in self.tools:
            if tool.name in user_input.lower():
                return tool
        return None

    def run(self):
        print("ResearchAgent ready. Type 'exit' to quit.")

        while True:
            user_input = input("You: ")
            if user_input.lower() == "exit":
                break

            self.add_message("user", user_input)

            tool = self.choose_tool(user_input)
            if tool:
                result = tool.run(user_input)
                self.add_message("tool", result)
                print(f"[Tool: {tool.name}] {result}")
            else:
                response = f"I received your message: '{user_input}'. No tool needed yet."
                self.add_message("assistant", response)
                print(response)


if __name__ == "__main__":
    tools = [SearchTool()]
    agent = ResearchAgent(tools=tools)
    agent.run()