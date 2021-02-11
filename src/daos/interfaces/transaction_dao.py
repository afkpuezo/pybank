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

    def find_by_account(self, account: Account) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects involving the given Account.
        NOTE: default implementation just calls find_by_account_id with account's id
        Raises DAOException if there is a problem with the database.
        """
        return self.find_by_account_id(account.id)

    def find_by_account_id(self, account_id: int) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects involving the Account with the 
        given id.
        Raises DAOException if there is a problem with the database.
        """
        pass

    def find_after_time(self, start: int) -> list[Transaction]:
        """
        Returns a list of all the Transaction objects occuring after the given timestamp,
        or an empty list if there are no such Transactions.
        """
        pass