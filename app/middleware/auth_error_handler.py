from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from jose import JWTError

class AuthErrorHandler(BaseHTTPMiddleware):
    """
    Middleware to catch authentication errors (401/403) and return a consistent JSON response.
    """

    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except JWTError:
            # JWT decoding or validation error
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "error": "Invalid or expired token.",
                    "hint": "Please log in again to continue."
                },
            )
        except Exception as exc:
            # Handle other unexpected errors gracefully
            if hasattr(exc, "status_code") and exc.status_code in [401, 403]:
                return JSONResponse(
                    status_code=exc.status_code,
                    content={
                        "error": exc.detail if hasattr(exc, "detail") else "Unauthorized access.",
                        "hint": "Ensure you are logged in with the correct account."
                    },
                )
            raise exc
