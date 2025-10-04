from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication if you want to extend logic later
    (e.g. logging, custom claims).
    """
    pass
