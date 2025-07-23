import logging
from database import SessionLocal
from users.model import User

logger = logging.getLogger(__name__)


def get_user_by_email(email: str):
    """Get a user by email from the database."""
    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.email == email).first()
        return user
    except Exception as exc:
        logger.error(f"Error in get_user_by_email: {str(exc)}", exc_info=True)
        raise Exception("Failed to fetch user by email from the database.")


def get_user_by_phone_number(phone_number: str):
    """Get a user by phone number from the database."""
    try:
        with SessionLocal() as db:
            user = db.query(User).filter(User.phone_number == phone_number).first()
        return user
    except Exception as exc:
        logger.error(f"Error in get_user_by_phone_number: {str(exc)}", exc_info=True)
        raise Exception("Failed to fetch user by phone number from the database.")


def create_user(user_payload: dict) -> User:
    """Create a new user in the database."""
    try:
        with SessionLocal() as db:
            new_user = User(**user_payload)
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
        return new_user
    except Exception as exc:
        logger.error(f"Error in create_user: {str(exc)}", exc_info=True)
        raise Exception("Failed to create user in the database.")


def verify_user(user) -> User:
    """Verify a user in the database."""
    try:
        with SessionLocal() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
        return user
    except Exception as exc:
        logger.error(f"Error in verify_user: {str(exc)}", exc_info=True)
        raise Exception("Failed to verify user in the database.")


def update_password(user, password) -> User:
    """Update a user's password in the database."""
    try:
        with SessionLocal() as db:
            res = db.query(User).filter(User.email == user.email).first()
            if res:
                res.password = password  
                db.commit()
                db.refresh(res)
                return res
            else:
                logger.warning(f"User not found for password update: {user.email}")
                raise ValueError("User not found")
    except Exception as exc:
        logger.error(f"Error in update_password: {str(exc)}", exc_info=True)
        raise Exception("Failed to update user password in the database.")
