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

            if isinstance(tools, dict) and "multi_step" in tools:
                print("It looks like you're asking for a multi-step task.")
                print("Here are the steps I detected:")
                for i, step in enumerate(tools["multi_step"], 1):
                    print(f"{i}. {step}")
                print("Should I proceed with these steps in this order?")
                continue

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
                if self.needs_clarification(user_input):
                    response = self.clarifying_question(user_input)
                else:
                    response = f"I received your message: '{user_input}'. No tool needed yet."

                self.add_message("assistant", response)
                print(response)


    def reason_about_tools(self, user_input: str):

        lowered = user_input.lower()

        # Detect multi-step tasks BEFORE tool selection
        steps = self.detect_multi_step_task(user_input)
        if steps:
            extracted = self.extract_steps(user_input)
            return {"multi_step": extracted or steps}

        # 1) Multi-tool reasoning FIRST
        if "define" in lowered and ("search" in lowered or "look up" in lowered):
            define_tool = next((t for t in self.tools if t.name == "define"), None)
            search_tool = next((t for t in self.tools if t.name == "search"), None)
            if define_tool and search_tool:
                return [define_tool, search_tool]

        if ("search" in lowered or "look up" in lowered) and ("summarize" in lowered or "summary" in lowered):
            search_tool = next((t for t in self.tools if t.name == "search"), None)
            summarizer_tool = next((t for t in self.tools if t.name == "summarizer"), None)
            if search_tool and summarizer_tool:
                return [search_tool, summarizer_tool]

        # 2) Naive tool triggers
        tools = self.choose_tools(user_input)

        # 3) Override: definition + question → search
        if tools:
            if (len(tools) == 1 
                and tools[0].name == "define"
                and user_input.strip().endswith("?")):

                search_tool = next((t for t in self.tools if t.name == "search"), None)
                if search_tool:
                    return [search_tool]

            return tools

        # 4) Fallback: question → search
        if user_input.strip().endswith("?"):
            search_tool = next((t for t in self.tools if t.name == "search"), None)
            if search_tool:
                return [search_tool]

        # 5) Summarize-on-request
        if "summarize" in lowered or "summary" in lowered:
            summarizer_tool = next((t for t in self.tools if t.name == "summarizer"), None)
            if summarizer_tool:
                return [summarizer_tool]

        # 6) No tools
        return []

    
    def needs_clarification(self, user_input: str) -> bool:
        """
        Decide if the input is too vague and needs a clarifying question.
        """
        lowered = user_input.lower().strip()

        # Very short or generic commands
        if lowered in ["tell me more", "explain", "help", "look this up", "research this", "what about this"]:
            return True

        # Very short messages with no clear subject
        if len(lowered.split()) <= 3 and any(
            phrase in lowered for phrase in ["this", "that", "it", "thing"]
        ):
            return True

        return False

    def clarifying_question(self, user_input: str) -> str:
        return (
            "I’m not sure what you’d like me to focus on.\n"
            "Can you clarify what topic, question, or goal you have in mind?"
        )


    def detect_multi_step_task(self, user_input: str):
        """
        Detects whether the user is describing a multi-step task.
        Returns a list of detected steps if found, otherwise None.
        """
        lowered = user_input.lower()

        # --- Pattern A: Sequential connectors ---
        sequential_markers = ["first", "next", "then", "after that", "finally"]
        seq_hits = [m for m in sequential_markers if m in lowered]
        if len(seq_hits) >= 2:
            return ["multi-step detected via sequential markers"]

        # --- Pattern B: Multiple verbs in sequence ---
        verbs = ["search", "summarize", "compare", "define", "extract",
                "analyze", "synthesize", "evaluate", "look up", "find"]
        verb_hits = [v for v in verbs if v in lowered]
        if len(verb_hits) >= 3:
            return ["multi-step detected via verb chain"]

        # --- Pattern C: Numbered steps ---
        import re
        numbered_steps = re.findall(r"\b\d+\.", user_input)
        if len(numbered_steps) >= 2:
            return ["multi-step detected via numbered steps"]

        # --- Pattern D: Multi-clause instructions ---
        clauses = [c.strip() for c in re.split(r",|;|and then|followed by", lowered)]
        clause_verbs = sum(any(v in c for v in verbs) for c in clauses)
        if clause_verbs >= 2:
            return ["multi-step detected via multi-clause instruction"]

        # --- Pattern E: Multi-stage research tasks ---
        research_verbs = ["search", "find", "gather", "look up"]
        analysis_verbs = ["analyze", "evaluate", "extract"]
        synthesis_verbs = ["summarize", "compare", "conclude"]

        if (any(v in lowered for v in research_verbs)
            and any(v in lowered for v in analysis_verbs)
            and any(v in lowered for v in synthesis_verbs)):
            return ["multi-step detected via multi-stage research pattern"]

        return None


    def extract_steps(self, user_input: str):
        """
        Extracts ordered steps from a multi-step instruction.
        Returns a list of step strings.
        """
        lowered = user_input.lower()
        steps = []

        import re

        # --- Pattern 1: Numbered steps ---
        numbered = re.findall(r"\d+\.\s*([^0-9]+)", user_input)
        if len(numbered) >= 2:
            return [step.strip() for step in numbered]

        # --- Pattern 2: Sequential connectors ---
        connectors = ["first", "next", "then", "after that", "finally"]
        pattern = r"(first|next|then|after that|finally)"
        parts = re.split(pattern, lowered)

        if len(parts) > 1:
            # Reconstruct steps by pairing connector + text
            for i in range(1, len(parts), 2):
                connector = parts[i]
                text = parts[i+1].strip()
                steps.append(f"{connector} {text}")
            return steps

        # --- Pattern 3: Verb-anchored clauses ---
        verbs = ["search", "summarize", "compare", "define", "extract",
                "analyze", "synthesize", "evaluate", "look up", "find"]

        clauses = re.split(r",|;|and then|followed by", lowered)
        for clause in clauses:
            clause = clause.strip()
            if any(v in clause for v in verbs):
                steps.append(clause)

        if len(steps) >= 2:
            return steps

        return None

if __name__ == "__main__":
    llm = LLMClient()
    tools = [
        SearchTool(),
        DefinitionTool(),
        SummarizerTool(llm_client=llm)
    ]
    agent = ResearchAgent(tools=tools)
    agent.run()