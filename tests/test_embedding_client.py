
import pytest
import respx
import httpx
from search_api.clients.embedding_client import get_embedding_litellm, LITELLM_HOST, LITELLM_MODEL


@pytest.mark.asyncio
@respx.mock
async def test_get_embedding_litellm_success():
    # Arrange: mock LiteLLM response
    url = f"{LITELLM_HOST}/embeddings"
    expected_embedding = [0.1, 0.2, 0.3, 0.4]
    mock_response = {
        "data": [
            {"embedding": expected_embedding}
        ]
    }

    route = respx.post(url).mock(return_value=httpx.Response(200, json=mock_response))

    # Act
    embedding = await get_embedding_litellm("test input")

    # Assert
    assert route.called
    assert embedding == expected_embedding

@pytest.mark.asyncio
@respx.mock
async def test_get_embedding_litellm_failure():
    # Arrange: mock LiteLLM failure response
    url = f"{LITELLM_HOST}/embeddings"

    route = respx.post(url).mock(return_value=httpx.Response(500))

    # Act & Assert
    with pytest.raises(httpx.HTTPStatusError):
        await get_embedding_litellm("test input")
