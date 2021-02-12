import pymongo
from daos.interfaces.user_dao import UserDAO
from daos.kafka.user_dao_kafka import UserDAOKafka
from models.user import User


def main():
    pymongo.MongoClient().drop_database("pybank")
    dao : UserDAO = UserDAOKafka()
    result: User = dao.write(User("testguy"))
    print("write result:" + str(result.encode()))


if __name__ == "__main__":
    main()