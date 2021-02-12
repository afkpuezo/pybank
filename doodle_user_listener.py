import pymongo
from mongo_listeners.user_listener import UserListener


def main():
    pymongo.MongoClient().drop_database("pybank")
    listener: UserListener = UserListener()
    listener.listen()


if __name__ == "__main__":
    main()