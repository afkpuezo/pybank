"""
Instances of this class each model a single recorded transaction
"""
from enums.ActionUtil import Action


class Transaction():
    """
    Instances of this class each model a single recorded transaction
    """

    def __init__(
            self,
            id: int = -1,
            time: int = 0,
            action: Action = Action.LOG_IN,
            acting_username: str = "",
            source_account_id: int = -1,
            destination_account_id: int = -1,
            funds_amount: int = 0) -> None:
        """
        id defaults to -1
        time defaults to 0
        action defaults to log in
        acting_username defaults to ""
        source_account_id defaults to -1
        destination_account_id defaults to -1
        funds_amount defaults to 0
        """
        self.id: int = id
        self.time: int = time
        self.action: Action = action
        self.acting_username: str = acting_username
        self.source_account_id: int = source_account_id
        self.destination_account_id: int = destination_account_id
        self.funds_amount: int = funds_amount