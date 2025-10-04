import time
from collections import defaultdict
from django.http import HttpResponseForbidden

class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages a user can send per minute (per IP).
    Blocks requests exceeding 5 POST messages per minute.
    """

    # Track requests per IP
    ip_requests = defaultdict(list)

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only track POST requests to chat/messages
        if request.method == "POST" and ("messages" in request.path or "chats" in request.path):
            ip = self.get_client_ip(request)
            now = time.time()

            # Clean up requests older than 60 seconds
            self.ip_requests[ip] = [t for t in self.ip_requests[ip] if now - t < 60]

            if len(self.ip_requests[ip]) >= 5:
                return HttpResponseForbidden(
                    "Message limit exceeded. Maximum 5 messages per minute allowed."
                )

            # Record current request
            self.ip_requests[ip].append(now)

        response = self.get_response(request)
        return response

    @staticmethod
    def get_client_ip(request):
        """
        Get the real client IP address from request headers.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
