from datetime import datetime
from django.http import HttpResponseForbidden

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
