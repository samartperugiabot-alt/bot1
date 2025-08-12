import logging
import sys

# Configure logger to output in a structured format (e.g., JSON-like)
# This is better for log analysis services.
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout,
)

logger = logging.getLogger("SmartStudentBot")

# Example of how to use the logger in other files:
# from .logger import logger
# logger.info("This is an info message.")
# logger.warning("This is a warning.")
# logger.error("This is an error.")
