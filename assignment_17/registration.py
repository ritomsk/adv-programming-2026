import re

class InvalidEmailError(ValueError):
    """Raised when an email string is null, empty, or incorrectly formatted."""
    pass

class UnderageError(ValueError):
    """Raised when a user does not meet the minimum age requirement."""
    pass


class RegistrationService:
    def __init__(self):
        self.system_ready = True 

    def register_user(self, email: str, age: int) -> bool:
        """
        Validates incoming user data and processes registration.
        
        :param email: The user's email address.
        :param age: The user's age.
        :return: True if registration is successful.
        """
        assert self.system_ready is True, "System Context Error: Registration service is currently down."
        
        if not email or not email.strip():
            raise InvalidEmailError("Registration failed: Email address cannot be empty.")
 
        email_pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[A-Za-z]{2,}$")
        if not email_pattern.match(email):
            raise InvalidEmailError(f"Registration failed: '{email}' is not a valid email format.")

        if age < 18:
            raise UnderageError(f"Registration failed: Applicant must be at least 18 (Provided age: {age}).")

        return True
    
if __name__ == "__main__":

    service = RegistrationService()

    try:
        result = service.register_user("9@9.999", 19)

        if result:
            print("Registraion successful")
    
    except (InvalidEmailError, UnderageError) as e:
        print(e)