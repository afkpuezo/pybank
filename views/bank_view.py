"""
Displays output and gets input

@author Andrew Curry
"""
from exceptions.service_exception import ServiceException
from services.user_service import UserService
from services.account_service import AccountService
from services.transaction_service import TransactionService
from enums.action_util import Action
from enums.action_util import action_to_string
from enums.user_level_util import UserLevel
from models.user import User


class BankView():
    """
    Displays output and gets input
    """
    
    # ----------
    # CONSTRUCTOR
    # ----------

    def __init__(
            self, 
            user_service: UserService, 
            account_service: AccountService, 
            transaction_service: TransactionService):
        self.user_service = user_service
        self.account_service = account_service
        self.transaction_service = transaction_service

    # ----------
    # VIEW METHODS
    # ----------

    def interact(self):
        print()
        print("----------")
        print("Welcome to PYBANK")
        print("----------")
        print()
        should_continue = True
        current_user: User = User("") # means logged out
        logged_out_choices: list[Action] = \
                [Action.REGISTER_USER, Action.LOG_IN, Action.QUIT]
        customer_choices: list[Action] = \
                [Action.OPEN_ACCOUNT, Action.DEPOSIT, Action.WITHDRAW, Action.TRANSFER,
                Action.LOG_OUT, Action.QUIT]
        admin_choices: list[Action] = \
                [Action.APPROVE_ACCOUNT, Action.VIEW_TRANSACTIONS, 
                Action.LOG_OUT, Action.QUIT]
        while should_continue:
            if current_user.username == "":
                print("----- LOGGED OUT -----")
                choices = logged_out_choices
            elif current_user.level == UserLevel.CUSTOMER:
                print("-----", current_user.username, "-----")
                choices = customer_choices
            else:
                print("-----", current_user.username, "-----")
                choices = admin_choices
            choice = self.get_user_choice(choices, "These are your available actions:")
            # big if chain to determine what to do
            try: # one try/except here rather than one in each method
                if choice == Action.REGISTER_USER:
                    current_user = self.register_user()
                elif choice == Action.LOG_IN:
                    current_user = self.log_in()
                elif choice == Action.LOG_OUT:
                    current_user = User("")
                elif choice == Action.OPEN_ACCOUNT:
                    pass
                elif choice == Action.DEPOSIT:
                    pass
                elif choice == Action.WITHDRAW:
                    pass
                elif choice == Action.TRANSFER:
                    pass
                elif choice == Action.VIEW_TRANSACTIONS:
                    pass
                elif choice == Action.APPROVE_ACCOUNT:
                    pass
                else: # quit
                    should_continue = False
            except ServiceException as e:
                print("There was a problem:", e.message)
        # end while loop
        print()
        print("----------")
        print("Goodbye!")
        print("----------")
        print()
    
    def register_user(self) -> User:
        username: str = input("Enter the new username: ")
        L: str = input("Type C for customer, A for admin: ")
        level: UserLevel = UserLevel.CUSTOMER if L == 'c' or L == 'C' else UserLevel.ADMIN
        return self.user_service.register_user(username, level)
    
    def log_in(self) -> User:
        username: str = input("Enter username: ")
        return self.user_service.log_in(username)

    # ----------
    # HELPER METHODS
    # ----------

    def get_user_choice(self, choices: list[Action], message: str) -> Action:
        """
        Prompts the user to pick one of the given choices.
        """
        print()
        print(message)
        print()
        for x in range(0, len(choices)):
            print(str(x + 1) + ": " + action_to_string(choices[x]))
        while True: # loop until we get valid input
            c: int = int(input("Make your selection:")) - 1
            if 0 <= c < len(choices):
                return choices[c]
            else:
                print("Invalid choice.")
    