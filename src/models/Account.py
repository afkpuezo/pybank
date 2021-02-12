"""
Instances of this class each model a single bank account

@author: Andrew Curry
"""


class Account():
    """
    Instances of this class each model a single bank account
    """

    def __init__(
            self, id: int = -1, 
            is_approved: bool = False, 
            owner_username: str = "", 
            funds: int = 0) -> None:
        """
        id defaults to -1
        is_approved defaults to False
        owner_username defaults to ""
        funds defaults to 0
        Does NOT validate params
        """
        self.id: int = id
        self.is_approved: bool = is_approved
        self.owner_username: str = owner_username
        self.funds: int = funds

    def __eq__(self, other):
        return isinstance(other, Account) \
                and self.id == other.id \
                and self.is_approved == other.is_approved \
                and self.owner_username == other.owner_username \
                and self.funds == other.funds

    # ----------
    # SERIALIZATION / DESERIALIZATION
    # ----------
    
    def encode(self) -> bytes:
        """
        Returns a bytes representation of this account.
        """
        code: str = str(id) \
                + " " + str(self.is_approved) \
                + " " + self.owner_username \
                + " " + str(self.funds)
        return code.encode()

    def decode(code: bytes):# -> Account:
        """
        Returns a new Account based on the information in the given bytes
        """
        vals: list[str] = str(bytes).split(' ')
        result: Account = Account()
        result.id = int(vals[0])
        result.is_approved = bool(vals[1])
        result.owner_username = vals[2]
        result.funds = int(vals[3])
        return result