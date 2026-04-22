import json
from openai import OpenAI
from anthropic import Anthropic
from startupscope.config import Config
from startupscope.logger import logger
from startupscope.models import StartupInput, ValidationReport
from startupscope.prompts import SYSTEM_PROMPT, build_analysis_prompt
from startupscope.utils import safe_parse_json
from startupscope.exceptions import PromptParsingError
from startupscope.scoring import generate_fallback_report

def call_openai(prompt: str) -> dict:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        response_format={"type": "json_object"}
    )
    return safe_parse_json(response.choices[0].message.content)

def call_anthropic(prompt: str) -> dict:
    client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    response = client.messages.create(
        model=Config.ANTHROPIC_MODEL,
        max_tokens=4000,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return safe_parse_json(response.content[0].text)

def run_analysis_with_retries(startup: StartupInput, max_retries: int = 2) -> dict:
    prompt = build_analysis_prompt(startup.model_dump())
    mode = Config.get_analysis_mode()
    
    for attempt in range(max_retries):
        try:
            if mode == "OpenAI Analysis":
                return call_openai(prompt)
            elif mode == "Anthropic Analysis":
                return call_anthropic(prompt)
            else:
                break # Fallback handled below
        except ValueError as e:
            logger.warning(f"JSON parsing failed on attempt {attempt+1}: {e}")
            prompt += "\n\nCRITICAL: The previous output was invalid JSON. You MUST return ONLY valid JSON."
        except Exception as e:
            logger.error(f"API call failed on attempt {attempt+1}: {e}")
            
    raise PromptParsingError("Exhausted retries or no API keys available.")

def analyze_startup(startup: StartupInput) -> ValidationReport:
    """Main entrypoint for analysis. Returns a ValidationReport."""
    try:
        if Config.get_analysis_mode() == "Local Heuristic Analysis":
            logger.info("Using heuristic engine.")
            return generate_fallback_report(startup)
            
        data = run_analysis_with_retries(startup)
        
        # Build the final report
        report = ValidationReport(
            analysis_mode=Config.get_analysis_mode(),
            input_data=startup,
            **data
        )
        return report
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}. Falling back to heuristics.")
        return generate_fallback_report(startup)
