#!/usr/bin/env python3
"""
User Session Model

This module defines the UserSession model for storing session IDs in a database.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid


Base = declarative_base()


class UserSession(Base):
    """ UserSession Model """

    __tablename__ = 'user_sessions'

    id = Column(String(60), primary_key=True)
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, *args, **kwargs):
        """ Initialize UserSession """
        super().__init__(*args, **kwargs)
        self.id = str(uuid.uuid4())
