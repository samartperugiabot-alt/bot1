import os
import json
import base64
from dotenv import load_dotenv
from typing import List, Optional

from .utils.logger import logger

# Load environment variables from .env file for local development
load_dotenv()

def get_env_var(key: str, default: Optional[str] = None) -> Optional[str]:
    """Gets an environment variable, logging an error if it's missing and no default is provided."""
    value = os.environ.get(key, default)
    if value is None and default is None:
        logger.error(f"FATAL: Environment variable '{key}' not set.")
    return value

# --- Core Bot Configuration ---
TELEGRAM_BOT_TOKEN: str = get_env_var("TELEGRAM_BOT_TOKEN")
BASE_URL: str = get_env_var("BASE_URL")
WEBHOOK_SECRET: str = get_env_var("WEBHOOK_SECRET")
ADMIN_CHAT_ID: int = int(get_env_var("ADMIN_CHAT_ID", "0"))

# --- API Keys ---
OPENWEATHERMAP_API_KEY: Optional[str] = get_env_var("OPENWEATHERMAP_API_KEY")
EXCHANGE_RATE_API_KEY: Optional[str] = get_env_var("EXCHANGE_RATE_API_KEY")
HUGGINGFACE_API_KEY: Optional[str] = get_env_var("HUGGINGFACE_API_KEY")

# --- Redis Configuration ---
REDIS_URL: Optional[str] = get_env_var("REDIS_URL")

# --- Google Services Configuration ---
SHEET_ID: Optional[str] = get_env_var("SHEET_ID")
GOOGLE_DRIVE_UPLOAD_FOLDER_ID: Optional[str] = get_env_var("GOOGLE_DRIVE_UPLOAD_FOLDER_ID")

def get_google_creds() -> Optional[dict]:
    """Decodes the base64 encoded Google credentials."""
    creds_base64 = get_env_var("GOOGLE_CREDS_BASE64")
    if not creds_base64:
        logger.error("GOOGLE_CREDS_BASE64 is not set. Google services will be unavailable.")
        return None
    try:
        creds_json = base64.b64decode(creds_base64).decode("utf-8")
        return json.loads(creds_json)
    except (json.JSONDecodeError, base64.binascii.Error) as e:
        logger.error(f"Failed to decode GOOGLE_CREDS_BASE64: {e}")
        return None

GOOGLE_CREDS: Optional[dict] = get_google_creds()

# --- Data Sources ---
GITHUB_DATA_URL: str = get_env_var("GITHUB_DATA_URL", "https://raw.githubusercontent.com/your-username/your-repo/main")

# --- Bot Behavior ---
DEFAULT_CITY: str = get_env_var("DEFAULT_CITY", "Perugia")
DEFAULT_LANG: str = get_env_var("DEFAULT_LANG", "fa")
SUPPORTED_LANGUAGES: List[str] = ["fa", "en", "it"]

# --- Webserver ---
PORT: int = int(get_env_var("PORT", "8000"))

# --- Constants for Sheet Names ---
USERS_SHEET_NAME = "users"
QUESTIONS_SHEET_NAME = "questions"
FEEDBACK_SHEET_NAME = "feedback"
# ... other sheet names

# --- Validation ---
if not all([TELEGRAM_BOT_TOKEN, BASE_URL, WEBHOOK_SECRET, ADMIN_CHAT_ID]):
    raise ValueError("One or more critical environment variables are missing: TELEGRAM_BOT_TOKEN, BASE_URL, WEBHOOK_SECRET, ADMIN_CHAT_ID")

logger.info("Configuration loaded successfully.")
