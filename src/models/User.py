"""
Instances of this class each model a single user profile

@author: Andrew Curry
"""
from enums.user_level_util import UserLevel
from enums.user_level_util import string_to_user_level


class User():
    """
    Instances of this class each model a single user profile.
    """

    def __init__(self, username: str = "", level: UserLevel = UserLevel.CUSTOMER) -> None:
        """
        username defaults to ""
        level defaults to customer
        Does NOT validate params.
        """
        self.username: str = username
        self.level: UserLevel = level
    
    def __eq__(self, other):
        return isinstance(other, User) \
                and self.username == other.username \
                and self.level == other.level
    
    # ----------
    # SERIALIZATION / DESERIALIZATION
    # ----------

    def encode(self) -> bytes:
        """
        Returns a bytes representation of this user.
        """
        code: str = self.username + " " + str(self.level)
        return code.encode()

    def decode(code: bytes):# -> User:
        """
        Returns a new user based on the information in the given bytes
        """
        vals: list[str] = str(bytes).split(' ')
        result: User = User()
        result.username = vals[0]
        result.level = string_to_user_level(vals[1])