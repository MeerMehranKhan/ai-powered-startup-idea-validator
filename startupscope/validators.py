from typing import Dict, Any
from startupscope.constants import INDUSTRIES, BUSINESS_TYPES

def normalize_string(val: str) -> str:
    if not val:
        return ""
    return val.strip()

def validate_startup_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes raw dictionary input before creating a StartupInput model.
    Raises ValueError if required fields are missing or constraints are violated.
    """
    name = normalize_string(data.get("name", ""))
    pitch = normalize_string(data.get("one_line_pitch", ""))
    desc = normalize_string(data.get("description", ""))
    
    if not name:
        raise ValueError("Startup name cannot be empty.")
    if not pitch:
        raise ValueError("One-line pitch cannot be empty.")
    if not desc:
        raise ValueError("Description cannot be empty.")
        
    try:
        budget = float(data.get("budget", 0))
    except ValueError:
        raise ValueError("Budget must be a number.")
        
    if budget < 0:
        raise ValueError("Budget cannot be negative.")
        
    try:
        team_size = int(data.get("team_size", 1))
    except ValueError:
        raise ValueError("Team size must be an integer.")
        
    if team_size < 1:
        raise ValueError("Team size must be at least 1.")
        
    industry = data.get("industry", "Other")
    if industry not in INDUSTRIES:
        industry = "Other"
        
    business_type = data.get("business_type", "B2C (Business to Consumer)")
    if business_type not in BUSINESS_TYPES:
        business_type = "B2C (Business to Consumer)"
        
    data["name"] = name
    data["one_line_pitch"] = pitch
    data["description"] = desc
    data["budget"] = budget
    data["team_size"] = team_size
    data["industry"] = industry
    data["business_type"] = business_type
    
    return data
