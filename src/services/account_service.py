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

    def open_account(self, owner_username: str) -> Account:
        """
        A customer opens a new account, and returns that account.
        Fails and raises a ServiceException if:
            - the owner does not exist
            - the owner is not a customer
            - there is a DAOException
        """
        try:
            owner: User = self.user_dao.find(owner_username)
            if not owner:
                raise ServiceException("User '" + owner_username + "' not found.")
            elif owner.level != UserLevel.CUSTOMER:
                raise ServiceException("Only CUSTOMERS can open accounts.")
            else: # if owner is valid
                account: Account = Account(owner_username)
                return self.account_dao.write(account)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
    
    def approve_account(self, current_username: str, account_id: int) -> Account:
        """
        An admin approves an account that is pending.
        Fails and raises a ServiceException if:
            - the current user does not exist
            - the current user is not an admin
            - the account does not exist
            - the account has already been approved
            - there is a DAOException
        """
        try:
            current_user: User = self.user_dao.find(current_username)
            if not current_user:
                raise ServiceException("User '" + current_username + "' not found.")
            elif current_user.level != UserLevel.ADMIN:
                raise ServiceException("Only ADMINS can open accounts.")
            else:  # if user is valid
                target_account: Account = self.account_dao.find(account_id)
                if not target_account:
                    raise ServiceException("Account #" + str(account_id) + " not found.")
                elif target_account.is_approved:
                    raise ServiceException(
                            "Account #" + str(account_id) + " has already been approved.")
                else:  # valid user and account
                    target_account.is_approved = True
                    return target_account
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
    
    def deposit(self, current_username: str, account_id: int, amount: int) -> Account:
        """
        A customer makes a deposit into their own account.
        Fails and raises a ServiceException if:
            - the current user does not exist
            - the user is not a customer
            - the account does not exist
            - the user does not own the account
            - the account is not open/approved
            - the funds amount is not positive
            - there is a DAO exception
        """
        try:
            current_user: User = self.user_dao.find(current_username)
            if not current_user:
                raise ServiceException("User '" + current_username + "' not found.")
            elif current_user.level != UserLevel.CUSTOMER:
                raise ServiceException("Only CUSTOMERS can deposit funds.")
            else:  # if user is valid
                target_account: Account = self.account_dao.find(account_id)
                if not target_account:
                    raise ServiceException("Account #" + str(account_id) + " not found.")
                elif target_account.owner_username != current_username:
                    raise ServiceException(
                            "You do not have permission to access Account #" 
                            + str(account_id))
                elif not target_account.is_approved:
                    raise ServiceException(
                            "Account #" + str(account_id) + " has not yet been approved.")
                elif amount <= 0:
                    raise ServiceException("You must deposit a positive amount of funds.")
                else:  # valid user and account and amount
                    target_account.funds += amount
                    return self.account_dao.write(target_account)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
    
    def withdraw(self, current_username: str, account_id: int, amount: int) -> Account:
        """
        A customer makes a withdrawal from their own account.
        Fails and raises a ServiceException if:
            - the current user does not exist
            - the user is not a customer
            - the account does not exist
            - the user does not own the account
            - the account is not open/approved
            - the funds amount is not positive
            - there are not enough funds in the account for a withdrawal
            - there is a DAO exception
        """
        try:
            current_user: User = self.user_dao.find(current_username)
            if not current_user:
                raise ServiceException("User '" + current_username + "' not found.")
            elif current_user.level != UserLevel.CUSTOMER:
                raise ServiceException("Only CUSTOMERS can withdraw funds.")
            else:  # if user is valid
                target_account: Account = self.account_dao.find(account_id)
                if not target_account:
                    raise ServiceException("Account #" + str(account_id) + " not found.")
                elif target_account.owner_username != current_username:
                    raise ServiceException(
                            "You do not have permission to access Account #" 
                            + str(account_id))
                elif not target_account.is_approved:
                    raise ServiceException(
                            "Account #" + str(account_id) + " has not yet been approved.")
                elif amount <= 0:
                    raise ServiceException("You must withdraw a positive amount.")
                elif amount > target_account.funds:
                    raise ServiceException(
                        "Account #" + str(account_id) + " has insufficient funds.")
                else:  # valid user and account and amount
                    target_account.funds -= amount
                    return self.account_dao.write(target_account)
        except DAOException as e:
            raise ServiceException("DAOException: " + e.message)
        