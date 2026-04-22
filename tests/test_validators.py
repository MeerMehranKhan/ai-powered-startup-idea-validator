import pytest
from startupscope.validators import validate_startup_input

def test_validate_startup_input_valid():
    raw_data = {
        "name": "Test Startup",
        "one_line_pitch": "A pitch",
        "description": "A detailed description",
        "budget": 5000,
        "team_size": 2,
        "industry": "Software as a Service (SaaS)",
        "business_type": "B2B (Business to Business)"
    }
    result = validate_startup_input(raw_data)
    assert result["name"] == "Test Startup"
    assert result["budget"] == 5000.0
    assert result["team_size"] == 2

def test_validate_startup_input_missing_name():
    raw_data = {
        "one_line_pitch": "A pitch",
        "description": "A detailed description"
    }
    with pytest.raises(ValueError, match="Startup name cannot be empty"):
        validate_startup_input(raw_data)

def test_validate_startup_input_negative_budget():
    raw_data = {
        "name": "Test Startup",
        "one_line_pitch": "A pitch",
        "description": "A detailed description",
        "budget": -100
    }
    with pytest.raises(ValueError, match="Budget cannot be negative"):
        validate_startup_input(raw_data)
