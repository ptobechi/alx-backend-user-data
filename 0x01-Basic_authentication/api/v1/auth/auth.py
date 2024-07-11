#!/usr/bin/env python3
"""
Authentication module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class to manage the API authentication
    """
    def require_auth(self, path: str,
                     excluded_paths: List[str]) -> bool:
        """
        Method to check if authentication is required
        """
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        # Normalize path to ensure it ends with a slash
        if not path.endswith('/'):
            path += '/'

        # Check if the normalized path is in excluded_paths
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Method to get the authorization header from a request
        """
        if request is None or "Authorization" not in request.headers:
            return None

        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Method to get the current user from a request
        """
        return None
