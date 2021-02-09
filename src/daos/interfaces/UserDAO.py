"""
This 'interface' / abstract class / whatever describes the methods needed for DAO
functionality related to Users.
"""
from models.User import User


class UserDAO():
    """
    This 'interface' / abstract class / whatever describes the methods needed for DAO
    functionality related to Users.
    """

    def write(self, user: User) -> User:
        """
        Saves or updates the given user object
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find(self, username: str):
        """
        Returns the User object associated with the given username.
        Returns null if no such User is found.
        Raises DAOException if there is a problem with the database.
        """
        pass