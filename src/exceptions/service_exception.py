"""
A custom exception thrown by Service classes.
"""

class ServiceException(Exception):
    """
    A custom exception thrown by Service classes.
    """   

    def __init__(self, message: str = "") -> None:
        self.message = message
        super().__init__()