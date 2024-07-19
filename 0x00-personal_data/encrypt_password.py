#!/usr/bin/env python3
"""
Module for password hashing.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The hashed password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the generated salt
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed

def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validate that the provided password matches the hashed password.

    Args:
        hashed_password (bytes): The hashed password.
        password (str): The plain text password.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Check if the hashed password matches the provided password
    return bcrypt.checkpw(password.encode(), hashed_password)
