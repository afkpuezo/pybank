"""
Instances of this class each model a single user profile
"""
from enums.UserLevelUtil import UserLevel


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