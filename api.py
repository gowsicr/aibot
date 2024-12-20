import enum
import random
import string
import uuid
import logging
from typing import Annotated
from livekit.agents import llm

logger = logging.getLogger("voice-assistant")
logger.setLevel(logging.INFO)

class Users(enum.Enum):
    MANO_RANJIT_KUMAR = "Mano Ranjit Kumar"
    ADMIN = "admin"

class AssistantFnc(llm.FunctionContext):
    def __init__(self) -> None:
        super().__init__()

        # Predefined user passwords (these should be stored securely in a real application)
        self._user_passwords = {
            Users.MANO_RANJIT_KUMAR: "password123",
            Users.ADMIN: "securepass456",
        }

    def _generate_temp_password(self):
        """Generate a random temporary password."""
        temp_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        return temp_pass

    def _generate_ticket_id(self):
        """Generate a unique ticket ID."""
        return str(uuid.uuid4())

    @llm.ai_callable(description="Reset the password for a specific user")
    def reset_password(
        self, 
        username: Annotated[str, llm.TypeInfo(description="The username to reset the password for")]
    ):
        user_enum = Users[username.upper().replace(" ", "_")] if username.upper().replace(" ", "_") in Users.__members__ else None
        if user_enum and user_enum in self._user_passwords:
            temp_pass = self._generate_temp_password()
            self._user_passwords[user_enum] = temp_pass  # Update with the temporary password
            logger.info("Password reset for user %s", username)
            return f"Hi {username}, your password has been reset. Your temporary password is: {temp_pass}"
        else:
            return f"Sorry, I could not find a user with the name '{username}'. Please check and try again."

    @llm.ai_callable(description="Report printer issue")
    def printer_access(
        self,
        username: Annotated[str, llm.TypeInfo(description="The username to verify")]
    ):
        """
        Verify user existence and log printer issue report.
        """
        logger.info("Printer issue reported by username: %s", username)

        # Normalize the username input
        normalized_username = username.strip().lower()

        # Verify the username against defined users in a case-insensitive manner
        if normalized_username == "mano ranjit kumar" or normalized_username == "admin":
            return f"Your printer issue has been recorded. You will be redirected to our support agent. Thank you."
        
        return f"Sorry, I couldn't verify your identity, {username}. Please contact your administrator."

    @llm.ai_callable(description="Grant access for ZIF application")
    def grant_access_zif(
        self,
        username: Annotated[str, llm.TypeInfo(description="The username to grant access for")]
    ):
        """
        Grant access for ZIF application if the user exists.
        """
        logger.info("Access request for ZIF application by username: %s", username)

        # Normalize the username input
        normalized_username = username.strip().lower()

        if normalized_username == "mano ranjit kumar" or normalized_username == "admin":
            ticket_id = self._generate_ticket_id()
            return f"Your request to grant access for ZIF application is being processed. Here is your ticket ID: {ticket_id}"
        
        return f"Sorry, I couldn't verify your identity, {username}. Please contact your administrator."
