"""
Contains unit tests for the TransactionService class.

@author: Andrew Curry
"""
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
    transaction_service: TransactionService = TransactionService(TransactionDAO())
    mocker.patch.object(transaction_service, 'transaction_dao')
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