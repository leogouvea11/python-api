from fastapi import Request, Response
from typing import Callable
import uuid
import contextvars
from functools import wraps

# Create a context variable to store the correlation ID
correlation_id_context = contextvars.ContextVar('correlation_id', default=None)

def get_correlation_id() -> str:
    """Get the correlation ID from the current context"""
    return correlation_id_context.get()

def with_correlation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cor_id = get_correlation_id()
        
        # Always create a new extra dict to avoid mutation issues
        extra = kwargs.get('extra', {})
        kwargs['extra'] = {**extra, 'correlation_id': cor_id}
        
        return func(*args, **kwargs)
    return wrapper

async def correlation_middleware(request: Request, call_next: Callable):
    # Generate or get correlation ID from headers
    correlation_id = request.headers.get('X-Correlation-ID') or str(uuid.uuid4())
    
    # Set the correlation ID and get the token
    token = correlation_id_context.set(correlation_id)
    
    try:
        # Get response
        response = await call_next(request)
        
        # Handle different response types
        if isinstance(response, Response):
            response.headers["X-Correlation-ID"] = correlation_id
        else:
            # If it's not a Response object, create a new Response
            new_response = Response(content=response)
            new_response.headers["X-Correlation-ID"] = correlation_id
            response = new_response
            
        return response
    finally:
        # Reset using the token
        correlation_id_context.reset(token) 