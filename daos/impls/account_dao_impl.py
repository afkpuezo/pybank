"""
A straightforward implementation of AccountDAO.

@author: Andrew Curry
"""
from daos.interfaces.account_dao import AccountDAO
from models.account import Account
from models.user import User
from exceptions.dao_exception import DAOException
import pymongo


class AccountDAOImpl(AccountDAO):
    """
    A straightforward implementation of AccountDAO.
    """

    # ----------
    # INTERFACE METHODS
    # ----------

    def write(self, account: Account) -> Account:
        """
        Save or update the given account object.
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["accounts"]
            if account.id == -1: # not yet saved
                # get account with the current highest id
                highest_account: dict = mycol.find_one(sort=[("id", -1)])
                if highest_account:
                    account.id = highest_account["id"] + 1
                else:
                    account.id = 1
                result = mycol.insert_one(account.to_dict())
                if result:
                    return account
                else:
                    raise DAOException("Unable to write account.")
            else:
                result = mycol.upsert_one(account.to_dict())
                if result:
                    return account
                else:
                    raise DAOException("Unable to write account.")
        except Exception as e:
            raise DAOException("Problem in AccountDAOImpl.")

    def find(self, id: int):
        """
        Returns the Account object(s) corresponding to the given id(s), or None if there
        is(are) no such Account(s)
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["accounts"]
            return Account.from_dict(mycol.find_one({"id": id}))
        except Exception as e:
            raise DAOException("Problem in AccountDAOImpl: " + e)

    def find_by_owner(self, username: str) -> list[Account]:
        """
        Returns a list of all the the Account objects owned by the given user, or an empty
        list if there are no such Accounts.
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["accounts"]
            results = mycol.find({"owner_username": username})
            answer: list[Account] = []
            for d in results:
                answer.append(Account.from_dict(d))
            return answer
        except Exception as e:
            raise DAOException("Problem in AccountDAOImpl: " + e)