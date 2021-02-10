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
    account_service.user_dao.find.return_value = User
    account_service.account_dao.write.return_value = expected_account
    result_account: Account = account_service.open_account(user)
    assert result_account == expected_account


def test_open_account_user_not_found(account_service: AccountService):
    """
    Should not be able to open an account with a user that does not exist
    """
    with pytest.raises(ServiceException):
        user: User = User("test")
        account_service.user_dao.find.return_value = None
        account_service.open_account(user)


def test_open_account_as_admin(account_service: AccountService):
    """
    Should not be able to open an account with an admin
    """
    with pytest.raises(ServiceException):
        user: User = User("test", UserLevel.ADMIN)
        account_service.user_dao.find.return_value = User
        account_service.open_account(user)