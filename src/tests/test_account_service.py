"""
Contains unit tests for the AccountService class.

@author: Andrew Curry
"""
from daos.interfaces.user_dao import UserDAO
from enums.user_level_util import UserLevel
from exceptions.dao_exception import DAOException
from exceptions.service_exception import ServiceException
import pytest
from pytest_mock import mocker

from services.account_service import AccountService
from daos.interfaces.account_dao import AccountDAO
from models.user import User
from models.account import Account


# ----------
# SETUP
# ----------


@pytest.fixture
def account_service(mocker):
    account_service: AccountService = AccountService(AccountDAO(), UserDAO())
    mocker.patch.object(account_service, 'account_dao')
    mocker.patch.object(account_service, 'user_dao')
    return account_service


# ----------
# TESTS
# ----------


# -----
# open_account TESTS
# -----


def test_open_account(account_service: AccountService):
    """
    Should be able to open an account with a customer
    """
    user: User = User("test")
    expected_account: Account = Account(owner_username = "test")
    account_service.user_dao.find.return_value = user
    account_service.account_dao.write.return_value = expected_account
    result_account: Account = account_service.open_account("test")
    assert result_account == expected_account


def test_open_account_user_not_found(account_service: AccountService):
    """
    Should not be able to open an account with a user that does not exist
    """
    with pytest.raises(ServiceException):
        user: User = User("test")
        account_service.user_dao.find.return_value = None
        account_service.open_account("test")


def test_open_account_as_admin(account_service: AccountService):
    """
    Should not be able to open an account with an admin
    """
    with pytest.raises(ServiceException):
        user: User = User("test", UserLevel.ADMIN)
        account_service.user_dao.find.return_value = user
        account_service.open_account("test")


# -----
# approve_account TESTS
# -----


def test_approve_account(account_service: AccountService):
    """
    Should be able to have an admin approve a pending account.
    """
    current_user: User = User("admin", UserLevel.ADMIN)
    target_account: Account = Account(id = 1) # default values should be good?
    account_service.user_dao.find.return_value = current_user
    account_service.account_dao.find.return_value = target_account
    result_account: Account = account_service.approve_account("admin", 1)
    assert result_account.is_approved and result_account.id == target_account.id


def test_approve_account_user_not_found(account_service: AccountService):
    """
    Should not be able to approve an account if the current user does not exist
    """
    with pytest.raises(ServiceException):
        account_service.user_dao.find.return_value = None
        account_service.approve_account("admin", 1)


def test_approve_account_user_not_admin(account_service: AccountService):
    """
    Should not be able to approve an account if the current user is a customer
    """
    with pytest.raises(ServiceException):
        current_user: User = User("customer", UserLevel.CUSTOMER)
        account_service.user_dao.find.return_value = current_user
        account_service.approve_account("admin", 1)


def test_approve_account_account_not_found(account_service: AccountService):
    """
    Should not be able to approve an account if the account is not found
    """
    with pytest.raises(ServiceException):
        current_user: User = User("admin", UserLevel.ADMIN)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = None
        account_service.approve_account("admin", 1)


def test_approve_account_account_not_found(account_service: AccountService):
    """
    Should not be able to approve an account if the account is already approved
    """
    with pytest.raises(ServiceException):
        current_user: User = User("admin", UserLevel.ADMIN)
        target_account: Account = Account(id = 1, is_approved = True)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.approve_account("admin", 1)


# -----
# deposit TESTS
# -----


def test_deposit(account_service: AccountService):
    """
    A customer should be able to deposit money into their own account.
    """
    current_username: str = "customer"
    account_id: int = 1
    amount: int = 10000
    initial_funds: int = 123456
    current_user: User = User(current_username)
    target_account: Account = Account(1, True, current_username, initial_funds)
    account_service.user_dao.find.return_value = current_user
    account_service.account_dao.find.return_value = target_account
    account_service.account_dao.write.return_value = target_account
    result_account: Account = \
            account_service.deposit(current_username, account_id, amount)
    assert result_account.id == target_account.id
    assert result_account.funds == initial_funds + amount


def test_deposit_user_not_found(account_service: AccountService):
    """
    Should not be able to deposit with a user that doesn't exist.
    """
    with pytest.raises(ServiceException):
        account_service.user_dao.find.return_value = None
        account_service.deposit("customer", 1, 10000)


def test_deposit_user_not_customer(account_service: AccountService):
    """
    Should not be able to deposit with an admin
    """
    with pytest.raises(ServiceException):
        current_username: str = "admin"
        current_user: User = User(current_username, UserLevel.ADMIN)
        account_service.user_dao.find.return_value = current_user
        account_service.deposit(current_username, 1, 1)


