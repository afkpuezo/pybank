"""
Handles the service-layer logic for Transaction-related operations.

@author: Andrew Curry
"""
from daos.interfaces.user_dao import UserDAO
from enums.user_level_util import UserLevel
from models.account import Account
from models.transaction import Transaction
from daos.interfaces.transaction_dao import TransactionDAO
from daos.interfaces.account_dao import AccountDAO
from exceptions.service_exception import ServiceException
from exceptions.dao_exception import DAOException
from datetime import datetime

from models.user import User


class TransactionService():
    """
    Handles the service-layer logic for Transaction-related operations.
    """
    
    # ----------
    # CONSTRUCTOR
    # ----------

    def __init__(
            self, 
            transaction_dao: TransactionDAO, 
            account_dao: AccountDAO,
            user_dao: UserDAO) -> None:
        self.transaction_dao = transaction_dao
        self.account_dao = account_dao
        self.user_dao = user_dao
    
    # ----------
    # SERVICE METHODS
    # ----------

    def record(self, transaction: Transaction) -> Transaction:
        """
        Adds a timestamp to the transaction, and writes it to the database.
        Doensn't require the current user's username
        Will NOT validate the given transaction.
        Fails and raises a ServiceException if:
            - there is a DAOException
        """
        transaction.time = datetime.timestamp(datetime.now())
        try:
            return self.transaction_dao.write(transaction)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
    
    def find_by_account(
            self, current_username: str, account_id: int) -> list[Transaction]:
        """
        Returns a list of all of the transactions involving the given account, or an
        empty list if there are no such transactions.
        Fails and raises a ServiceException if:
            - the current user does not exist
            - the current user is not an admin
            - The account does not exist
            - there is a DAOException
        """
        try:
            current_user: User = self.user_dao.find(current_username)
            if not current_user:
                raise ServiceException("User '" + current_username + "' not found.")
            elif current_user.level != UserLevel.ADMIN:
                raise ServiceException("Only ADMINS can view transaction history.")
            if not self.account_dao.find(account_id):
                raise ServiceException("Account #" + str(account_id) + "does not exist.")
            return self.transaction_dao.find_by_account(account_id)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)