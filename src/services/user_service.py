"""
Handles the service-layer logic for User-related operations.

@author: Andrew Curry
"""
from models.user import User
from daos.interfaces.user_dao import UserDAO
from exceptions.service_exception import ServiceException
from exceptions.dao_exception import DAOException


class UserService():
    """
    Handles the service-layer logic for User-related operations.
    """

    # ----------
    # CONSTRUCTOR
    # ----------

    def __init__(self, user_dao: UserDAO) -> None:
        self.user_dao = user_dao

    # ----------
    # SERVICE METHODS
    # ----------

    def register_user(self, user: User) -> User:
        """
        If user is unique (eg: username not yet in the system), register it.
        Raises a ServiceException if there is a problem, such as if user is not unique.
        """
        try:
            if self.user_dao.find(user.username):
                raise ServiceException("This user already exists.")
            else:
                return self.user_dao.write(user)
        except DAOException as e:
            raise ServiceException("There was a problem with the DAO:" + e.message)

    def log_in(self, username: str) -> User:
        """
        If username corresponds to a User, return it. If it doesn't, return None.
        Raises a ServiceException if there is a problem.
        """
        try:
            return self.user_dao.find(username)
        except DAOException as e:
            raise ServiceException("There was a problem with the DAO:" + e.message)

    def log_out(self):
        """
        Doesn't actually do anything right now
        """
        pass