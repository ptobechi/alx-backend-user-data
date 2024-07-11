#!/usr/bin/env python3
"""
Basic Authentication module for the API
"""
from api.v1.auth.auth import Auth


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


def decode_base64_authorization_header(
        self, base64_authorization_header: str) -> str:
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
