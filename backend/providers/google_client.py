"""Google Generative AI (Gemini) API client."""

import os
import asyncio
from typing import List, Dict, Any, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Google client
_client_initialized = False


def initialize_client():
    """Initialize Google Generative AI client."""
    global _client_initialized
    if not _client_initialized:
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=GOOGLE_API_KEY)
        _client_initialized = True


def _query_google_sync(
    model: str,
    messages: List[Dict[str, str]]
) -> Optional[Dict[str, Any]]:
    """
    Synchronous Google query function (to be run in thread).
    """
    try:
        initialize_client()
        
        # Get the model instance
        model_instance = genai.GenerativeModel(model)
        
        # Google's API expects a different message format
        # Convert messages to a single prompt string or use chat history
        # For simplicity, we'll concatenate messages into a prompt
        prompt_parts = []
        
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                prompt_parts.append(content)
            elif role == "assistant":
                # For assistant messages, we need to handle them differently
                # Google's API can handle chat history, but for simplicity we'll append
                prompt_parts.append(f"Assistant: {content}")
            elif role == "system":
                prompt_parts.append(f"System: {content}")
        
        # Combine into a single prompt
        prompt = "\n\n".join(prompt_parts)
        
        # Generate content (synchronous call)
        response = model_instance.generate_content(prompt)
        
        # Extract text from response
        content = ""
        if response.text:
            content = response.text
        elif response.candidates and response.candidates[0].content:
            content = response.candidates[0].content.parts[0].text
        
        return {
            'content': content,
            'reasoning_details': None  # Google doesn't expose reasoning details
        }
    
    except Exception as e:
        print(f"Error querying Google model {model}: {e}")
        return None


async def query_google(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query Google Gemini model.
    
    Args:
        model: Google model name (e.g., "gemini-2.0-flash-exp", "gemini-1.5-pro")
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
    
    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    try:
        # Run the synchronous function in a thread pool
        result = await asyncio.wait_for(
            asyncio.to_thread(_query_google_sync, model, messages),
            timeout=timeout
        )
        return result
    except asyncio.TimeoutError:
        print(f"Timeout querying Google model {model}")
        return None
    except Exception as e:
        print(f"Error querying Google model {model}: {e}")
        return None

