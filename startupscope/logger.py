import logging
import os
from startupscope.config import Config

def setup_logger(name: str) -> logging.Logger:
    """Setup and return a dedicated logger."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # File Handler
        if Config.LOG_PATH:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(Config.LOG_PATH), exist_ok=True)
            file_handler = logging.FileHandler(Config.LOG_PATH)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

    return logger

logger = setup_logger("startupscope")
