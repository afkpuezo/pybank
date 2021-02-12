from daos.impls.account_dao_impl import AccountDAOImpl
from models.account import Account
from enums.user_level_util import UserLevel
import pymongo

pymongo.MongoClient().drop_database("pybank")
impl: AccountDAOImpl = AccountDAOImpl()
id_1: int = impl.write(Account(owner_username = "customer", funds = 1)).id
impl.write(Account(owner_username = "customer", funds = 2))
impl.write(Account(owner_username = "customer", funds = 3))
impl.write(Account(owner_username = "customer2", funds = 4))
impl.write(Account(owner_username = "customer2", funds = 5))
found: Account = impl.find(id_1)
print("found with id_1:", found)