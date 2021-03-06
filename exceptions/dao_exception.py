"""
A custom exception thrown by DAO classes.

@author: Andrew Curry
"""

class DAOException(Exception):
    """
    A custom exception thrown by DAO classes.
    """

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__()
