from daos.interfaces.user_dao import UserDAO
from models.user import User
from daos.impls.transaction_dao_impl import TransactionDAOImpl
from daos.impls.account_dao_impl import AccountDAOImpl
from daos.impls.user_dao_impl import UserDAOImpl
from services.account_service import AccountService
from services.transaction_service import TransactionService
from services.user_service import UserService
from views.bank_view import BankView

udi = UserDAOImpl()
adi = AccountDAOImpl()
tdi = TransactionDAOImpl()
user_service: UserService = UserService(udi)
account_service: AccountService = AccountService(adi, udi)
transaction_service: TransactionService = TransactionService(tdi, adi, udi)
view: BankView = BankView(user_service, account_service, transaction_service)
view.interact()