from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.pipeline import get_weather, normalize_city


def test_normalize_city():

    result = normalize_city(" london### ")

    assert result == "London"


def test_normalize_city_caps():

    result = normalize_city("PARIS")

    assert result == "Paris"



""" def test_fetch_weather():
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "hourly": {
            "time": ["2023-01-01T00:00", "2023-01-01T01:00"],
            "temperature_2m": [10, 12]
        }
    }
    mock_client = MagicMock()
    mock_client.get.return_value = mock_response
    result=fetch_weather(mock_client, "Paris",40.7128, -74.0060)
    assert result["city"]=="New York"
    assert result["data"]["temperature_2m"][0]==[22.5]

    # Test the get_weather function with valid coordinates
    lat = 40.7128
    lon = -74.0060
    result = get_weather(lat, lon)

    assert "temperature_2m" in result
    assert "time" in result
     """

@pytest.mark.asyncio
@patch("src.pipeline.httpx.Client.get")
async def test_get_weather_async(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "hourly": {
            "time": ["2023-01-01T00:00", "2023-01-01T01:00"],
            "temperature_2m": [10, 12],
            "precipitation": [0.1, 0.2],
        }
    }
    mock_client=AsyncMock()
    mock_client.get.return_value = mock_response
    result=await get_weather_async(mock_client, 40.7128, -74.0060)
    assert result["city"]=="New York"
    assert result["data"]["temperature_2m"][0]==[22.5]

    #mock_get.return_value = mock_response

    lat = 40.7128
    lon = -74.0060
    result = await get_weather(lat, lon)

    assert "hourly" in result
    assert "time" in result["hourly"]
    assert "temperature_2m" in result["hourly"]
    assert "precipitation" in result["hourly"]