def test_deposit_account_not_found(account_service: AccountService):
    """
    Should not be able to deposit into an account that does not exist
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        current_user: User = User(current_username)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = None
        account_service.deposit(current_username, 1, 1)


def test_deposit_account_not_approved(account_service: AccountService):
    """
    Should not be able to deposit into an account that has not been approved yet
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        account_id: int = 1
        amount: int = 10000
        initial_funds: int = 123456
        current_user: User = User(current_username)
        target_account: Account = Account(1, False, current_username, initial_funds)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.deposit(current_username, account_id, amount)


def test_deposit_negative_funds(account_service: AccountService):
    """
    Should not be able to make a negative deposit
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        account_id: int = 1
        amount: int = -10000
        initial_funds: int = 123456
        current_user: User = User(current_username)
        target_account: Account = Account(1, True, current_username, initial_funds)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.account_dao.write.return_value = target_account
        account_service.deposit(current_username, account_id, amount)


def test_deposit_dao_exception(account_service: AccountService):
    """
    Should raise a service exception when there is a dao exception
    """
    with pytest.raises(ServiceException):
        account_service.user_dao.find.side_effects = DAOException("test")
        account_service.deposit("test", 1, 1)


# -----
# withdraw TESTS
# -----


def test_withdraw(account_service: AccountService):
    """
    A customer should be able to make a withdrawal from their own account.
    """
    current_username: str = "customer"
    account_id: int = 1
    amount: int = 10000
    initial_funds: int = 123456
    current_user: User = User(current_username)
    target_account: Account = Account(1, True, current_username, initial_funds)
    account_service.user_dao.find.return_value = current_user
    account_service.account_dao.find.return_value = target_account
    account_service.account_dao.write.return_value = target_account
    result_account: Account = \
            account_service.withdraw(current_username, account_id, amount)
    assert result_account.id == target_account.id
    assert result_account.funds == initial_funds - amount


def test_withdraw_user_not_found(account_service: AccountService):
    """
    Should not be able to withdraw with a user that doesn't exist.
    """
    with pytest.raises(ServiceException):
        account_service.user_dao.find.return_value = None
        account_service.withdraw("customer", 1, 10000)


def test_withdraw_user_not_customer(account_service: AccountService):
    """
    Should not be able to withdraw with an admin
    """
    with pytest.raises(ServiceException):
        current_username: str = "admin"
        current_user: User = User(current_username, UserLevel.ADMIN)
        account_service.user_dao.find.return_value = current_user
        account_service.withdraw(current_username, 1, 1)


def test_withdraw_account_not_found(account_service: AccountService):
    """
    Should not be able to withdraw into an account that does not exist
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        current_user: User = User(current_username)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = None
        account_service.withdraw(current_username, 1, 1)


def test_withdraw_account_not_approved(account_service: AccountService):
    """
    Should not be able to withdraw into an account that has not been approved yet
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        account_id: int = 1
        amount: int = 10000
        initial_funds: int = 123456
        current_user: User = User(current_username)
        target_account: Account = Account(1, False, current_username, initial_funds)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.withdraw(current_username, account_id, amount)


def test_withdraw_negative_funds(account_service: AccountService):
    """
    Should not be able to make a negative withdraw
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        account_id: int = 1
        amount: int = -10000
        initial_funds: int = 123456
        current_user: User = User(current_username)
        target_account: Account = Account(1, True, current_username, initial_funds)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.account_dao.write.return_value = target_account
        account_service.withdraw(current_username, account_id, amount)


def test_withdraw_overdraft(account_service: AccountService):
    """
    Should not be able to withdraw more money than exists in the account
    """
    with pytest.raises(ServiceException):
        current_username: str = "customer"
        account_id: int = 1
        amount: int = 1001
        initial_funds: int = 1000
        current_user: User = User(current_username)
        target_account: Account = Account(1, True, current_username, initial_funds)
        account_service.user_dao.find.return_value = current_user
        account_service.account_dao.find.return_value = target_account
        account_service.account_dao.write.return_value = target_account
        account_service.withdraw(current_username, account_id, amount)


def test_withdraw_dao_exception(account_service: AccountService):
    """
    Should raise a service exception when there is a dao exception
    """
    with pytest.raises(ServiceException):
        account_service.user_dao.find.side_effects = DAOException("test")
        account_service.withdraw("test", 1, 1)