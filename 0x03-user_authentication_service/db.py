#!/usr/bin/env python3
"""DB module"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base, User


class DB:
    """DB class"""

    def __init__(self) -> None:
        """Initialize a new DB instance"""
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Add a new user to the database

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The newly created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """Find a user by arbitrary keyword arguments

        Args:
            **kwargs:
                Arbitrary keyword arguments to filter the users table.

        Returns:
            User:
                The first User object that matches the filters.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If query is invalid.
        """
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise NoResultFound("No user found with the given criteria.")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments.")
        except Exception as e:
            raise InvalidRequestError(f"Unexpected error: {e}")

    def update_user(self, user_id: int, **kwargs) -> None:
        """Update user attributes

        Args:
            user_id (int): The ID of the user to update.
            **kwargs:
                Arbitrary keyword arguments to update the user's attributes.

        Returns:
            None

        Raises:
            ValueError: If an invalid attribute is passed.
            NoResultFound: If the user with the given ID is not found.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError(f"Invalid attribute: {key}")
        self._session.commit()
