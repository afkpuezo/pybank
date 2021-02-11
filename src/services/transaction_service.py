"""
Handles the service-layer logic for Transaction-related operations.

@author: Andrew Curry
"""
from models.transaction import Transaction
from daos.interfaces.transaction_dao import TransactionDAO
from exceptions.service_exception import ServiceException
from exceptions.dao_exception import DAOException
from datetime import datetime


class TransactionService():
    """
    Handles the service-layer logic for Transaction-related operations.
    """
    
    # ----------
    # CONSTRUCTOR
    # ----------

    def __init__(self, transaction_dao: TransactionDAO) -> None:
        self.transaction_dao = transaction_dao
    
    # ----------
    # SERVICE METHODS
    # ----------

    def record(self, transaction: Transaction) -> Transaction:
        """
        Adds a timestamp to the transaction, and writes it to the database.
        Will NOT validate the given transaction.
        Fails and raises a ServiceException if:
            - there is a DAOException
        """
        transaction.time = datetime.timestamp(datetime.now())
        try:
            return self.transaction_dao.write(transaction)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)