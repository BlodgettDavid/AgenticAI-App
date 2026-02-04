from agenticai.core.agent import BaseAgent
from agenticai.core.message import Message
from agenticai.tools.search_tool import SearchTool


class ResearchAgent(BaseAgent):
    """
    A simple agent that:
    - receives user input
    - decides whether to use the search tool
    - returns a Message object
    """

    def __init__(self):
        super().__init__(name="ResearchAgent")
        self.search = SearchTool()

    def step(self, user_input: str) -> Message:
        """
        Very simple logic:
        - if the user asks to 'search', call the SearchTool
        - otherwise, echo a placeholder response
        """
        if user_input.lower().startswith("search "):
            query = user_input[len("search "):]
            result = self.search.run(query)
            return Message(role="assistant", content=result, tool_name="search")

        # Default behavior
        return Message(role="assistant", content=f"You said: {user_input}")
    
if __name__ == "__main__":
    agent = ResearchAgent()
    print("ResearchAgent ready. Type something (or 'quit').")

    while True:
        user_input = input("> ")
        if user_input.lower() in {"quit", "exit"}:
            break

        response = agent.step(user_input)
        print(f"{response.role}: {response.content}")