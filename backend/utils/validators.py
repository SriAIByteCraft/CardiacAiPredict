"""
Input Validation Utilities for Authentication, Registration, and Medical Profile updates.
"""
import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

def is_valid_email(email: str) -> bool:
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))

def is_strong_password(password: str) -> tuple[bool, str]:
    if not password or not isinstance(password, str):
        return False, "Password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit (0-9)."
    if not any(char.isalpha() for char in password):
        return False, "Password must contain at least one letter."
    return True, ""

def validate_registration(payload: dict) -> tuple[bool, str, dict]:
    if not isinstance(payload, dict):
        return False, "Request body must be a JSON object.", {}

    name = str(payload.get("name", "")).strip()
    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))
    confirm_password = str(payload.get("confirm_password", ""))

    if not name or len(name) < 2:
        return False, "Full name must be at least 2 characters long.", {}
    
    if not is_valid_email(email):
        return False, "Please provide a valid email address.", {}

    valid_pass, pass_msg = is_strong_password(password)
    if not valid_pass:
        return False, pass_msg, {}

    if confirm_password and password != confirm_password:
        return False, "Passwords do not match.", {}

    return True, "", {"name": name, "email": email, "password": password}

def validate_login(payload: dict) -> tuple[bool, str, dict]:
    if not isinstance(payload, dict):
        return False, "Request body must be a JSON object.", {}

    email = str(payload.get("email", "")).strip().lower()
    password = str(payload.get("password", ""))

    if not email or not is_valid_email(email):
        return False, "Please enter a valid email address.", {}

    if not password:
        return False, "Password is required.", {}

    return True, "", {"email": email, "password": password}

def validate_password_change(payload: dict) -> tuple[bool, str, dict]:
    if not isinstance(payload, dict):
        return False, "Request body must be a JSON object.", {}

    current_password = str(payload.get("current_password", ""))
    new_password = str(payload.get("new_password", ""))
    confirm_new_password = str(payload.get("confirm_new_password", ""))

    if not current_password:
        return False, "Current password is required.", {}

    valid_pass, pass_msg = is_strong_password(new_password)
    if not valid_pass:
        return False, f"New password invalid: {pass_msg}", {}

    if confirm_new_password and new_password != confirm_new_password:
        return False, "New passwords do not match.", {}

    if current_password == new_password:
        return False, "New password cannot be identical to current password.", {}

    return True, "", {"current_password": current_password, "new_password": new_password}
