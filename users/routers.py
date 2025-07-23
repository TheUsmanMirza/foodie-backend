import logging
from fastapi import APIRouter, Depends, HTTPException

from users import services
from users.model import User
from users.schema import SignupRequest, LoginRequest, ResetPasswordRequest, ChangePasswordRequest, UserResponse
from users.utils import get_current_user


logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/signup/")
def signup(user_data: SignupRequest):
    try:
        access_token = services.signup_user(user_data)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as exc:
        logger.error(f"Error during signup: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Signup failed.")


@router.get("/verify-email/")
def verify_email(token: str):
    try:
        user = services.verify_user(token)
        if user:
            return {"message": "Email verified! You can now login."}
    except Exception as exc:
        logger.error(f"Error during email verification: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Email verification failed.")


@router.post("/login")
def login(request: LoginRequest) -> dict:
    try:
        access_token = services.login(request.email, request.password)
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as exc:
        logger.error(f"Error during login: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed.")


@router.get("/protected/")
def protected(current_user: User = Depends(get_current_user)):
    try:
        return UserResponse(
            id=current_user.id,
            name=current_user.name,
            email=current_user.email,
            phone_number=current_user.phone_number,
            restaurant_id=current_user.restaurant_id,
        )
    except Exception as exc:
        logger.error(f"Error accessing protected resource: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to access protected resource.")


@router.get("/forget_password")
def forget_password(email: str):
    try:
        return services.forget_password(email)
    except Exception as exc:
        logger.error(f"Error during password reset request: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password reset request failed.")


@router.post("/reset_password/{token}")
def reset_password(request: ResetPasswordRequest, token: str):
    try:
        return services.reset_password(token, request.password)
    except Exception as exc:
        logger.error(f"Error during password reset: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password reset failed.")


@router.post("/change-password")
def change_password(request: ChangePasswordRequest, current_user: User = Depends(get_current_user)):
    """
    Change the password for the authenticated user
    """
    try:
        return services.change_password(current_user, request.old_password, request.new_password)
    except Exception as exc:
        logger.error(f"Error during password change: {str(exc)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Password change failed.")
