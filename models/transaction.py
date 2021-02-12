"""
Instances of this class each model a single recorded transaction

@author: Andrew Curry
"""
from enums.action_util import Action
from enums.action_util import string_to_action


class Transaction():
    """
    Instances of this class each model a single recorded transaction
    """

    def __init__(
            self,
            id: int = -1,
            time: int = 0,
            action: Action = Action.LOG_IN,
            was_success: bool = True,
            acting_username: str = "",
            source_account_id: int = -1,
            destination_account_id: int = -1,
            funds_amount: int = 0) -> None:
        """
        id defaults to -1
        time defaults to 0
        was_success: bool = True
        action defaults to log in
        acting_username defaults to ""
        source_account_id defaults to -1
        destination_account_id defaults to -1
        funds_amount defaults to 0
        """
        self.id: int = id
        self.time: int = time
        self.action: Action = action
        self.was_success: bool = was_success
        self.acting_username: str = acting_username
        self.source_account_id: int = source_account_id
        self.destination_account_id: int = destination_account_id
        self.funds_amount: int = funds_amount
    
    def __eq__(self, other):
        return isinstance(other, Transaction) \
                and self.id == other.id \
                and self.time == other.time \
                and self.action == other.action \
                and self.was_success == other.was_success \
                and self.acting_username == other.acting_username \
                and self.source_account_id == other.source_account_id \
                and self.destination_account_id == other.destination_account_id \
                and self.funds_amount == other.funds_amount
    
    # ----------
    # SERIALIZATION / DESERIALIZATION
    # ----------

    def encode(self) -> bytes:
        """
        Returns a bytes representation of this transaction.
        """
        code: str = str(self.id) + " " \
                + str(self.time) + " " \
                + str(self.action) + " " \
                + str(self.was_success) + " " \
                + self.acting_username + " " \
                + str(self.source_account_id) + " " \
                + str(self.destination_account_id) + " " \
                + str(self.funds_amount)
        return code.encode()
    
    def decode(code: bytes):# -> Transaction:
        """
        Returns a new tx based on the information in the given bytes
        """
        vals: list[str] = str(bytes).split(' ')
        result: Transaction = Transaction()
        result.id = int(vals[0])
        result.time = int(vals[1])
        result.action = string_to_action(vals[2])
        result.acting_username = vals[3]
        result.source_account_id = int(vals[4])
        result.destination_account_id = int(vals[5])
        result.funds_amount = int(vals[6])
        return result

    def to_dict(self) -> dict:
        """
        Returns a dict representation of this transaction.
        """
        d: dict = {
            "time" : self.time,
            "action" : str(self.action),
            "acting_username" : self.acting_username,
            "source_account_id" : self.source_account_id,
            "destination_account_id" : self.destination_account_id,
            "funds_amount" : self.funds_amount,
        }
        if self.id != -1:
            d["_id"] = self.id
        return d
    
    def from_dict(d: dict):
        """
        Returns a new tx based on the information in the given dicts
        """
        result: Transaction = Transaction()
        result.id = int(d["_id"])
        result.time = int(d["time"])
        result.action = string_to_action(d["action"])
        result.acting_username = d["acting_username"]
        result.source_account_id = int(d["source_account_id"])
        result.destination_account_id = int(d["destination_account_id"])
        result.funds_amount = int(d["funds_amount"])
        return result

