import logging
from datetime import datetime

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Log to file
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
