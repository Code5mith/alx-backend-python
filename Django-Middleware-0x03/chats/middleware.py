import logging
from datetime import datetime
from django.http import HttpResponseForbidden

# --- Setup logger for RequestLoggingMiddleware ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


# --- Middleware 1: Logs user requests ---
class RequestLoggingMiddleware:
    """
    Logs each user request to requests.log with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


# --- Middleware 2: Restrict access by time ---
class RestrictAccessByTimeMiddleware:
    """
    Restricts access to chats/messages outside 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("18:00", "%H:%M").time()  # 6 PM
        end_time = datetime.strptime("21:00", "%H:%M").time()    # 9 PM

        # Only apply to chat/message paths
        if "messages" in request.path or "chats" in request.path:
            if not (start_time <= now <= end_time):
                return HttpResponseForbidden("Chat access is only allowed between 6 PM and 9 PM.")

        response = self.get_response(request)
        return response
from datetime import datetime
from django.http import HttpResponseForbidden

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to chat/messages outside 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now = datetime.now().time()
        start_time = datetime.strptime("18:00", "%H:%M").time()  # 6 PM
        end_time = datetime.strptime("21:00", "%H:%M").time()    # 9 PM

        # Apply only to chat/message URLs
        if "messages" in request.path or "chats" in request.path:
            if not (start_time <= now <= end_time):
                return HttpResponseForbidden(
                    "Chat access is only allowed between 6 PM and 9 PM."
                )

        response = self.get_response(request)
        return response
