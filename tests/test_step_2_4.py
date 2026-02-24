# ---------------------------------------------------------
# Step 2.4 Test Harness for ResearchAgent.parse_step()
# ---------------------------------------------------------

from agenticai.agents.research_agent import ResearchAgent

# For Step 2.4, tools are not needed, so we pass an empty list.
agent = ResearchAgent(tools=[])



def run_test(description, text):
    print("\n" + "="*80)
    print(f"TEST: {description}")
    print("-"*80)
    print(f"Input: {text}")

    # Extract raw steps
    steps = agent.extract_steps(text)
    print(f"\nExtracted steps:")
    for s in steps:
        print(f"  - {s}")

    # Parse each step
    parsed = [agent.parse_step(s) for s in steps]
    print("\nParsed steps:")
    for p in parsed:
        print(f"  {p}")


# ---------------------------------------------------------
# Test Suite
# ---------------------------------------------------------

# 1. Trailing punctuation cleanup
run_test(
    "Trailing punctuation cleanup",
    "Investigate quantum computing, then outline its main challenges."
)

# 2. Compare cleanup
run_test(
    "Compare cleanup",
    "To begin, compare GPT‑4 and Gemini, afterwards summarize the differences."
)

# 3. Multi-word verb detection
run_test(
    "Multi-word verb detection",
    "Look into neural networks, then highlight the key ideas."
)

# 4. Mid-clause verb detection
run_test(
    "Mid-clause verb detection",
    "In the end, outline the major findings."
)

# 5. Mid-clause verb + punctuation
run_test(
    "Mid-clause verb + punctuation",
    "Eventually, summarize the results."
)

# 6. Compare with punctuation
run_test(
    "Compare with punctuation",
    "Compare apples and oranges."
)

# 7. No trailing punctuation
run_test(
    "No trailing punctuation",
    "Analyze the dataset."
)

# 8. Noun phrase (should not split)
run_test(
    "Noun phrase only",
    "AI and machine learning"
)

print("\nAll Step 2.4 tests executed.\n")
