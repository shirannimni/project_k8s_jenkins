import pytest
from app import get_background_color

def test_background_color():
    assert get_background_color() == "blue", "Background color is not blue"
