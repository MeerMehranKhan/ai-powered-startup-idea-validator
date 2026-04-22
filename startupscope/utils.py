import re
import json

def clean_json_response(raw_text: str) -> str:
    """Removes markdown code blocks if present in LLM response to get raw JSON."""
    text = raw_text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text)
        text = re.sub(r"```$", "", text)
    return text.strip()

def safe_parse_json(text: str) -> dict:
    """Attempts to cleanly parse JSON, throwing ValueError on failure."""
    cleaned = clean_json_response(text)
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")
