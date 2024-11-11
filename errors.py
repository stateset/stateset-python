"""
Contains error types for the Stateset SDK, providing a comprehensive set of 
exceptions for handling various API error scenarios.
"""
from typing import Any, Dict, Optional, Type
from http import HTTPStatus
import json

class StatesetError(Exception):
    """Base exception class for all Stateset API related errors."""
    
    def __init__(
        self,
        message: str,
        error_type: str,
        code: Optional[str] = None,
        detail: Optional[str] = None,
        path: Optional[str] = None,
        status_code: Optional[int] = None,
        raw_response: Optional[Dict[str, Any]] = None
    ) -> None:
        super().__init__(message)
        self.type = error_type
        self.code = code
        self.detail = detail
        self.path = path
        self.status_code = status_code
        self.raw_response = raw_response or {}
        
    @classmethod
    def from_response(
        cls,
        response_content: bytes,
        status_code: Optional[int] = None
    ) -> "StatesetError":
        """Create an error instance from an API response."""
        try:
            data = json.loads(response_content)
        except (json.JSONDecodeError, UnicodeDecodeError):
            data = {
                "message": response_content.decode('utf-8', errors='replace'),
                "type": "api_error"
            }
            
        error_type = data.get("type", "api_error")
        message = data.get("message", "Unknown error occurred")
        
        # Map error types to specific error classes
        error_class = ERROR_TYPE_MAPPING.get(error_type, cls)
        
        return error_class(
            message=message,
            error_type=error_type,
            code=data.get("code"),
            detail=data.get("detail"),
            path=data.get("path"),
            status_code=status_code,
            raw_response=data
        )

class StatesetInvalidRequestError(StatesetError):
    """Raised when the request is invalid."""
    
    def __init__(
        self,
        message: str = "Invalid request",
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="invalid_request_error",
            **kwargs
        )

class StatesetAPIError(StatesetError):
    """Raised when there's an API error."""
    
    def __init__(
        self,
        message: str = "API error occurred",
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="api_error",
            **kwargs
        )

class StatesetAuthenticationError(StatesetError):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="authentication_error",
            **kwargs
        )

class StatesetPermissionError(StatesetError):
    """Raised when permission is denied."""
    
    def __init__(
        self,
        message: str = "Permission denied",
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="permission_error",
            **kwargs
        )

class StatesetNotFoundError(StatesetError):
    """Raised when a resource is not found."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: str = "resource",
        resource_id: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        if resource_id:
            message = f"{resource_type} not found: {resource_id}"
        super().__init__(
            message=message,
            error_type="not_found_error",
            **kwargs
        )
        self.resource_type = resource_type
        self.resource_id = resource_id

class StatesetConnectionError(StatesetError):
    """Raised when there's a connection error."""
    
    def __init__(
        self,
        message: str = "Connection error occurred",
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="connection_error",
            **kwargs
        )

class StatesetRateLimitError(StatesetError):
    """Raised when API rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        if retry_after:
            message = f"{message}. Retry after {retry_after} seconds"
        super().__init__(
            message=message,
            error_type="rate_limit_error",
            **kwargs
        )
        self.retry_after = retry_after

# Mapping of error types to their corresponding classes
ERROR_TYPE_MAPPING: Dict[str, Type[StatesetError]] = {
    "invalid_request_error": StatesetInvalidRequestError,
    "api_error": StatesetAPIError,
    "authentication_error": StatesetAuthenticationError,
    "permission_error": StatesetPermissionError,
    "not_found_error": StatesetNotFoundError,
    "connection_error": StatesetConnectionError,
    "rate_limit_error": StatesetRateLimitError
}

def raise_for_status_code(
    status_code: int,
    content: bytes,
    expected_codes: Optional[set[int]] = None
) -> None:
    """Raise appropriate error based on status code."""
    try:
        status_desc = HTTPStatus(status_code).phrase
    except ValueError:
        status_desc = "Unknown Status"

    if 200 <= status_code < 300:
        return

    try:
        error = StatesetError.from_response(content, status_code)
    except Exception:
        # If we can't parse the error response, create a generic error
        message = f"HTTP {status_code} {status_desc}"
        error = StatesetAPIError(message=message, status_code=status_code)
    
    # Map status codes to specific error types if not already mapped
    if not error.type:
        if status_code == 400:
            error = StatesetInvalidRequestError(message=str(error))
        elif status_code == 401:
            error = StatesetAuthenticationError(message=str(error))
        elif status_code == 403:
            error = StatesetPermissionError(message=str(error))
        elif status_code == 404:
            error = StatesetNotFoundError(message=str(error))
        elif status_code == 429:
            error = StatesetRateLimitError(message=str(error))
    
    raise error

__all__ = [
    "StatesetError",
    "StatesetInvalidRequestError",
    "StatesetAPIError",
    "StatesetAuthenticationError",
    "StatesetPermissionError",
    "StatesetNotFoundError",
    "StatesetConnectionError",
    "StatesetRateLimitError",
    "raise_for_status_code",
]