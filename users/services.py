import logging
from users.schema import SignupRequest
from fastapi import HTTPException
from users import repository
from users.utils import (
    get_password_hash,
    create_access_token,
    get_current_user,
    verify_password,
    send_reset_password_email,
)
from users.model import User

logger = logging.getLogger(__name__)


def signup_user(user_data: SignupRequest) -> User:
    """
    Register a new user and return an access token.
    """
    try:
        existing_user = repository.get_user_by_email(user_data.email)
        if existing_user:
            logger.warning(f"User with email {user_data.email} already exists.")
            raise HTTPException(status_code=400, detail="User already exists")
        existing_phone = repository.get_user_by_phone_number(user_data.phone_number)
        if existing_phone:
            logger.warning(f"Duplicate phone number: {user_data.phone_number}")
            raise HTTPException(status_code=400, detail="Duplicate phone number")
        password = get_password_hash(user_data.password)
        user_payload = user_data.dict()
        user_payload["password"] = password
        user = repository.create_user(user_payload)
        access_token = create_access_token(data={"sub": user.email})
        return access_token
    except Exception as exc:
        logger.error(f"Error in signup_user: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Signup failed.")


def verify_user(token: str):
    try:
        user = get_current_user(token)
        if not user:
            logger.warning("User does not exist for verification.")
            raise HTTPException(status_code=404, detail="User does not exist")
        if user.is_verified:
            logger.info(f"User {user.email} already verified.")
            raise HTTPException(status_code=400, detail="User already verified")
        user.is_verified = True
        user.is_active = True
        return repository.verify_user(user)
    except Exception as exc:
        logger.error(f"Error in verify_user: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Email verification failed.")


def login(email, password) -> str:
    try:
        user = repository.get_user_by_email(email)
        if not user:
            logger.warning(f"Login failed: user {email} not found.")
            raise HTTPException(status_code=400, detail="User not found.")
        if user.is_deleted:
            logger.warning(f"Login failed: user {email} is deleted.")
            raise HTTPException(status_code=400, detail="This user account is deleted.")
        if not verify_password(password, user.password):
            logger.warning(f"Login failed: incorrect password for user {email}.")
            raise HTTPException(
                status_code=403,
                detail="Incorrect password",
            )
        access_token = create_access_token(
            data={"sub": user.email}
        )
        return access_token
    except Exception as exc:
        logger.error(f"Error in login: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed.")


def forget_password(email):
    try:
        user = repository.get_user_by_email(email)
        if not user:
            logger.warning(f"Password reset requested for non-existent user {email}.")
            raise HTTPException(status_code=400, detail="User not found.")
        access_token = create_access_token(data={"sub": user.email})
        send_reset_password_email(user.email, user.name, access_token)
        return {"message": "please check your email"}
    except Exception as exc:
        logger.error(f"Error in forget_password: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password reset request failed.")


def reset_password(token, password):
    try:
        user = get_current_user(token, is_token=True)
        if not user:
            logger.warning("Password reset: user does not exist.")
            raise HTTPException(status_code=404, detail="User does not exist")
        if verify_password(password, user.password):
            logger.warning("Password reset: new password same as old password.")
            raise HTTPException(
                status_code=403,
                detail="New password cannot be the same as the old password",
            )
        hashed_password = get_password_hash(password)
        return repository.update_password(user, hashed_password)
    except Exception as exc:
        logger.error(f"Error in reset_password: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password reset failed.")


def change_password(user, old_password, new_password):
    """
    Change a user's password after verifying the old password
    """
    try:
        if not verify_password(old_password, user.password):
            logger.warning(f"Change password failed: incorrect old password for user {user.email}.")
            raise HTTPException(status_code=400, detail="Current password is incorrect")
        hashed_password = get_password_hash(new_password)
        return repository.update_password(user, hashed_password)
    except Exception as exc:
        logger.error(f"Error in change_password: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password change failed.")
