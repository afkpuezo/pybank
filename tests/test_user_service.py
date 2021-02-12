"""
Contains unit tests for the UserService class.

@author: Andrew Curry
"""
#import mock
import pytest # not sure what's up with this
from pytest_mock import mocker

from daos.interfaces.user_dao import UserDAO
from services.user_service import UserService
from models.user import User
from enums.user_level_util import UserLevel
from exceptions.service_exception import ServiceException
from exceptions.dao_exception import DAOException

# ----------
# SETUP
# ----------


@pytest.fixture
def user_service(mocker) -> UserService:
    user_service: UserService = UserService(UserDAO())
    mocker.patch.object(user_service, 'user_dao')
    return user_service


# ----------
# TESTS
# ----------


# -----
# register_user TESTS
# -----


def test_register_user(user_service: UserService):
    """
    Should be able to register a new user
    """
    user: User = User("test", UserLevel.CUSTOMER)
    user_service.user_dao.find.return_value = False
    user_service.user_dao.write.return_value = user
    result: User = user_service.register_user("test", UserLevel.CUSTOMER)
    assert result == user


def test_register_user_already_exists(user_service: UserService):
    """
    Shouldn't be able to register a user that already exists
    """
    with pytest.raises(ServiceException):
        user: User = User("test", UserLevel.CUSTOMER)
        user_service.user_dao.find.return_value = True
        user_service.register_user("test", UserLevel.CUSTOMER)


def test_register_user_dao_exception(mocker, user_service: UserService):
    """
    Should raise a ServiceException when there's a DAOException
    """
    with pytest.raises(ServiceException):
        user_service.user_dao.find.side_effect = DAOException("test")
        user: User = User("test", UserLevel.CUSTOMER)
        user_service.user_dao.find.return_value = True
        user_service.register_user("test", UserLevel.CUSTOMER)


# -----
# log_in TESTS
# -----


def test_log_in(user_service: UserService):
    """
    Should be able to log in to a user profile that exists
    """
    username: str = "test"
    user: User = User(username, UserLevel.CUSTOMER)
    user_service.user_dao.find.return_value = user
    result: User = user_service.log_in(username)
    assert result == user


def test_log_in_not_found(user_service: UserService):
    """
    Should not be able to log in to a user profile that doesn't exist
    """
    username: str = "test"
    user_service.user_dao.find.return_value = None
    assert user_service.log_in(username) == None


def test_log_in_dao_exception(user_service: UserService):
    """
    Should raise a service exception if there is a dao exception
    """
    with pytest.raises(ServiceException):
        username: str = "test"
        user_service.user_dao.find.side_effect = DAOException("test")
        user_service.log_in(username)