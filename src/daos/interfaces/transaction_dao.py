"""
This 'interface' / abstract class / whatever describes the methods needed for DAO
functionality related to Transactions.

@author: Andrew Curry
"""
from models.transaction import Transaction
from models.user import User
from models.account import Account
from enums.action_util import Action


class TransactionDAO():
    """
    This 'interface' / abstract class / whatever describes the methods needed for DAO
    functionality related to Transactions.
    """

    def write(self, transaction):
        """
        Save or update the given transaction object(s).
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find(self, id):
        """
        Returns the Transaction object(s) corresponding to the given id(s), or None if 
        there is(are) no such Transaction(s)
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find_by_acting_user(self, user: User) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects owned by the given user, or an 
        empty list if there are no such Transactions.
        NOTE: default implementation just calls find_by_acting_username w/ user's username
        Raises DAOException if there is a problem with the database.
        """
        return self.find_by_acting_username(user.username)

    def find_by_acting_username(self, username: str) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects owned by the user with the given
        username, or an empty list if there are no such Transactions.
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find_by_account(self, account: Account, mode: int = 0) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects involving the given Account.
        If the mode parameter is 0, all such Transactions will be included; if mode is 1,
        only Transactions where the account is the source account; if mode is 2, only 
        Transactions where the account is the destination account.
        NOTE: default implementation just calls find_by_account_id with account's id
        Raises DAOException if there is a problem with the database.
        """
        return self.find_by_account_id(account.id, mode)

    def find_by_account_id(self, id: int, mode: int = 0) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects involving the Account with the 
        given id. If the mode parameter is 0, all such Transactions will be included; if 
        mode is 1, only Transactions where the account is the source account; if mode is 
        2, only Transactions where the account is the destination account.
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find_after_time(self, start: int) -> list[Transaction]:
        """
        Returns a list of all the Transaction objects occuring after the given timestamp,
        or an empty list if there are no such Transactions.
        """
        pass