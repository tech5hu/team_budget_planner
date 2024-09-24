# backends.py
from django.contrib.auth.backends import ModelBackend  # Importing ModelBackend for custom authentication
from .models import UserProfile  # Importing UserProfile model for user authentication
import logging  # Importing logging for debug and warning messages

# Setting up logging for the authentication process
logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    # Custom authenticate method to allow authentication using email
    def authenticate(self, request, email=None, password=None, **kwargs):
        logger.debug(f'Attempting to authenticate user with email: {email}')  # Log authentication attempt
        try:
            user = UserProfile.objects.get(email=email)  # Attempt to retrieve the user by email
        except UserProfile.DoesNotExist:
            logger.warning('User not found')  # Log a warning if the user does not exist
            return None  # Return None if the user is not found
        
        if user.check_password(password):  # Check if the provided password is correct
            logger.debug('User authenticated successfully')  # Log successful authentication
            return user  # Return the authenticated user
        
        logger.warning('Password mismatch')  # Log a warning for password mismatch
        return None  # Return None if the password does not match
