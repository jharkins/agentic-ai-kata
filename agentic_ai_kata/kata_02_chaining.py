from typing import Any, Optional
import os
import json
from slugify import slugify
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext, capture_run_messages, UnexpectedModelBehavior
import aiohttp
import asyncio
from openai import AsyncOpenAI

from agentic_ai_kata.base import KataBase
from agentic_ai_kata.settings import settings
from agentic_ai_kata.utils.wiki_search_agent import WikiSearchAgent


@dataclass
class Deps:
    openai: AsyncOpenAI


class ChainStep(BaseModel):
    """A single step in a chain of prompts"""

    step_name: str = Field(description="The name of the step")
    prompt: str = Field(description="The prompt for this step")
    response: str = Field(description="The response from the LLM")


class ChainResult(BaseModel):
    """Result from a chain of prompts"""

    steps: list[ChainStep] = Field(description="The steps in the chain")
    final_result: str = Field(description="The final result after all steps")

    def add_step(self, step: ChainStep):
        print(f"Finished Step: {step.step_name}")
        self.steps.append(step)
        self.final_result = step.response


class ChainingKata(KataBase):
    """
    Kata 02: Prompt Chaining Pattern

    This kata demonstrates:
    1. How to decompose tasks into multiple LLM calls
    2. How to chain prompts together with optional gating/checks
    3. How to handle errors and retries in chains
    """

    def __init__(self):
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.deps = Deps(openai=self.openai)
        self.agent = self._create_agent()

    async def _run_async(self) -> Any:
        """Async implementation of the kata run"""
        chain_result = ChainResult(
            steps=[],
            final_result="",
        )

        # Step 0: Generate a fake solar system, planet, and planetary capital
        class FakePlanetAndPlanetaryCapital(BaseModel):
            solar_system: str = Field(description="The name of the solar system")
            planet: str = Field(description="The name of the planet")
            planetary_capital: str = Field(
                description="The name of the planetary capital"
            )
            full_title_of_planetary_capital: str = Field(
                description="The full title of the planetary capital, including all the embellishments and titles given to it."
            )

            def to_string(self) -> str:
                return (
                    f"Solar System: {self.solar_system}\n"
                    f"Planet: {self.planet}\n"
                    f"Planetary Capital: {self.planetary_capital}\n"
                    f"Full Title of Planetary Capital: {self.full_title_of_planetary_capital}\n"
                )

        fake_planet_and_planetary_capital_agent = Agent(
            settings.DEFAULT_MODEL,
            result_type=FakePlanetAndPlanetaryCapital,
            system_prompt=(
                "You are an expert fiction writer, in the style of Rick & Morty."
                "Your task is to generate a fake solar system, planet, and planetary capital."
            ),
        )

        fake_planet_and_planetary_capital_result = (
            await fake_planet_and_planetary_capital_agent.run("Ok, go!")
        )

        chain_result.add_step(
            ChainStep(
                step_name="Fake Planet and Planetary Capital Agent",
                prompt="Ok, go!",
                response=fake_planet_and_planetary_capital_result.data.to_string(),
            )
        )

        # Step 1: Ask a question about a fictional city. Use wikipedia search agent to verify.
        question = (
            f"Tell me about the city of {fake_planet_and_planetary_capital_result.data.planetary_capital}"
            f" on the planet {fake_planet_and_planetary_capital_result.data.planet}"
            f" in the solar system {fake_planet_and_planetary_capital_result.data.solar_system}."
        )

        print(f"Question: {question}")
        search_agent = WikiSearchAgent()
        search_result = await search_agent.run(question)

        chain_result.add_step(
            ChainStep(
                step_name="Search Agent",
                prompt=question,
                response=search_result.data.to_string(),
            )
        )

        # Step 2: Let's chain right now just to interpret the result
        class SearchAndOutlineResult(BaseModel):
            is_real_city: bool = Field(description="Whether the city is real.")
            outline: Optional[list[str]] = Field(
                description="A list of markdown outline sections for a (made up) wiki article of the founding of the city.",
                default=None,
            )

        outline_agent = Agent(
            self.settings.DEFAULT_MODEL,
            result_type=SearchAndOutlineResult,
            deps_type=str,
            system_prompt=(
                "You are an expert fiction writer, in the style of Rick & Morty."
                "You write outlines for wikipedia articles about made up citiies.",
                "You are given an initial question.",
                "You are given a wikipedia search result for a city.",
                "You determine if the city is real or not.",
                "If it's real, you set is_real_city to a funny message."
                "If it's not a real city, write a fictional wikipedia style city outline.",
            ),
        )

        @outline_agent.system_prompt
        def add_the_question_and_search_result(ctx: RunContext[str]) -> str:
            return f"The wikipedia search result was: {ctx.deps}"

        outline_result = await outline_agent.run(
            question, deps=search_result.data.to_string()
        )

        chain_result.add_step(
            ChainStep(
                step_name="Outline Agent",
                prompt=question,
                response="\n".join(outline_result.data.outline),
            )
        )

        # Check the result - in normal circumstances, we'd do something smarter
        # print("\n".join(outline_result.data.outline))
        assert outline_result.data.is_real_city is False

        # Step 3: Generate fake facts about the city
        class MadeUpFacts(BaseModel):
            facts: list[dict[str, str]] = Field(
                description="The (made up) facts about the city and the officially formatted bibliography entry (also made up)"
            )

        @dataclass
        class FakeFactsDeps:
            outline: list[str]

        fake_facts_agent = Agent(
            self.settings.DEFAULT_MODEL,
            result_type=MadeUpFacts,
            deps_type=FakeFactsDeps,
            retries=3,  # Increase retries to handle potential tool call issues
            system_prompt=(
                "You are an expert fiction writer, in the style of Rick & Morty. "
                "You are given an outline for a wikipedia article about a made up city. "
                "Your task is to generate a list of 'facts' about the city. They are all made up. "
                "Each fact is a dictionary with the fact and a bibliography entry. "
                "It's all made up, the facts aren't real. "
                "Return the facts directly in the response, do not use any tools."
            ),
        )

        @fake_facts_agent.system_prompt
        def add_outline_context(ctx: RunContext[FakeFactsDeps]) -> str:
            return f"The article outline is:\n{ctx.deps.outline}"

        with capture_run_messages() as messages:
            try:
                fake_facts_result = await fake_facts_agent.run(
                    "Please generate 3-5 made up facts about this city. "
                    "Each fact should be a dictionary with 'fact' and 'bibliography' keys.",
                    deps=FakeFactsDeps(outline=outline_result.data.outline),
                )
            except UnexpectedModelBehavior as e:
                print("Fake Facts Agent Error:", e)
                print("Cause:", repr(e.__cause__))
                print("Messages:", messages)
                # Retry with more explicit prompt
                fake_facts_result = await fake_facts_agent.run(
                    "Please generate 3-5 made up facts about this city. "
                    "Each fact should be a dictionary with 'fact' and 'bibliography' keys. "
                    "Return the facts directly in your response, do not use any tools.",
                    deps=FakeFactsDeps(outline=outline_result.data.outline),
                )

        chain_result.add_step(
            ChainStep(
                step_name="Fake Facts Agent",
                prompt=f"The article outline for the city is: {outline_result.data.outline}",
                response=f"facts: {fake_facts_result.data.facts}",
            )
        )

        # print(fake_facts_result.data)

        # Step 4: Write a wikipedia style article about the city
        @dataclass
        class ArticleWriterDeps:
            full_city_name: str
            outline: list[str]
            facts: list[dict[str, str]]

        class ArticleWriterResult(BaseModel):
            article: str = Field(
                description="The wikipedia style article about the city."
            )

        article_writer_agent = Agent(
            self.settings.DEFAULT_MODEL,
            result_type=ArticleWriterResult,
            system_prompt=(
                "You are an expert fiction writer, in the style of Rick & Morty."
                "You also write the best wikipedia style articles."
                "You are given an outline and facts about a city."
                "You write a wikipedia style article about the city."
                "You care that the entire article is completely up to snuff for a wikipedia page."
                "You turn the facts into bibiliography entires."
            ),
        )

        @article_writer_agent.system_prompt
        def add_the_outline_and_facts(ctx: RunContext[ArticleWriterDeps]) -> str:
            outline = "\n".join(ctx.deps.outline)
            facts = json.dumps(ctx.deps.facts)
            return f"The outline for the city is: {outline}\nThe facts about the city are: {facts}"

        article_writer_result = await article_writer_agent.run(
            f"Please write a wikipedia style article about the city of {fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital}.",
            deps=ArticleWriterDeps(
                full_city_name=fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital,
                outline=outline_result.data.outline,
                facts=fake_facts_result.data.facts,
            ),
        )

        chain_result.add_step(
            ChainStep(
                step_name="Article Writer Agent",
                prompt=f"Please write a wikipedia style article about the city of {fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital}.",
                response=article_writer_result.data.article,
            )
        )

        # Step 5: Format the article into a wikipedia style article
        @dataclass
        class WikipediaFormatterDeps:
            article_draft: str
            outline: list[str]
            facts: list[dict[str, str]]

        class WikipediaFormatterResult(BaseModel):
            article: str = Field(
                description="The fully formatted wikipedia article about the city, including citations, that fully conforms (as applicable) to the wikipedia template."
            )
            highlight: str = Field(description="A short highlight of the article.")

        wikipedia_formatter = Agent(
            self.settings.DEFAULT_MODEL,
            result_type=WikipediaFormatterResult,
            system_prompt=(
                "You are an expert wikipedia formatter."
                "Your output is a markdown formatted wikipedia article."
                "You are given: a draft article about a city, an outline for the article, and a list of facts about the city."
                "You have a tool, get_template_defintion, that returns the wikipedia template for a city."
            ),
        )

        # A tool that async gets a URL and returns the contents
        @wikipedia_formatter.tool_plain
        async def get_template_definition() -> str:
            """Get the template definition for a wikipedia article about a city."""
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://r.jina.ai/https://en.wikipedia.org/wiki/Template:Article_templates/City"
                ) as response:
                    return await response.text()

        wikipedia_formatter_result = await wikipedia_formatter.run(
            f"Please format the article about the city of {fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital} into a wikipedia style article.",
            deps=WikipediaFormatterDeps(
                article_draft=article_writer_result.data.article,
                outline=outline_result.data.outline,
                facts=fake_facts_result.data.facts,
            ),
        )

        chain_result.add_step(
            ChainStep(
                step_name="Wikipedia Formatter Agent",
                prompt=f"Please format the article about the city of {fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital} into a wikipedia style article.",
                response=wikipedia_formatter_result.data.article,
            )
        )

        # Write the article to a file
        # Make a folder in the current directory called "articles"
        os.makedirs("articles", exist_ok=True)

        # Write the article to a file in the folder
        article_slug = slugify(
            fake_planet_and_planetary_capital_result.data.full_title_of_planetary_capital
        )
        with open(f"articles/{article_slug}.md", "w") as f:
            f.write(wikipedia_formatter_result.data.article)

        print(f"Article written to articles/{article_slug}.md")
        print(f"Highlight: {wikipedia_formatter_result.data.highlight}")

        return chain_result

    def run(self) -> Any:
        """Demonstrates the prompt chaining pattern"""
        return asyncio.run(self._run_async())

    def validate_result(self, result: ChainResult) -> bool:
        """Validates that the chaining pattern worked correctly"""
        # Check we have a valid result object
        assert result is not None
        assert isinstance(result, ChainResult)
        assert result.steps is not None

        # Print chain execution for visibility
        print("\n🔗 Chain Execution Summary:")
        print("=" * 30)
        for step in result.steps:
            print(f"\nStep: {step.step_name}")
            print(f"Prompt: {step.prompt[:100]}...")
            print(f"Response: {step.response[:100]}...")

        # 1. Verify task decomposition into sequential steps
        assert len(result.steps) >= 4, "Should have at least 4 steps in the chain"
        step_names = [step.step_name for step in result.steps]
        assert "Search Agent" in step_names, "Should start with search"
        assert "Outline Agent" in step_names, "Should generate outline"
        assert "Fake Facts Agent" in step_names, "Should generate facts"
        assert "Article Writer Agent" in step_names, "Should write article"

        # 2. Verify correct sequence
        step_order = {name: i for i, name in enumerate(step_names)}
        assert (
            step_order["Search Agent"] < step_order["Outline Agent"]
        ), "Search should come before outline"
        assert (
            step_order["Outline Agent"] < step_order["Fake Facts Agent"]
        ), "Outline should come before facts"
        assert (
            step_order["Fake Facts Agent"] < step_order["Article Writer Agent"]
        ), "Facts should come before article"

        # 3. Verify each step produces meaningful output
        for step in result.steps:
            assert (
                step.response and len(step.response.strip()) > 0
            ), f"Step {step.step_name} should have output"
            assert (
                len(step.response) > 50
            ), f"Step {step.step_name} output seems too short"

            # Content-specific checks
            if step.step_name == "Search Agent":
                # The response should be a QuestionAnswerWithContext string representation
                assert (
                    'question="' in step.response
                ), "Search response should include question"
                assert (
                    'answer="' in step.response
                ), "Search response should include answer"
                assert (
                    "context=[" in step.response
                ), "Search response should include context"
            elif step.step_name == "Outline Agent":
                assert any(
                    marker in step.response.lower() for marker in ["#", "*", "-"]
                ), "Outline should have markdown-style formatting"
            elif step.step_name == "Fake Facts Agent":
                # assert (
                #     "full_city_name" in step.response
                # ), "Facts should include city name"
                assert "facts" in step.response, "Should include facts list"
            elif step.step_name == "Article Writer Agent":
                assert any(
                    marker in step.response for marker in ["==", "#"]
                ), "Article should have section markers"

        # 4. Verify final result
        assert (
            result.final_result and len(result.final_result) > 0
        ), "Should have final result"
        assert any(
            marker in result.final_result for marker in ["==", "#"]
        ), "Final result should be formatted article"

        return True
