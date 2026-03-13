# AgenticAI-App

AgenticAI-App is the application layer built on top of the AgenticAI framework. While the framework provides deterministic planning, workflow execution, tool orchestration, and core abstractions, this repository demonstrates how to assemble those components into a runnable command-line application.

The app exposes a simple CLI that sends user queries through the deterministic Phase 2 pipeline:

1. **PlanningAgent** generates a structured multi-step plan.  
2. **WorkflowAgent** executes the plan step-by-step.  
3. **Tools** are invoked deterministically when required.  
4. **Final results** are synthesized and returned to the user.

This repository also includes a clean Phase 2 test suite (unit + integration) that validates the deterministic pipeline end-to-end.

---

## Purpose of This Repository

- Provide a runnable example of how to use the AgenticAI framework  
- Demonstrate how to assemble the deterministic planning → workflow pipeline into an application  
- Serve as a testing ground for deterministic workflows, tool execution, and multi-step reasoning  
- Offer a clean starting point for building more advanced agentic applications  

This repository depends on the AgenticAI framework, which must be installed separately.

---

## Architecture Overview

The application layer uses the following deterministic pipeline:

```
User Input
   ↓
PlanningAgent
   ↓
Structured Plan (steps with actions, targets, and optional tools)
   ↓
WorkflowAgent
   ↓
Deterministic step-by-step execution
   ↓
Tool calls (if required)
   ↓
Final synthesized output
```

This pipeline ensures:

- No hidden reasoning  
- No unpredictable branching  
- Fully inspectable intermediate steps  
- Deterministic execution for testing and reproducibility  

---

## Project Structure

```
src/
    agenticai_app/
        main.py            – CLI entry point for running the deterministic pipeline
        __init__.py        – Package initializer

    cli/                   – Placeholder for future CLI commands
    configs/               – Placeholder for configuration files
    workflows/             – Placeholder for workflow definitions

tests/
    unit/                  – Unit tests for CLI and app-level components
    integration/           – Integration tests for deterministic planning → workflow execution

docs/
    Notes.txt              – Personal notes (ignored by Git)

pyproject.toml             – Package metadata
requirements.txt           – Python dependencies
README.md                  – This file
.gitignore                 – Ignore rules
```

---

## Installation

Before running the app, install the AgenticAI framework. If you have cloned the framework repository locally, install it in editable mode:

```bash
pip install -e ../AgenticAI
```

Or install directly from GitHub once the framework is published:

```bash
pip install git+https://github.com/YOUR_USERNAME/AgenticAI.git
```

Then install the app dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

To start the deterministic CLI:

```bash
python -m agenticai_app.main
```

You will see:

```
AgenticAI deterministic CLI ready. Type 'exit' to quit.
```

You can then type natural language queries, and the app will:

1. Generate a deterministic plan  
2. Execute each step  
3. Call tools if needed  
4. Produce a final synthesized answer  

---

## Example Interaction

```
You: summarize the history of quantum computing

Plan:
1. action=research, target=history of quantum computing, tool=SearchTool
2. action=summarize, target=research results, tool=SummarizerTool

Execution:
[SearchTool] Quantum computing began...
[SummarizerTool] Summary: ...

Final:
Quantum computing emerged from...
```

---

## Running Tests

This repository includes a Phase 2 test suite that validates:

### Unit tests
- CLI behavior  
- Input handling  
- Output formatting  

### Integration tests
- Deterministic planning  
- Step execution  
- Tool invocation  
- Final synthesis  

To run all tests:

```bash
pytest
```

---

## Design Philosophy

The app follows the same principles as the AgenticAI framework:

### 1. Simplicity  
The application should be easy to run and modify.

### 2. Modularity  
CLI, workflows, and configuration are separated cleanly.

### 3. Extensibility  
New workflows, tools, and agents can be added without modifying core logic.

### 4. Determinism  
All reasoning and execution paths are explicit and testable.

### 5. Transparency  
The app exposes intermediate reasoning steps when appropriate.

---

## Roadmap

### Phase 2 (Completed)
- Deterministic CLI  
- Deterministic planning → workflow pipeline  
- New unit + integration test suite  
- Removal of Phase 1 workflow tests  
- Clean repo structure  

### Phase 3 (Next)
- Multi-agent orchestration demos  
- Advanced workflow execution examples  
- Logging and tracing utilities  

### Future Iterations
- GUI or web-based interface  
- Plugin system for custom workflows  
- Deployment templates  

---

## License

This project is licensed under the MIT License.
```