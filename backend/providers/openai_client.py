"""OpenAI API client."""

import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
_client = None


def get_client():
    """Get or create OpenAI client instance."""
    global _client
    if _client is None:
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = AsyncOpenAI(api_key=OPENAI_API_KEY)
    return _client


async def query_openai(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query OpenAI model.
    
    Args:
        model: OpenAI model name (e.g., "gpt-4o", "gpt-4-turbo")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
    
    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    try:
        client = get_client()
        
        # Convert messages format if needed (OpenAI expects role/content)
        formatted_messages = [
            {"role": msg["role"], "content": msg["content"]}
            for msg in messages
        ]
        
        response = await client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            timeout=timeout
        )
        
        message = response.choices[0].message
        
        return {
            'content': message.content,
            'reasoning_details': getattr(message, 'reasoning_details', None)
        }
    
    except Exception as e:
        print(f"Error querying OpenAI model {model}: {e}")
        return None

