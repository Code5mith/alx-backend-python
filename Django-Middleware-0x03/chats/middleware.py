from django.http import HttpResponseForbidden

class RolePermissionMiddleware:
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
            user
