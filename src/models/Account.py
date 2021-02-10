"""
Instances of this class each model a single bank account

@author: Andrew Curry
"""


class Account():
    """
    Instances of this class each model a single bank account
    """

    def __init__(self, id: int = -1, owner_username: str = "", funds: int = 0) -> None:
        """
        id defaults to -1
        owner_username defaults to ""
        funds defaults to 0
        Does NOT validate params
        """
        self.id: int = id
        self.owner_username: str = owner_username
        self.funds: int = funds

    def __eq__(self, other):
        return isinstance(other, Account) \
                and self.id == other.id \
                and self.owner_username == other.owner_username \
                and self.funds == other.funds