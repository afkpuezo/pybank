"""
A straightforward implementation of TransactionDAO.

@author: Andrew Curry
"""
from daos.interfaces.transaction_dao import TransactionDAO
from models.transaction import Transaction
from exceptions.dao_exception import DAOException
import pymongo


class TransactionDAOImpl(TransactionDAO):
    """
    A straightforward implementation of TransactionDAO.
    """

    # ----------
    # INTERFACE METHODS
    # ----------

    def write(self, transaction: Transaction):
        """
        Save or update the given transaction object.
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["transactions"]
            if transaction.id == -1: # not yet saved
                # get transaction with the current highest id
                highest_transaction: dict = mycol.find_one(sort=[("id", -1)])
                if highest_transaction:
                    transaction.id = highest_transaction["id"] + 1
                else:
                    transaction.id = 1
                result = mycol.insert_one(transaction.to_dict())
                if result:
                    return transaction
                else:
                    raise DAOException("Unable to write transaction.")
            else:
                result = mycol.upsert_one(transaction.to_dict())
                if result:
                    return transaction
                else:
                    raise DAOException("Unable to write transaction.")
        except Exception as e:
            raise DAOException("Problem in TransactionDAOImpl.")

    def find(self, id: int):
        """
        Returns the Transaction object(s) corresponding to the given id(s), or None if 
        there is(are) no such Transaction(s)
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["transactions"]
            return Transaction.from_dict(mycol.find_one({"id": id}))
        except Exception as e:
            raise DAOException("Problem in TransactionDAOImpl: " + e)

    def find_by_account(self, account_id: int) -> list[Transaction]:
        """
        Returns a list of all the the Transaction objects involving the Account with the 
        given id.
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["transactions"]
            results = mycol.find({"$or": [
                {"source_account_id" : account_id},
                {"destination_account_id" : account_id}
            ]})
            answer: list[Transaction] = []
            for d in results:
                answer.append(Transaction.from_dict(d))
            return answer
        except Exception as e:
            raise DAOException("Problem in TransactionDAOImpl: " + e)

    def find_after_time(self, start: int) -> list[Transaction]:
        """
        Returns a list of all the Transaction objects occuring after the given timestamp,
        or an empty list if there are no such Transactions.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["transactions"]
            results = mycol.find({"time" : {"$gt" : start}})
            answer: list[Transaction] = []
            for d in results:
                answer.append(Transaction.from_dict(d))
            return answer
        except Exception as e:
            raise DAOException("Problem in TransactionDAOImpl: " + e)