from models.user import User
from enums.user_level_util import UserLevel

print("WHY")
user: User = User("admin", UserLevel.ADMIN)
print(str(user.encode()))