"""Anthropic API client."""

import os
from typing import List, Dict, Any, Optional
from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Initialize Anthropic client
_client = None


def get_client():
    """Get or create Anthropic client instance."""
    global _client
    if _client is None:
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY environment variable is not set")
        _client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
    return _client


async def query_anthropic(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query Anthropic model.
    
    Args:
        model: Anthropic model name (e.g., "claude-sonnet-4-20250514", "claude-3-5-sonnet-20241022")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
    
    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    try:
        client = get_client()
        
        # Anthropic requires system message to be separate and messages to be in specific format
        # Convert messages: Anthropic expects messages array with role 'user' or 'assistant'
        # System messages should be extracted separately
        system_message = None
        formatted_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            elif msg["role"] in ["user", "assistant"]:
                formatted_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Anthropic API call
        response = await client.messages.create(
            model=model,
            max_tokens=4096,
            system=system_message if system_message else None,
            messages=formatted_messages,
            timeout=timeout
        )
        
        # Extract content from response
        # Anthropic returns content as a list of text blocks
        content = ""
        for block in response.content:
            if block.type == "text":
                content += block.text
        
        return {
            'content': content,
            'reasoning_details': None  # Anthropic doesn't expose reasoning details in the same way
        }
    
    except Exception as e:
        print(f"Error querying Anthropic model {model}: {e}")
        return None

