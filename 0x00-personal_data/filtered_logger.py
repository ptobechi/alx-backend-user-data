#!/usr/bin/env python3
"""
Module to obfuscate specific fields in a log message.
"""

import re
import logging
from typing import List, Tuple

PII_FIELDS: Tuple[str, ...] = (
    "name", "email", "phone", "ssn", "password"
)


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """
    Return the log message obfuscated.

    Args:
        fields (List[str]):
            List of fields to obfuscate.
        redaction (str):
            String to replace the field values with.
        message (str):
            The log line to process.
        separator (str):
            The character that separates the fields in the log line.

    Returns:
        str: The obfuscated log line.
    """
    pattern = '|'.join(f'{field}=[^{separator}]*' for field in fields)
    return re.sub(pattern, lambda m: f"{m.group().split('=')[0]}={redaction}",
                  message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class for obfuscating sensitive
    information in log messages.
    """
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize the formatter with specific fields to redact.

        Args:
            fields (List[str]): List of fields to obfuscate.
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record, obfuscating the specified fields.

        Args:
            record (logging.LogRecord): The log record to process.

        Returns:
            str: The formatted log record with obfuscated fields.
        """
        record.msg = filter_datum(self.fields,
                                  self.REDACTION,
                                  record.msg,
                                  self.SEPARATOR)
        return super(RedactingFormatter, self).format(record)

    def get_logger() -> logging.Logger:
        """
        Get a logger configured with RedactingFormatter.

        Returns:
            logging.Logger: Configured logger.
        """
        logger = logging.getLogger("user_data")
        logger.setLevel(logging.INFO)
        logger.propagate = False

        handler = logging.StreamHandler()
        handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))

        logger.addHandler(handler)

        return logger
