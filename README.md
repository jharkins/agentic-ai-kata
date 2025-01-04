# agentic-ai-kata

> In the garden of code, the AI monk Sudo Matsumoto sat in contemplation. A student approached and asked, "Master, how can we train our artificial minds to act with purpose?" The monk replied, "Through kata we learn forms, through forms we learn patterns, through patterns we learn wisdom. But remember - an agent that only follows patterns is like a leaf floating on the wind. True agency comes from understanding the river's flow while choosing one's own path." The student was enlightened.

---

A collection of Python katas illustrating how to build and reason about effective LLM-based agents. Each kata (after the first initial “setup” kata) showcases a pattern from [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.

## Table of Contents

- [Introduction](#introduction)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Patterns Covered](#patterns-covered)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

“Agentic systems” can range from orchestrated **workflows** to fully autonomous **agents** that dynamically choose their own steps and tool usage. The article [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) lays out patterns for composing LLMs effectively without unnecessary complexity.

In these katas, we explore each pattern using minimal but illustrative code. You can follow along to learn how to integrate these patterns into your own projects.

## Repository Structure

```plaintext
agentic-ai-kata/
├── agentic_ai_kata/
│   ├── __init__.py
│   ├── kata_00_setup.py
│   ├── kata_01_augmented_llm.py
│   ├── kata_02_prompt_chaining.py
│   ├── kata_03_routing.py
│   ├── kata_04_parallelization.py
│   ├── kata_05_orchestrator_workers.py
│   ├── kata_06_evaluator_optimizer.py
│   ├── kata_07_agent.py
│   └── ...
├── tests/
│   ├── test_kata_00_setup.py
│   ├── test_kata_01_augmented_llm.py
│   ├── test_kata_02_prompt_chaining.py
│   └── ...
├── .env.example
├── pyproject.toml  (or setup.py)
├── README.md
└── LICENSE
```

**Key Folders & Files**:

- **`agentic_ai_kata/`**: Where all katas and related modules live.
  - Each kata is a standalone Python file showcasing a particular agentic pattern.
- **`tests/`**: Unit tests for each kata, typically one test file per kata.
- **`.env.example`**: Template showing how to store secrets (e.g., OpenAI API key).
- **`pyproject.toml`** _(or `setup.py`)_: Handles packaging and dependencies.

## Installation

1. **Clone this repo**:

   ```bash
   git clone https://github.com/your-username/agentic-ai-kata.git
   cd agentic-ai-kata
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Linux/Mac
   # or:
   venv\Scripts\activate     # On Windows
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   > Alternatively, if using Poetry or a similar tool, run:
   >
   > ```bash
   > poetry install
   > ```

## Environment Variables

We use [Pydantic Settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) to handle configuration, including your OpenAI (or other LLM) API keys. The `.env.example` file serves as a template:

```plaintext
OPENAI_API_KEY=your_openai_key_goes_here
```

1. Duplicate `.env.example` and rename it to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your actual API key(s).

When you run any kata (or the entire package), the code automatically picks up environment variables through Pydantic.

## Usage

Each **kata** is self-contained, with documentation and minimal example usage. You can run them individually or explore them interactively:

```bash
# Example: run kata_02_prompt_chaining
python -m agentic_ai_kata.kata_02_prompt_chaining
```

You can also run **all tests** to see the katas in action:

```bash
pytest
```

Or, if you have [pytest-watch](https://pypi.org/project/pytest-watch/):

```bash
ptw
```

## Patterns Covered

Each kata focuses on a pattern from [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents):

1. **Kata 00: Setup**

   - Basic environment setup, confirming your key is accessible.

2. **Kata 01: Augmented LLM**

   - Integrates retrieval, tools, or memory into basic LLM calls.

3. **Kata 02: Prompt Chaining**

   - Decomposes tasks into multiple LLM calls with optional gating or checks.

4. **Kata 03: Routing**

   - Classifies inputs and directs them to specialized prompts or tools.

5. **Kata 04: Parallelization**

   - Shows how to split tasks into parallel calls or use voting to improve accuracy.

6. **Kata 05: Orchestrator-Workers**

   - Demonstrates a central orchestrator LLM that delegates subtasks to workers.

7. **Kata 06: Evaluator-Optimizer**

   - Involves iterative loops where one LLM generates output and another critiques it.

8. **Kata 07: Agent**
   - Implements a simple autonomous agent that can plan, act, and use tools in a loop.

Each kata includes docstrings, comments, and references back to Anthropic’s article for further reading and context.

## Contributing

Contributions are welcome! Here’s how you can help:

1. **Fork** the repository.
2. **Create a new branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes** (add new kata, improve tests, etc.).
4. **Run tests** to ensure everything passes:
   ```bash
   pytest
   ```
5. **Commit** and **push** to your fork:
   ```bash
   git push origin feature/my-new-feature
   ```
6. **Open a Pull Request** describing the changes.

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to adapt the code for your own purposes. We appreciate attribution if you build upon it!

---

Enjoy exploring these katas and applying the **agentic** patterns in your own LLM projects!  
If you have any questions, suggestions, or feedback, please [open an issue](https://github.com/your-username/agentic-ai-kata/issues) or create a pull request.
