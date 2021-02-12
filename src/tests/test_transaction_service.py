"""
Contains unit tests for the TransactionService class.

@author: Andrew Curry
"""
from datetime import datetime
from daos.interfaces.account_dao import AccountDAO
from daos.interfaces.user_dao import UserDAO
from enums.user_level_util import UserLevel
from models.account import Account
from models.user import User
from services.transaction_service import TransactionService
from daos.interfaces.transaction_dao import TransactionDAO
from models.transaction import Transaction
from exceptions.dao_exception import DAOException
from exceptions.service_exception import ServiceException
import pytest
from pytest_mock import mocker


# ----------
# SETUP
# ----------


@pytest.fixture
def transaction_service(mocker):
    transaction_service: TransactionService = TransactionService(
            TransactionDAO(), 
            AccountDAO(),
            UserDAO())
    mocker.patch.object(transaction_service, 'transaction_dao')
    mocker.patch.object(transaction_service, 'account_dao')
    mocker.patch.object(transaction_service, 'user_dao')
    return transaction_service


# ----------
# TESTS
# ----------


# -----
# record TESTS
# -----


def test_record(transaction_service: TransactionService):
    """
    Should be able to record a transaction into the database.
    Will also check to see if the transaction's timestamp has been updated.
    """
    tx: Transaction = Transaction() # default values should be fine
    transaction_service.transaction_dao.write.return_value = tx
    result: Transaction = transaction_service.record(tx)
    assert result
    assert result.time > 0


def test_record_dao_exception(transaction_service: TransactionService):
    """
    Should raise a service exception if there is a problem with the dao.
    """
    with pytest.raises(ServiceException):
        tx: Transaction = Transaction() # default values should be fine
        transaction_service.transaction_dao.write.side_effect = DAOException("test")
        transaction_service.record(tx)


# -----
# find_by_account TESTS
# -----


def test_find_by_account(transaction_service: TransactionService):
    """
    Should be able to find all tx's involving a given account.
    """
    current_username: str = "admin"
    current_user: User = User(current_username, UserLevel.ADMIN)
    target_account_id: int = 1
    target_account: Account = Account(target_account_id, True, "customer", 1234)
    txs: list[Transaction] = []  # a dummy list of transactions to return
    for x in range(0, 3):
        tx: Transaction = Transaction(source_account_id=target_account_id)
        txs.append(tx)
        tx = Transaction(destination_account_id=target_account_id)
        txs.append(tx)
    transaction_service.user_dao.find.return_value = current_user
    transaction_service.account_dao.find.return_value = target_account
    transaction_service.transaction_dao.find_by_account.return_value = txs
    result_list: list[Transaction] = \
            transaction_service.find_by_account(current_username, target_account_id)
    assert result_list == txs


def test_find_by_account_user_not_found(transaction_service: TransactionService):
    """
    Shouldn't be able to find tx's with a user that doesn't exist
    """
    with pytest.raises(ServiceException):
        transaction_service.user_dao.find.return_value = None
        transaction_service.find_by_account("test", 1)


def test_find_by_account_user_customer(transaction_service: TransactionService):
    """
    Shouldn't be able to find tx's with a user that doesn't exist
    """
    with pytest.raises(ServiceException):
        transaction_service.user_dao.find.return_value = User("customer")
        transaction_service.find_by_account("test", 1)


def test_find_by_account_account_not_found(transaction_service: TransactionService):
    """
    Should be able to find all tx's involving a given account.
    """
    with pytest.raises(ServiceException):
        current_username: str = "admin"
        current_user: User = User(current_username, UserLevel.ADMIN)
        transaction_service.user_dao.find.return_value = current_user
        transaction_service.account_dao.find.return_value = None
        transaction_service.find_by_account(current_username, 1)


def test_find_by_account_dao_exception(transaction_service: TransactionService):
    """
    Should raise a service exception when there is a dao exception
    """
    with pytest.raises(ServiceException):
        transaction_service.user_dao.find.side_effect = DAOException("test")
        transaction_service.find_by_account("test", 1)


# -----
# find_all_in_last_hour TESTS
# -----


def test_find_all_in_last_hour(transaction_service: TransactionService):
    """
    Should be able to find some tx's
    """
    txs: list[Transaction] = []  # a dummy list of transactions to return
    for x in range(0, 3):
        tx: Transaction = Transaction()
        tx.time = datetime.timestamp(datetime.now()) - 250
        txs.append(tx)
    transaction_service.transaction_dao.find_after_time.return_value = txs
    result_list: list[Transaction] = transaction_service.find_all_in_last_hour()
    assert result_list == txs


def test_find_all_in_last_hour_dao_exception(transaction_service: TransactionService):
    """
    Should raise a service exception when there is a dao exception
    """
    with pytest.raises(ServiceException):
        transaction_service.transaction_dao.find_after_time.side_effect \
                = DAOException("test")
        result_list: list[Transaction] = transaction_service.find_all_in_last_hour()
