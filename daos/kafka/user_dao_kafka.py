"""
Implements UserDAO by using kafka to communicate with another app that communicates with
the database.

@author Andrew Curry
"""
from daos.interfaces.user_dao import UserDAO
from models.user import User
from exceptions.dao_exception import DAOException
from kafka import KafkaProducer
from kafka import KafkaConsumer


class UserDAOKafka(UserDAO):
    """
    Implements UserDAO by using kafka to communicate with another app that communicates with    
    the database.
    """
    
    def write(self, user: User) -> User:
        """
        Saves or updates the given user object
        Raises DAOException if there is a problem with the database.
        """
        try:
            producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
            producer.send('bank_users', b'write ' + user.encode())
            consumer = KafkaConsumer('bank_users_reply')
            for message in consumer:
                return User.encode(message)
        except Exception as e:
            raise DAOException("There as a problem in UserDAOKafka.write")
    
    def find(self, username: str) -> User:
        """
        Returns the User object associated with the given username.
        Returns None if no such User is found.
        Raises DAOException if there is a problem with the database.
        """
        try:
            producer = KafkaProducer(bootstrap_servers = 'localhost:9092')
            producer.send('bank_users', b'find ' + username)
            consumer = KafkaConsumer('bank_users_reply')
            for message in consumer:
                return User.encode(message)
        except Exception as e:
            raise DAOException("There as a problem in UserDAOKafka.find")