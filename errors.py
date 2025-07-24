"""
Enhanced error types for the Stateset SDK, providing comprehensive exception handling
with detailed context, debugging information, and actionable error messages.
"""
from typing import Any, Dict, Optional, Type, List
from http import HTTPStatus
import json
import traceback
from datetime import datetime


class StatesetError(Exception):
    """
    Base exception class for all Stateset API related errors.
    
    Provides rich context information to help developers debug issues quickly.
    """
    
    def __init__(
        self,
        message: str,
        error_type: str,
        code: Optional[str] = None,
        detail: Optional[str] = None,
        path: Optional[str] = None,
        status_code: Optional[int] = None,
        raw_response: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
        timestamp: Optional[datetime] = None,
        suggestions: Optional[List[str]] = None,
        documentation_url: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.type = error_type
        self.code = code
        self.detail = detail
        self.path = path
        self.status_code = status_code
        self.raw_response = raw_response or {}
        self.request_id = request_id
        self.timestamp = timestamp or datetime.now()
        self.suggestions = suggestions or []
        self.documentation_url = documentation_url
        
    def __str__(self) -> str:
        """Enhanced string representation with debugging context."""
        parts = [f"[{self.type}] {self.message}"]
        
        if self.status_code:
            parts.append(f"Status: {self.status_code}")
        
        if self.code:
            parts.append(f"Code: {self.code}")
        
        if self.request_id:
            parts.append(f"Request ID: {self.request_id}")
            
        if self.path:
            parts.append(f"Path: {self.path}")
        
        return " | ".join(parts)
    
    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"message={self.message!r}, "
            f"type={self.type!r}, "
            f"status_code={self.status_code}, "
            f"code={self.code!r}"
            ")"
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert error to dictionary for logging/serialization."""
        return {
            "error_type": self.type,
            "message": self.message,
            "code": self.code,
            "detail": self.detail,
            "path": self.path,
            "status_code": self.status_code,
            "request_id": self.request_id,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "suggestions": self.suggestions,
            "documentation_url": self.documentation_url,
            "raw_response": self.raw_response,
        }
    
    def get_debug_info(self) -> str:
        """Get detailed debugging information."""
        lines = [
            f"Error Type: {self.type}",
            f"Message: {self.message}",
            f"Timestamp: {self.timestamp}",
        ]
        
        if self.status_code:
            lines.append(f"HTTP Status: {self.status_code}")
        
        if self.code:
            lines.append(f"Error Code: {self.code}")
        
        if self.request_id:
            lines.append(f"Request ID: {self.request_id}")
        
        if self.path:
            lines.append(f"API Path: {self.path}")
        
        if self.detail:
            lines.append(f"Details: {self.detail}")
        
        if self.suggestions:
            lines.append("Suggestions:")
            for suggestion in self.suggestions:
                lines.append(f"  • {suggestion}")
        
        if self.documentation_url:
            lines.append(f"Documentation: {self.documentation_url}")
        
        if self.raw_response:
            lines.append(f"Raw Response: {json.dumps(self.raw_response, indent=2)}")
        
        return "\n".join(lines)
    
    @classmethod
    def from_response(
        cls,
        response_content: bytes,
        status_code: Optional[int] = None,
        request_id: Optional[str] = None,
        path: Optional[str] = None,
    ) -> "StatesetError":
        """Create an error instance from an API response with enhanced context."""
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
        
        # Extract additional context
        suggestions = data.get("suggestions", [])
        documentation_url = data.get("documentation_url")
        
        # Add default suggestions for common issues
        if not suggestions:
            suggestions = cls._get_default_suggestions(error_type, status_code)
        
        return error_class(
            message=message,
            error_type=error_type,
            code=data.get("code"),
            detail=data.get("detail"),
            path=path,
            status_code=status_code,
            raw_response=data,
            request_id=request_id,
            suggestions=suggestions,
            documentation_url=documentation_url,
        )
    
    @staticmethod
    def _get_default_suggestions(error_type: str, status_code: Optional[int]) -> List[str]:
        """Get default suggestions based on error type and status code."""
        suggestions = []
        
        if status_code == 401:
            suggestions.extend([
                "Check your API key is correct and not expired",
                "Ensure the API key has the required permissions",
                "Verify you're using the correct base URL"
            ])
        elif status_code == 403:
            suggestions.extend([
                "Verify your API key has sufficient permissions",
                "Check if the resource requires additional access rights",
                "Contact support if you believe this is an error"
            ])
        elif status_code == 404:
            suggestions.extend([
                "Verify the resource ID is correct",
                "Check if the resource exists and hasn't been deleted",
                "Ensure you're using the correct API endpoint"
            ])
        elif status_code == 429:
            suggestions.extend([
                "Implement exponential backoff in your retry logic",
                "Consider reducing request frequency",
                "Check if you can upgrade your rate limit"
            ])
        elif status_code and status_code >= 500:
            suggestions.extend([
                "This is likely a temporary server issue",
                "Try again after a short delay",
                "Contact support if the issue persists"
            ])
        
        return suggestions


class StatesetValidationError(StatesetError):
    """Raised when request validation fails."""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[Dict[str, List[str]]] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="validation_error",
            **kwargs
        )
        self.field_errors = field_errors or {}
    
    def get_field_error(self, field: str) -> List[str]:
        """Get validation errors for a specific field."""
        return self.field_errors.get(field, [])
    
    def has_field_error(self, field: str) -> bool:
        """Check if a field has validation errors."""
        return field in self.field_errors
    
    def get_debug_info(self) -> str:
        """Enhanced debug info including field-specific errors."""
        base_info = super().get_debug_info()
        
        if self.field_errors:
            lines = [base_info, "\nField Errors:"]
            for field, errors in self.field_errors.items():
                lines.append(f"  {field}:")
                for error in errors:
                    lines.append(f"    • {error}")
            return "\n".join(lines)
        
        return base_info


class StatesetInvalidRequestError(StatesetValidationError):
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
            suggestions=[
                "Check your API key is correct and not expired",
                "Ensure the API key has the required permissions",
                "Verify you're using the correct base URL",
                "Make sure you're sending the Authorization header correctly"
            ],
            documentation_url="https://docs.stateset.com/authentication",
            **kwargs
        )


class StatesetPermissionError(StatesetError):
    """Raised when permission is denied."""
    
    def __init__(
        self,
        message: str = "Permission denied",
        required_permission: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="permission_error",
            suggestions=[
                "Verify your API key has sufficient permissions",
                "Check if the resource requires additional access rights",
                "Contact support if you believe this is an error"
            ],
            documentation_url="https://docs.stateset.com/permissions",
            **kwargs
        )
        self.required_permission = required_permission


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
            suggestions=[
                "Verify the resource ID is correct",
                "Check if the resource exists and hasn't been deleted",
                "Ensure you're using the correct API endpoint",
                f"Make sure you have access to this {resource_type}"
            ],
            **kwargs
        )
        self.resource_type = resource_type
        self.resource_id = resource_id


class StatesetConnectionError(StatesetError):
    """Raised when there's a connection error."""
    
    def __init__(
        self,
        message: str = "Connection error occurred",
        cause: Optional[Exception] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="connection_error",
            suggestions=[
                "Check your internet connection",
                "Verify the API base URL is correct",
                "Check if there are any firewall restrictions",
                "Try again after a short delay"
            ],
            **kwargs
        )
        self.cause = cause


class StatesetTimeoutError(StatesetConnectionError):
    """Raised when a request times out."""
    
    def __init__(
        self,
        message: str = "Request timed out",
        timeout_duration: Optional[float] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            suggestions=[
                "Increase the request timeout",
                "Check your network connection",
                "Try the request again",
                "Consider breaking large requests into smaller ones"
            ],
            **kwargs
        )
        self.timeout_duration = timeout_duration


class StatesetRateLimitError(StatesetError):
    """Raised when API rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None,
        reset_time: Optional[datetime] = None,
        **kwargs: Any
    ) -> None:
        if retry_after:
            message = f"{message}. Retry after {retry_after} seconds"
        
        suggestions = [
            "Implement exponential backoff in your retry logic",
            "Consider reducing request frequency",
            "Check if you can upgrade your rate limit"
        ]
        
        if retry_after:
            suggestions.insert(0, f"Wait {retry_after} seconds before retrying")
        
        super().__init__(
            message=message,
            error_type="rate_limit_error",
            suggestions=suggestions,
            documentation_url="https://docs.stateset.com/rate-limits",
            **kwargs
        )
        self.retry_after = retry_after
        self.limit = limit
        self.remaining = remaining
        self.reset_time = reset_time


class StatesetMaintenanceError(StatesetError):
    """Raised when the API is under maintenance."""
    
    def __init__(
        self,
        message: str = "API is currently under maintenance",
        estimated_duration: Optional[str] = None,
        **kwargs: Any
    ) -> None:
        super().__init__(
            message=message,
            error_type="maintenance_error",
            suggestions=[
                "Check the status page for updates",
                "Try again later",
                "Subscribe to status notifications"
            ],
            documentation_url="https://status.stateset.com",
            **kwargs
        )
        self.estimated_duration = estimated_duration


class StatesetDeprecationWarning(UserWarning):
    """Warning for deprecated API features."""
    
    def __init__(
        self,
        message: str,
        deprecated_feature: str,
        removal_version: Optional[str] = None,
        alternative: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.deprecated_feature = deprecated_feature
        self.removal_version = removal_version
        self.alternative = alternative


# Enhanced mapping of error types to their corresponding classes
ERROR_TYPE_MAPPING: Dict[str, Type[StatesetError]] = {
    "validation_error": StatesetValidationError,
    "invalid_request_error": StatesetInvalidRequestError,
    "api_error": StatesetAPIError,
    "authentication_error": StatesetAuthenticationError,
    "permission_error": StatesetPermissionError,
    "not_found_error": StatesetNotFoundError,
    "connection_error": StatesetConnectionError,
    "timeout_error": StatesetTimeoutError,
    "rate_limit_error": StatesetRateLimitError,
    "maintenance_error": StatesetMaintenanceError,
}


def raise_for_status_code(
    status_code: int,
    content: bytes,
    request_id: Optional[str] = None,
    path: Optional[str] = None,
    expected_codes: Optional[set[int]] = None
) -> None:
    """Raise appropriate error based on status code with enhanced context."""
    try:
        status_desc = HTTPStatus(status_code).phrase
    except ValueError:
        status_desc = "Unknown Status"

    if 200 <= status_code < 300:
        return

    try:
        error = StatesetError.from_response(
            content, 
            status_code=status_code,
            request_id=request_id,
            path=path
        )
    except Exception:
        # If we can't parse the error response, create a generic error
        message = f"HTTP {status_code} {status_desc}"
        error = StatesetAPIError(
            message=message, 
            status_code=status_code,
            request_id=request_id,
            path=path
        )
    
    # Map status codes to specific error types if not already mapped
    if error.type == "api_error" and status_code:
        if status_code == 400:
            error = StatesetInvalidRequestError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
        elif status_code == 401:
            error = StatesetAuthenticationError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
        elif status_code == 403:
            error = StatesetPermissionError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
        elif status_code == 404:
            error = StatesetNotFoundError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
        elif status_code == 429:
            error = StatesetRateLimitError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
        elif status_code == 503:
            error = StatesetMaintenanceError(
                message=error.message,
                status_code=status_code,
                request_id=request_id,
                path=path
            )
    
    raise error


__all__ = [
    "StatesetError",
    "StatesetValidationError",
    "StatesetInvalidRequestError",
    "StatesetAPIError",
    "StatesetAuthenticationError",
    "StatesetPermissionError",
    "StatesetNotFoundError",
    "StatesetConnectionError",
    "StatesetTimeoutError",
    "StatesetRateLimitError",
    "StatesetMaintenanceError",
    "StatesetDeprecationWarning",
    "raise_for_status_code",
]
