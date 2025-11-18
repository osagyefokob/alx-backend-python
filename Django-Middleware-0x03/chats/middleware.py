# Django-Middleware-0x03/chats/middleware.py

from datetime import datetime, timedelta
from django.http import HttpResponseForbidden, HttpResponse
import threading

# --- Existing middleware (RequestLoggingMiddleware, RestrictAccessByTimeMiddleware) ---
from datetime import datetime as _dt
import os as _os

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        base_dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
        self.log_file = _os.path.join(base_dir, "requests.log")

    def __call__(self, request):
        user = request.user if hasattr(request, "user") else "Anonymous"
        path = request.path
        log_entry = f"{_dt.now()} - User: {user} - Path: {path}\n"
        with open(self.log_file, "a") as f:
            f.write(log_entry)
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        # Allow access ONLY between 6PM (18) and 9PM (21)
        if current_hour < 18 or current_hour > 21:
            return HttpResponseForbidden("Access restricted during this time.")
        return self.get_response(request)


# --- Task 3: OffensiveLanguageMiddleware (rate-limit by IP) ---
class OffensiveLanguageMiddleware:
    """
    Limits number of POST requests (messages) from each IP address.
    Rule: max_messages = 5 per time_window_seconds = 60 (1 minute).
    Counts only POST requests (assumed to be message sends).
    """

    def __init__(self, get_response, max_messages: int = 5, time_window_seconds: int = 60):
        self.get_response = get_response
        self.max_messages = max_messages
        self.time_window = timedelta(seconds=time_window_seconds)
        # storage: { ip: [datetime_of_post1, datetime_of_post2, ...] }
        self._lock = threading.Lock()
        self.ip_requests = {}

    def _cleanup_old(self, timestamps, now):
        """Remove timestamps older than the time window."""
        cutoff = now - self.time_window
        # keep only timestamps >= cutoff
        return [t for t in timestamps if t >= cutoff]

    def __call__(self, request):
        # Only consider POST requests (messages)
        if request.method == "POST":
            # get client's IP (basic method). If behind proxy, ALX doesn't require X-Forwarded-For handling.
            ip = request.META.get("REMOTE_ADDR", "unknown")

            now = datetime.now()

            with self._lock:
                timestamps = self.ip_requests.get(ip, [])
                # cleanup
                timestamps = self._cleanup_old(timestamps, now)

                if len(timestamps) >= self.max_messages:
                    # Too many requests in time window -> block
                    # Return 429 Too Many Requests
                    return HttpResponse(
                        "Rate limit exceeded: send limit is 5 messages per minute",
                        status=429,
                    )

                # record this POST
                timestamps.append(now)
                self.ip_requests[ip] = timestamps

        # For non-POST or when under limit, continue processing
        return self.get_response(request)
