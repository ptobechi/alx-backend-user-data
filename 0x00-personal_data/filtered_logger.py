#!/usr/bin/env python3
"""
Module to obfuscate specific fields in a log message.
"""

import re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Return the log message obfuscated.

    Args:
        fields (List[str]): List of fields to obfuscate.
        redaction (str): String to replace the field values with.
        message (str): The log line to process.
        separator (str): The character that separates the fields in the log line.

    Returns:
        str: The obfuscated log line.
    """
    pattern = '|'.join(f'{field}=[^{separator}]*' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)
