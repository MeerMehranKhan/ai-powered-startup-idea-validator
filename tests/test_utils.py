import pytest
from startupscope.utils import clean_json_response, safe_parse_json

def test_clean_json_response():
    raw = "```json\n{\"test\": 123}\n```"
    cleaned = clean_json_response(raw)
    assert cleaned == "{\"test\": 123}"

def test_safe_parse_json_valid():
    raw = "```json\n{\"test\": 123}\n```"
    parsed = safe_parse_json(raw)
    assert parsed["test"] == 123

def test_safe_parse_json_invalid():
    raw = "{\"test\": 123"
    with pytest.raises(ValueError, match="Failed to parse JSON"):
        safe_parse_json(raw)
