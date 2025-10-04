from django.http import HttpResponseForbidden

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
