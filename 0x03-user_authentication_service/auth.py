#!/usr/bin/env python3
"""Authentication module"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password with bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
