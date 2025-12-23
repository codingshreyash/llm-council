"""Configuration for the LLM Council."""

import os
from dotenv import load_dotenv

load_dotenv()

# Provider API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Council members - list of model identifiers in format "provider:model_name"
COUNCIL_MODELS = [
    "openai:gpt-4o",
    "google:gemini-2.0-flash-exp",
    "anthropic:claude-3-5-sonnet-20241022",
]

# Chairman model - synthesizes final response (format: "provider:model_name")
CHAIRMAN_MODEL = "google:gemini-2.0-flash-exp"

# Data directory for conversation storage
DATA_DIR = "data/conversations"
