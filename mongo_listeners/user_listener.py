"""
Listens for the UserDAOKafka to make requests and addresses them.

@author Andrew Curry
"""
from models.user import User
from kafka import KafkaProducer
from kafka import KafkaConsumer
import pymongo


class UserListener():
    """
    Listens for the UserDAOKafka to make requests and addresses them.
    """
    
    def listen(self):
        """
        Continually loops and waits for requests.
        """
        consumer = KafkaConsumer('bank_users')
        for message in consumer:
            tokens: list[str] = str(message).split(' ')
            method: str = list[0]
            if method == "write":
                self.write(tokens[1:])
            elif method == "find":
                self.find(tokens[1:])
    
    def write(self, args: list[str]):
        """
        Saves or updates the given user object
        """
        user: User = User.decode(args)
        myclient = pymongo.MongoClient()
        mydb = myclient["pybank"]
        mycol = mydb["users"]
        written_dict = mycol.insert_one(user.to_dict())
        written_user: User = User.from_dict(written_dict)
        producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
        producer.send('bank_user_reply', written_user.encode())
    
    def find(self, args: list[str]):
        """
        Returns the User object associated with the given username.
        Returns None if no such User is found.
        """
        username: str = list[0]
        myclient = pymongo.MongoClient()
        mydb = myclient["pybank"]
        mycol = mydb["users"]
        found_dict = mycol.find_one(username)
        if found_dict:
            message = User.from_dict(found_dict).encode
        else:
            message = str(None)
        producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
        producer.send('bank_user_reply', message)
        