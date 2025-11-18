from datetime import datetime
import os

class RequestLoggingMiddleware:
    """
    Logs every incoming request to requests.log with:
    timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # Set the path to requests.log inside the project
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.log_file = os.path.join(base_dir, "requests.log")

    def __call__(self, request):
        user = request.user if hasattr(request, "user") else "Anonymous"
        path = request.path

        # Format text exactly as ALX expects
        log_entry = f"{datetime.now()} - User: {user} - Path: {path}\n"

        # Write to requests.log
        with open(self.log_file, "a") as f:
            f.write(log_entry)

        # continue middleware chain
        response = self.get_response(request)
        return response
