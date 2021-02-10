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


def test_register_user(user_service: UserService):
    user: User = User("test", UserLevel.CUSTOMER)
    user_service.user_dao.find.return_value = False
    user_service.user_dao.write.return_value = user
    result: User = user_service.register_user(user)
    assert result == user