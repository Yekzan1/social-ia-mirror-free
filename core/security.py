import bcrypt
import re
import secrets

def validate_email(email: str) -> bool:
    """Strict email validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password_strength(password: str) -> tuple[bool, str]:
    """Validate password strength (min 8 chars, 1 uppercase, 1 digit)."""
    if len(password) < 8:
        return False, "Le mot de passe doit faire au moins 8 caractères."
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule."
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre."
    return True, ""

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def generate_session_token() -> str:
    """Generate a secure random session token."""
    return secrets.token_urlsafe(32)
