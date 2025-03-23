from fastapi import Request, Response
import time
import json
from typing import Callable
from fastapi.responses import JSONResponse
from src.lib.logger import logger
from src.middleware.correlation import get_correlation_id

async def http_logger_middleware(request: Request, call_next: Callable):
    # Get request body
    request_body = {}
    if request.method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        try:
            # Check if request is multipart (file upload)
            content_type = request.headers.get("content-type", "")
            if "multipart/form-data" in content_type:
                request_body = "<file upload - content not logged>"
            else:
                body_bytes = await request.body()
                if body_bytes:
                    try:
                        request_body = json.loads(body_bytes.decode())
                    except json.JSONDecodeError:
                        request_body = body_bytes.decode()
        except:
            request_body = None

    # Convert query params to dict
    query_params = {}
    for key, value in request.query_params.items():
        query_params[key] = value

    # Get response
    response = await call_next(request)
    
    # Get response body
    response_body = b""
    async for chunk in response.body_iterator:
        response_body += chunk
    
    # Reconstruct response
    response_dict = {}
    if response.headers.get("content-type") == "application/json":
        try:
            response_dict = json.loads(response_body)
        except:
            response_dict = {"raw": str(response_body)}

    # Determine log level based on status code
    log_data = {
        "correlation_id": get_correlation_id(),
        "body": {
            "request": {
                "method": request.method,
                "path": request.url.path,
                "params": request.path_params,
                "query_params": query_params,
                "client_host": request.client.host,
                "body": request_body if request_body else None
            },
            "response": {
                "status_code": response.status_code,
                "body": response_dict
            }
        }
    }

    # Log with appropriate level based on status code
    if response.status_code >= 500:
        logger.error(f"{request.method} {request.url.path}", extra=log_data)
    elif response.status_code >= 400:
        logger.warning(f"{request.method} {request.url.path}", extra=log_data)
    else:
        logger.info(f"{request.method} {request.url.path}", extra=log_data)

    # Return a new response since we consumed the original response body
    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    ) 