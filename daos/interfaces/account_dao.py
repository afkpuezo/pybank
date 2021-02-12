"""
This 'interface' / abstract class / whatever describes the methods needed for DAO
functionality related to Accounts.

@author: Andrew Curry
"""
from models.account import Account
from models.user import User


class AccountDAO():
    """
    This 'interface' / abstract class / whatever describes the methods needed for DAO
    functionality related to Accounts.
    """

    def write(self, account):
        """
        Save or update the given account object(s).
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find(self, id):
        """
        Returns the Account object(s) corresponding to the given id(s), or None if there
        is(are) no such Account(s)
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find_by_owner(self, username: str) -> list[Account]:
        """
        Returns a list of all the the Account objects owned by the given user, or an empty
        list if there are no such Accounts.
        NOTE: default implementation just calls find_by_owner_username w/ user's username
        Raises DAOException if there is a problem with the database.
        """
        pass