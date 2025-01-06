import pytest
from agentic_ai_kata.kata_03_routing import RoutingKata


# def test_routing_kata_initialization():
#     # Given: A new kata instance
#     kata = RoutingKata()

#     # Then: It should have a valid API key
#     # assert kata.settings.OPENAI_API_KEY is not None


@pytest.mark.vcr()
def test_routing_kata_run():
    # Given: A configured kata instance
    kata = RoutingKata()

    # When: We run the kata
    result = kata.run()

    # Then: We should get a valid routing result
    assert kata.validate_result(result)
