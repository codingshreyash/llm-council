"""Base provider interface and unified query functions."""

from typing import List, Dict, Any, Optional
from .openai_client import query_openai
from .anthropic_client import query_anthropic
from .google_client import query_google


async def query_model(
    model: str,
    messages: List[Dict[str, str]],
    timeout: float = 120.0
) -> Optional[Dict[str, Any]]:
    """
    Query a single model via the appropriate provider API.
    
    Model identifier format: "provider:model_name"
    Examples:
        - "openai:gpt-4o"
        - "anthropic:claude-sonnet-4-20250514"
        - "google:gemini-2.0-flash-exp"
    
    Args:
        model: Model identifier in format "provider:model_name"
        messages: List of message dicts with 'role' and 'content'
        timeout: Request timeout in seconds
    
    Returns:
        Response dict with 'content' and optional 'reasoning_details', or None if failed
    """
    # Parse provider and model name
    if ':' not in model:
        print(f"Error: Invalid model identifier format: {model}. Expected 'provider:model_name'")
        return None
    
    provider, model_name = model.split(':', 1)
    
    try:
        if provider == 'openai':
            return await query_openai(model_name, messages, timeout)
        elif provider == 'anthropic':
            return await query_anthropic(model_name, messages, timeout)
        elif provider == 'google':
            return await query_google(model_name, messages, timeout)
        else:
            print(f"Error: Unknown provider '{provider}' for model {model}")
            return None
    except Exception as e:
        print(f"Error querying model {model}: {e}")
        return None


async def query_models_parallel(
    models: List[str],
    messages: List[Dict[str, str]]
) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Query multiple models in parallel.
    
    Args:
        models: List of model identifiers in format "provider:model_name"
        messages: List of message dicts to send to each model
    
    Returns:
        Dict mapping model identifier to response dict (or None if failed)
    """
    import asyncio
    
    # Create tasks for all models
    tasks = [query_model(model, messages) for model in models]
    
    # Wait for all to complete
    responses = await asyncio.gather(*tasks)
    
    # Map models to their responses
    return {model: response for model, response in zip(models, responses)}

