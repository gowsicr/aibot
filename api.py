import enum
import random
import string
from typing import Annotated
from livekit.agents import llm
import logging

logger = logging.getLogger("password-reset")
logger.setLevel(logging.INFO)

class Users(enum.Enum):
    USER1 = "user1"
    USER2 = "user2"
    USER3 = "user3"

class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        # Predefined user passwords (these should be stored securely in a real application)
        self._user_passwords = {
            Users.USER1: "password123",
            Users.USER2: "securepass456",
            Users.USER3: "mypassword789",
        }

    def _generate_temp_password(self):
        """Generate a random temporary password."""
        temp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return temp_pass

    @llm.ai_callable(description="Reset the password for a specific user")
    def reset_password(
        self, 
        username: Annotated[str, llm.TypeInfo(description="The username to reset the password for")]
    ):
        user_enum = Users[username.upper()] if username.upper() in Users.__members__ else None
        if user_enum and user_enum in self._user_passwords:
            temp_pass = self._generate_temp_password()
            self._user_passwords[user_enum] = temp_pass  # Update with the temporary password
            logger.info("Password reset for user %s", username)
            return f"Hi {username}, your password has been reset. Your temporary password is: {temp_pass}"
        else:
            return f"Sorry, I could not find a user with the name '{username}'. Please check and try again."

    @llm.ai_callable(description="Check the current password for a user (debugging purposes)")
    def check_password(
        self, 
        username: Annotated[str, llm.TypeInfo(description="The username to check the password for")]
    ):
        user_enum = Users[username.upper()] if username.upper() in Users.__members__ else None
        if user_enum and user_enum in self._user_passwords:
            current_password = self._user_passwords[user_enum]
            logger.info("Password retrieved for user %s", username)
            return f"The current password for {username} is: {current_password}"
        else:
            return f"User '{username}' not found."
