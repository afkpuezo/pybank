"""
This file contains the Action enum and some functions to support it.
"""
from enum import Enum


# ----------
# ENUM
# ----------

class Action(Enum):
    REGISTER_USER = 0
    LOG_IN = 1
    LOG_OUT = 2
    OPEN_ACCOUNT = 3
    DEPOSIT = 4
    WITHDRAW = 5
    TRANSFER = 6
    VIEW_TRANSACTIONS = 7

# ----------
# FUNCTIONS (and helper variables)
# ----------


# used for util function
_action_to_string_dict: dict[Action, str] = {
    Action.REGISTER_USER : "Register a new user",
    Action.LOG_IN : "Log in",
    Action.LOG_OUT : "Log out",
    Action.OPEN_ACCOUNT : "Open a new account",
    Action.DEPOSIT : "Deposit funds",
    Action.WITHDRAW : "Withdraw funds",
    Action.TRANSFER : "Transfer funds",
    Action.VIEW_TRANSACTIONS : "View transaction history",
}


_string_to_action_dict: dict[str, Action] = {
    "Action.REGISTER_USER" : Action.REGISTER_USER,
    "Action.LOG_IN" : Action.LOG_IN,
    "Action.LOG_OUT" : Action.LOG_OUT,
    "Action.OPEN_ACCOUNT" : Action.OPEN_ACCOUNT,
    "Action.DEPOSIT" : Action.DEPOSIT,
    "Action.WITHDRAW" : Action.WITHDRAW,
    "Action.TRANSFER" : Action.TRANSFER,
    "Action.VIEW_TRANSACTIONS" : Action.VIEW_TRANSACTIONS,
}


# Action enum -> user-friendly string representation
def action_to_string(action: Action) -> str:
    return _action_to_string_dict[action]


# str(enum) -> enum
# NOT for the user-friendly string representation
def string_to_action(string: str) -> Action:
    return _string_to_action_dict[string]