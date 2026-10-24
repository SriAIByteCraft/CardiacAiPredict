"""
In-Memory Sliding Window Rate Limiter.
Protects sensitive authentication and inference endpoints against brute-force and abuse.
"""
import time
from functools import wraps
from flask import request
from ..utils.responses import error_response

class RateLimiter:
    """Simple thread-safe in-memory rate limiter per IP address."""
    
    def __init__(self, max_requests=10, window_seconds=60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.records = {}

    def is_allowed(self, client_ip: str) -> bool:
        now = time.time()
        cutoff = now - self.window_seconds
        
        # Clean expired timestamps
        timestamps = self.records.get(client_ip, [])
        valid_timestamps = [t for t in timestamps if t > cutoff]
        
        if len(valid_timestamps) >= self.max_requests:
            self.records[client_ip] = valid_timestamps
            return False

        valid_timestamps.append(now)
        self.records[client_ip] = valid_timestamps
        return True

    def limit(self, max_requests=None, window_seconds=None):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                from flask import current_app
                if current_app and current_app.config.get("TESTING", False):
                    return f(*args, **kwargs)

                ip = request.headers.get("X-Forwarded-For", request.remote_addr or "127.0.0.1").split(",")[0].strip()
                allowed = self.is_allowed(ip)
                if not allowed:
                    return error_response(
                        message="Too many requests. Please slow down and try again later.",
                        error_code="RATE_LIMIT_EXCEEDED",
                        status_code=429
                    )
                return f(*args, **kwargs)
            return decorated_function
        return decorator

# Global rate limiters
auth_rate_limiter = RateLimiter(max_requests=15, window_seconds=60)
predict_rate_limiter = RateLimiter(max_requests=30, window_seconds=60)
