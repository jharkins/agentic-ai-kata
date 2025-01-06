# agentic-ai-kata

> In the garden of code, the AI monk Sudo Matsumoto sat in contemplation. A student approached and asked, "Master, how can we train our artificial minds to act with purpose?" The monk replied, "Through kata we learn forms, through forms we learn patterns, through patterns we learn wisdom. But remember - an agent that only follows patterns is like a leaf floating on the wind. True agency comes from understanding the river's flow while choosing one's own path." The student was enlightened.

---

A collection of Python katas illustrating how to build and reason about effective LLM-based agents. Each kata showcases a pattern from [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.

## Table of Contents

- [Introduction](#introduction)
- [Katas](#katas)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Environment Variables](#environment-variables)
- [Cache Initialization](#cache-initialization)
- [Testing and VCR](#testing-and-vcr)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

"Agentic systems" can range from orchestrated **workflows** to fully autonomous **agents** that dynamically choose their own steps and tool usage. The article [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) lays out patterns for composing LLMs effectively without unnecessary complexity.

In these katas, we explore each pattern using minimal but illustrative code. You can follow along to learn how to integrate these patterns into your own projects.

## Katas

1. **Kata 00: Setup** ([`kata_00_setup.py`](agentic_ai_kata/kata_00_setup.py) | [test](tests/test_kata_00_setup.py))

   - Basic environment setup
   - API key verification
   - LLM communication test

2. **Kata 01: Augmented LLM** ([`kata_01_augmented.py`](agentic_ai_kata/kata_01_augmented.py) | [test](tests/test_kata_01_augmented.py))

   - Integrates retrieval and tools
   - Maintains memory across interactions
   - Demonstrates context augmentation

3. **Kata 02: Prompt Chaining** ([`kata_02_chaining.py`](agentic_ai_kata/kata_02_chaining.py) | [test](tests/test_kata_02_chaining.py))

   - Decomposes tasks into steps
   - Implements checks and gates
   - Handles errors and retries

4. **Kata 03: Routing** ([`kata_03_routing.py`](agentic_ai_kata/kata_03_routing.py) | [test](tests/test_kata_03_routing.py))

   - Classifies inputs
   - Routes to specialized handlers
   - Manages uncertainty

5. **Kata 04: Parallelization** ([`kata_04_parallel.py`](agentic_ai_kata/kata_04_parallel.py) | [test](tests/test_kata_04_parallel.py))

   - Runs parallel LLM calls
   - Implements voting mechanisms
   - Aggregates results

6. **Kata 05: Orchestrator-Workers** ([`kata_05_orchestrator.py`](agentic_ai_kata/kata_05_orchestrator.py) | [test](tests/test_kata_05_orchestrator.py))

   - Delegates tasks to workers
   - Manages dependencies
   - Handles failures

7. **Kata 06: Evaluator-Optimizer** ([`kata_06_evaluator.py`](agentic_ai_kata/kata_06_evaluator.py) | [test](tests/test_kata_06_evaluator.py))

   - Evaluates LLM outputs
   - Iteratively improves results
   - Determines stopping conditions

8. **Kata 07: Full Agent** ([`kata_07_agent.py`](agentic_ai_kata/kata_07_agent.py) | [test](tests/test_kata_07_agent.py))
   - Implements autonomous behavior
   - Uses tools effectively
   - Maintains goal-directed behavior

## Repository Structure

```plaintext
.
├── agentic_ai_kata/           # Main package directory
│   ├── base.py               # Base classes and interfaces
│   ├── settings.py           # Configuration and settings
│   ├── kata_*.py            # Individual kata implementations
│   └── utils/               # Utility modules
│       ├── colbert_v2.py    # ColBERT retrieval
│       ├── routing.py       # Message routing
│       ├── text_message.py  # Example conversations
│       └── wiki_search_agent.py  # Wikipedia search
├── articles/                # Generated wiki-style articles
├── conversations/          # Cached example conversations
│   ├── casual_banter.json
│   ├── email_me_a_thing.json
│   ├── new_phone_who_dis.json
│   └── sea_shanty_lookup.json
├── tests/                  # Test suite
│   ├── cassettes/         # VCR.py recorded API responses
│   └── test_kata_*.py     # Individual kata tests
├── poetry.lock            # Poetry dependency lock file
├── pyproject.toml         # Project configuration
└── requirements.txt       # Direct dependencies
```

## Installation

1. **Clone this repo**:

   ```bash
   git clone https://github.com/your-username/agentic-ai-kata.git
   cd agentic-ai-kata
   ```

2. **Install Poetry** (if you haven't already):

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Install dependencies**:

   ```bash
   poetry install
   ```

4. **Activate the virtual environment**:

   ```bash
   poetry shell
   ```

Poetry will automatically create and manage a virtual environment for you, ensuring all dependencies are properly isolated.

## Environment Variables

We use [Pydantic Settings](https://docs.pydantic.dev/latest/usage/pydantic_settings/) to handle configuration. Create a `.env` file with your API keys:

```plaintext
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here  # Optional
```

## Cache Initialization

Some katas use example conversations that are generated using LLMs. To avoid regenerating these conversations every time, we use a caching system. Initialize the conversations by running:

```bash
python -m agentic_ai_kata.utils.text_message
```

This will:

1. Create a `conversations` directory in your project root
2. Generate example conversations using the LLM
3. Save them as JSON files for future use

The generated conversations include:

- Casual banter between friends
- "New phone, who dis?" between knights
- A Monty Python-style email request
- A sea shanty about a made-up disease

The katas will automatically use these saved conversations when needed. If a conversation isn't in the directory, it will be generated on demand.

## Testing and VCR

The tests use [VCR.py](https://vcrpy.readthedocs.io/) to record and replay API interactions. This:

- Makes tests faster and more reliable
- Reduces API costs during development
- Documents expected API behavior
- Works offline once cassettes are recorded

The cassettes are stored in `tests/cassettes/` and are committed to the repository. They contain:

- API request/response pairs
- Sanitized data (API keys replaced with "DUMMY")
- Expected model outputs

### Working with Cassettes

To regenerate cassettes (e.g., after changing tests or updating model behavior):

```bash
# Remove existing cassettes
rm -rf tests/cassettes

# Run tests to generate new cassettes
poetry run pytest -v
```

When running tests:

1. First run: Records real API calls to cassettes
2. Subsequent runs: Uses recorded cassettes
3. CI/CD: Uses committed cassettes (no API keys needed)

Note: Cassettes are automatically sanitized to remove sensitive data like API keys.

## Usage

Each kata is self-contained and demonstrates a specific pattern. The tests use a Given-When-Then pattern and include koans that illustrate the concepts:

```python
def test_kata_run():
    # Given: A configured kata instance
    kata = SomeKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get the expected result
    assert result.is_valid()
```

Run the tests to see the katas in action:

```bash
# Run all tests
poetry run pytest -v

# Stop on first failure (useful during development)
poetry run pytest -v -x

# Show print output
poetry run pytest -v -s

# Run specific kata tests
poetry run pytest -v -k "test_kata_01"
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add or improve katas
4. Ensure tests pass (`poetry run pytest`)
5. Submit a pull request

## License

This project is licensed under the [MIT License](LICENSE).

Feel free to adapt the code for your own projects. We appreciate attribution if you build upon it!
