from dataclasses import dataclass
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext

from agentic_ai_kata.settings import KataSettings
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

    def to_string(self) -> str:
        """Returns a flattened string representation of the question, answer and context"""
        context_str = "\n".join(f"  {ctx}" for ctx in self.context)
        return (
            f'<QuestionAnswerWithContext question="{self.question}" '
            f'answer="{self.answer}" '
            f"context=[\n{context_str}\n]>"
        )


class WikiSearchAgent:
    """
    A simple agent that uses a ColBERTv2 retriever to search wikipedia for context.
    """

    def __init__(self):
        self.settings = KataSettings.get_settings()
        self.retriever = ColBERTv2(url="http://20.102.90.50:2017/wiki17_abstracts")
        self.openai = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    def _create_agent(self) -> Agent:
        """Creates the augmented agent with tools"""
        agent = Agent(
            "openai:gpt-4o",
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

    async def run(self, question: str) -> QuestionAnswerWithContext:
        """Run the agent to answer a question with wikipedia context.

        Args:
            question: The question to answer.

        Returns:
            QuestionAnswerWithContext: The answer with context.
        """
        result = await self.agent.run(question, deps=self.deps)
        return result
