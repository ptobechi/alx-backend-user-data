#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class for basic authentication handling
    Currently empty, to be extended for basic authentication methods.
    """
    def extract_base64_authorization_header(
                self, authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication.

        Args:
            authorization_header (str): The Authorization
            header string.

        Returns:
            str: The Base64 part of the Authorization
            header, or None if invalid.
        """
        if authorization_header is None or not isinstance(
                    authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None

        # Get the part after "Basic "
        base64_part = authorization_header.split(" ")[1].strip()

        return base64_part

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes a Base64 encoded string and returns
        it as a UTF-8 string.

        Args:
            base64_authorization_header (str):
            The Base64 encoded string.

        Returns:
            str: The decoded UTF-8 string, or
            None if invalid Base64.
        """
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
    
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        Extracts user credentials (email and password)
        from a decoded Base64 authorization header.

        Args:
            decoded_base64_authorization_header (str):
            The decoded Base64 authorization header string.

        Returns:
            tuple: A tuple containing user email and password,
            or (None, None) if not found or invalid.
        """
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(':', 1)
        return user_email, user_password

    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """
        Retrieves the User instance based on email and
        password credentials.

        Args:
            user_email (str): The email of the user.
            user_pwd (str): The password of the user.

        Returns:
            User: The User instance if credentials are valid and
            found in the database, None otherwise.
        """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        # Search for the user based on email
        users = User.search({"email": user_email})
        if not users:
            return None

        # Check if the password matches
        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user

    def current_user(self, request=None) -> User:
        """
        Retrieves the User instance based on Basic Authentication
        credentials in the request.

        Args:
            request (Request): The Flask request object
            containing Authorization header.

        Returns:
            User: The User instance if authentication is successful,
            None otherwise.
        """
        if request is None:
            return None

        # Extract Authorization header
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        # Extract Base64 part of Authorization header
        base64_header = self.extract_base64_authorization_header(auth_header)
        if base64_header is None:
            return None

        # Decode Base64 Authorization header
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None

        # Extract user credentials (email and password)
        user_email, user_pwd = self.extract_user_credentials(decoded_header)
        if user_email is None or user_pwd is None:
            return None

        # Retrieve User object based on credentials
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
