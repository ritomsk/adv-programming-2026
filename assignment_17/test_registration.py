import pytest
from assignment_17.registration import RegistrationService, InvalidEmailError, UnderageError

@pytest.fixture
def service():
    """Provides a fresh instance of RegistrationService for each test."""
    return RegistrationService()

def test_successful_registration(service):
    """Validates that a correct email and valid age return True."""
    result = service.register_user("newuser@example.com", 25)
    assert result is True

def test_empty_email_raises_error(service):
    """Validates that empty strings trigger an InvalidEmailError."""
    with pytest.raises(InvalidEmailError, match="Email address cannot be empty"):
        service.register_user("", 22)

def test_whitespace_email_raises_error(service):
    """Validates that whitespace-only strings trigger an InvalidEmailError."""
    with pytest.raises(InvalidEmailError, match="Email address cannot be empty"):
        service.register_user("   ", 22)

def test_malformed_email_raises_error(service):
    """Validates that emails lacking an @ or domain trigger an InvalidEmailError."""
    bad_emails = ["userexample.com", "user@.com", "user@domain", "@domain.com"]
    
    for bad_email in bad_emails:
        with pytest.raises(InvalidEmailError, match="is not a valid email format"):
            service.register_user(bad_email, 30)

def test_underage_applicant_raises_error(service):
    """Validates that an age under 18 triggers an UnderageError."""
    with pytest.raises(UnderageError, match="Applicant must be at least 18"):
        service.register_user("youngling@example.com", 17)

def test_system_inactive_assertion(service):
    """Validates the internal system context assertion."""
    service.system_ready = False
    
    with pytest.raises(AssertionError, match="Registration service is currently down"):
        service.register_user("user@example.com", 20)