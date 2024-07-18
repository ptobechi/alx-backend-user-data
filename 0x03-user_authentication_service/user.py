#!/usr/bin/env python3
"""User model for the user authentication service."""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    """User model for storing user data."""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

# Example usage
if __name__ == "__main__":
    # SQLite engine for demonstration purposes
    engine = create_engine('sqlite:///:memory:', echo=True)
    
    # Create all tables in the engine
    Base.metadata.create_all(engine)

    # Create a configured "Session" class
    Session = sessionmaker(bind=engine)
    
    # Create a Session
    session = Session()

    # Print table name and columns
    print(User.__tablename__)
    for column in User.__table__.columns:
        print("{}: {}".format(column, column.type))
