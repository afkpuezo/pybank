"""
Handles the service-layer logic for Account-related operations.

@author: Andrew Curry
"""
from enums.user_level_util import UserLevel
from models.account import Account
from models.user import User
from daos.interfaces.account_dao import AccountDAO
from daos.interfaces.user_dao import UserDAO
from exceptions.service_exception import ServiceException
from exceptions.dao_exception import DAOException


class AccountService():
    """
    Handles the service-layer logic for Account-related operations.

    @author: Andrew Curry
    """
    
    # ----------
    # CONSTRUCTOR
    # ----------

    def __init__(self, account_dao: AccountDAO, user_dao: UserDAO) -> None:
        self.account_dao = account_dao
        self.user_dao = user_dao
    
    # ----------
    # SERVICE METHODS
    # ----------

    def open_account(self, owner: User) -> Account:
        """
        A customer opens a new account, and returns that account.
        Fails and raises a ServiceException if:
            - the owner does not exist
            - the owner is not a customer
            - there is a DAOException
        """
        try:
            if not self.user_dao.find(owner.username):
                raise ServiceException("User '" + owner.username + "' not found.")
            elif owner.level != UserLevel.CUSTOMER:
                raise ServiceException("Only CUSTOMERS can open accounts.")
            else: # if owner is valid
                account: Account = Account(owner_username = owner.username)
                return self.account_dao.write(account)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
    
    def approve_account(self, current_user: User, )