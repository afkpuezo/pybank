"""
A straightforward implementation of UserDAO.

@author: Andrew Curry
"""
from daos.interfaces.user_dao import UserDAO
from models.user import User
from exceptions.dao_exception import DAOException
import pymongo


class UserDAOImpl(UserDAO):
    """
    A straightforward implementation of UserDAO.
    """

    # ----------
    # INTERFACE METHODS
    # ----------

    def write(self, user: User) -> User:
        """
        Saves or updates the given user object
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["users"]
            if mycol.insert_one(user.to_dict()):
                return user
            else:
                raise DAOException("Unabable to write user.")
        except Exception as e:
            raise DAOException("Problem in UserDAOImpl.")
    
    def find(self, username: str) -> User:
        """
        Returns the User object associated with the given username.
        Returns null if no such User is found.
        Raises DAOException if there is a problem with the database.
        """
        try:
            myclient = pymongo.MongoClient()
            mydb = myclient["pybank"]
            mycol = mydb["users"]
            return User.from_dict(mycol.find_one({"username": username}))
        except Exception as e:
            raise DAOException("Problem in UserDAOImpl: " + e)
