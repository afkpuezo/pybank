"""
This file contains the UserLevel enum and some functions to support it.
"""
from enum import Enum


# ----------
# ENUM
# ----------


class UserLevel(Enum):
    CUSTOMER = 0
    ADMIN = 1


# ----------
# FUNCTIONS (and helper variables)
# ----------


_user_level_to_string_dict : dict = {
    UserLevel.CUSTOMER : "Customer",
    UserLevel.ADMIN : "Admin",
}


_string_to_user_level_dict : dict = {
    "UserLevel.CUSTOMER" : UserLevel.CUSTOMER,
    "UserLevel.ADMIN" : UserLevel.ADMIN,
}


def user_level_to_string(user_level: UserLevel) -> str:
    """
    enum -> user-friendly string representation
    """
    return _user_level_to_string_dict[user_level]


def string_to_user_level(string: str) -> UserLevel:
    """
    str(enum) -> enum - NOT for user-friendly strings!
    """
    return _string_to_user_level_dict[string]