import pytest
from agentic_ai_kata.kata_03_routing import RoutingKata, RoutingResult, Route


def test_routing_kata_initialization():
    # Given: A new kata instance
    kata = RoutingKata()

    # Then: It should have a valid API key
    assert kata.settings.OPENAI_API_KEY is not None


def test_routing_kata_run():
    # Given: A configured kata instance
    kata = RoutingKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid routing result
    assert result.data is not None
    assert isinstance(result.data, RoutingResult)
    assert result.data.input is not None
    assert result.data.response is not None
    assert isinstance(result.data.route, Route)
    assert result.data.route.category is not None
    assert 0 <= result.data.route.confidence <= 1
    assert result.data.route.handler is not None

    # Display the routing decision
    print(f"\nInput: {result.data.input}")
    print(
        f"Category: {result.data.route.category} (confidence: {result.data.route.confidence:.2f})"
    )
    print(f"Handler: {result.data.route.handler}")
    print(f"Response: {result.data.response}")
