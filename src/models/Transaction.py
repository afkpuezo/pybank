"""
Instances of this class each model a single recorded transaction

@author: Andrew Curry
"""
from enums.action_util import Action


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