from typing import Any, Optional
import asyncio
from openai import AsyncOpenAI
from dataclasses import dataclass

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.result import RunResult
from pydantic_ai.messages import ToolCallPart

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings
from agentic_ai_kata.utils import ColBERTv2


@dataclass
class Deps:
    openai: AsyncOpenAI


# Define a response model for PydanticAI Agents to use
class QuestionAnswerWithContext(BaseModel):
    """A question, with context, and an answer"""

    question: str = Field(description="The question.")
    answer: str = Field(description="A concise, one sentence answer to the question.")
    context: list[str] = Field(description="A list of context used for the answer.")


class AugmentedResult(BaseModel):
    """Result from an augmented LLM that includes context used"""

    capital_size_result: Optional[RunResult] = Field(
        description="The LLM's response to the capital size question",
        default=None,
    )
    density_result: Optional[RunResult] = Field(
        description="The LLM's response to the density question",
        default=None,
    )


class AugmentedKata(KataBase):
    """
    Kata 01: Augmented LLM Pattern

    This kata demonstrates:
    1. How to augment LLM calls with retrieval
    2. How to integrate tools into LLM responses
    3. How to maintain memory across interactions
    """

    def __init__(self):
        self.retriever = ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Creates the augmented agent with tools"""
        agent = Agent(
            settings.DEFAULT_MODEL,
            deps_type=Deps,
            system_prompt=(
                "You are a helpful assistant that uses tools to augment your knowledge. "
                "Always use the search_wikipedia tool to verify facts before answering. "
                "Be concise and reply with one or two sentences at most."
            ),
            result_type=QuestionAnswerWithContext,
            retries=3,
        )

        @agent.tool
        async def search_wikipedia(context: RunContext[Deps], query: str) -> str:
            """Retrieve wikipedia sections based on a search query.

            Args:
                context: The call context.
                query: The search query.
            """
            results = self.retriever.call_sync(query, k=3)
            # Extract text from each result dictionary
            texts = [result.get("text", "") for result in results]
            return "\n".join(texts)

        return agent

    async def _run_async(self) -> AugmentedResult:
        """Async implementation of the kata run"""

        run_data = AugmentedResult()

        # Ask a question that requires fact checking
        run_data.capital_size_result = await self.agent.run(
            "Does the capital of France have more people than the capital of Germany?",
            deps=self.deps,
        )

        # There is message data in the result.
        # We could save it to a database if we wanted to retreive it later.
        # Instead, we'll just pass it to the next run.
        messages = run_data.capital_size_result.new_messages()

        # Ask a question that requires fact checking and context from the previous run
        run_data.density_result = await self.agent.run(
            "Which is more densely populated?",
            deps=self.deps,
            message_history=messages,  # Here we pass the messages from the previous run
        )

        return run_data

    def run(self) -> Any:
        """Demonstrates the augmented LLM pattern"""
        return asyncio.run(self._run_async())

    def validate_result(self, result: AugmentedResult) -> bool:
        """Validates that the augmented LLM pattern worked correctly"""
        # Check we have a valid result object
        assert result
        assert isinstance(result, AugmentedResult)

        # Validate capital size question
        assert result.capital_size_result is not None
        messages = result.capital_size_result.all_messages()
        assert len(messages) > 0

        # Check for tool usage in first question
        tool_calls = []
        for msg in messages:
            for part in msg.parts:
                if isinstance(part, ToolCallPart):
                    tool_calls.append(part)

        assert len(tool_calls) >= 1, "Should have at least one tool call"

        # Verify search queries were relevant
        search_queries = []
        for call in tool_calls:
            if call.tool_name == "search_wikipedia":
                search_queries.append(call.args)

        assert len(search_queries) >= 2, "Should search at least twice"
        assert any(
            "Paris" in str(query) for query in search_queries
        ), "Should search for Paris"
        assert any(
            "Berlin" in str(query) for query in search_queries
        ), "Should search for Berlin"

        # Validate density question
        assert result.density_result is not None
        assert len(result.density_result.all_messages()) > 0

        # Check for memory usage in final results
        assert result.capital_size_result.data is not None
        assert result.density_result.data is not None

        # Print Q&A pairs for debugging
        print("\nCapital Size Question:")
        print(f"Q: {result.capital_size_result.data.question}")
        print(f"A: {result.capital_size_result.data.answer}")
        print("\nDensity Question:")
        print(f"Q: {result.density_result.data.question}")
        print(f"A: {result.density_result.data.answer}")

        # Verify final answers are complete and use the data
        assert result.capital_size_result.data.answer is not None
        assert result.density_result.data.answer is not None

        # Check for key concepts in answers rather than exact words
        size_answer = result.capital_size_result.data.answer.lower()
        density_answer = result.density_result.data.answer.lower()

        assert any(
            word in size_answer for word in ["population", "million", "inhabitants"]
        ), "Answer should mention population numbers"
        assert any(
            word in density_answer for word in ["densely", "density", "per", "area"]
        ), "Answer should discuss density"

        # Verify conversation coherence through message history
        # The second answer should reference both cities without needing to name them again
        # since they were established in the conversation context
        assert not (
            "which city" in density_answer or "what city" in density_answer
        ), "Answer should maintain conversation context without asking for clarification"
        assert (
            result.density_result.data.answer is not None
            and len(result.density_result.data.answer.strip()) > 0
        ), "Should provide a complete answer to the follow-up question"

        return True
