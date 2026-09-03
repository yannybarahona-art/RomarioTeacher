from src.pipeline import normalize_city


def test_normalize_city():

    result = normalize_city(" london### ")

    assert result == "London"


def test_normalize_city_caps():

    result = normalize_city("PARIS")

    assert result == "Paris"