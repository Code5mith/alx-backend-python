from django.http import HttpResponseForbidden


import logging
from datetime import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class RequestLoggingMiddleware:
    """
    Middleware to log each user request to a file with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Determine the user (Anonymous if not logged in)
        user = request.user if request.user.is_authenticated else 'Anonymous'

        # Log request
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        # Proceed to the next middleware/view
        response = self.get_response(request)
        return response


class RolepermissionMiddleware:
    """
    Middleware to enforce role-based access.
    Only admin or moderator users can access certain URLs (e.g., message management).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define paths that require admin/moderator access
        restricted_paths = ["messages/manage", "chats/manage"]  # adjust as needed

        # Check if request path is restricted
        if any(path in request.path for path in restricted_paths):
            user = request.user
            if not user.is_authenticated:
                return HttpResponseForbidden("Access denied: unauthenticated user.")
            # Assuming 'role' attribute exists on user model
            if getattr(user, "role", None) not in ["admin", "moderator"]:
                return HttpResponseForbidden("Access denied: insufficient permissions.")

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app outside 6 PM - 9 PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current server time
        now = datetime.now().time()

        # Define allowed start and end times
        start_time = datetime.strptime("18:00", "%H:%M").time()  # 6 PM
        end_time = datetime.strptime("21:00", "%H:%M").time()    # 9 PM

        # Check if request path contains 'messages' or 'chats' (adjust as needed)
        if "messages" in request.path or "chats" in request.path:
            # Deny access if current time is outside allowed range
            if not (start_time <= now <= end_time):
                return HttpResponseForbidden("Chat access is only allowed between 6 PM and 9 PM.")

        # Proceed to next middleware or view
        response = self.get_response(request)
        return response