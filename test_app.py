import pytest
import asyncio
import aiohttp
import allure
import app


@pytest.fixture
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def mock_response():
    return {
        "status": "success",
        "message": "Mock message"
    }


@pytest.mark.asyncio
@allure.title("Test get_json with valid URL")
@allure.description("Test the get_json function with a valid URL")
def test_get_json_valid_url(event_loop, mock_response):
    valid_url = "https://dog.ceo/api/breeds/list/all"

    async def mock_get(url):
        return mock_response

    app.aiohttp.ClientSession.get = mock_get

    result = event_loop.run_until_complete(app.get_json(valid_url))

    assert result == mock_response


@pytest.mark.asyncio
@allure.title("Test get_json with invalid URL")
@allure.description("Test the get_json function with an invalid URL")
def test_get_json_invalid_url(event_loop):
    invalid_url = "https://example.com/invalid"

    with pytest.raises(aiohttp.ClientError):
        event_loop.run_until_complete(app.get_json(invalid_url))