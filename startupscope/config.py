import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")
    
    DEFAULT_EXPORT_FORMAT = os.getenv("DEFAULT_EXPORT_FORMAT", "pdf")
    USE_LLM = os.getenv("USE_LLM", "auto")
    
    DATABASE_PATH = os.getenv("DATABASE_PATH", "data/startupscope.db")
    LOG_PATH = os.getenv("LOG_PATH", "data/startupscope.log")

    @classmethod
    def get_analysis_mode(cls):
        """Determine the current analysis mode based on available keys."""
        if cls.USE_LLM.lower() == "false":
            return "Local Heuristic Analysis"
        if cls.OPENAI_API_KEY:
            return "OpenAI Analysis"
        if cls.ANTHROPIC_API_KEY:
            return "Anthropic Analysis"
        return "Local Heuristic Analysis"
