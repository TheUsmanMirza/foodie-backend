from pydantic import EmailStr, BaseModel, Field
from uuid import UUID


class SignupRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr = Field(..., description="User's email address.")
    phone_number: str = Field(..., description="User's phone number.")
    name: str = Field(..., description="User's full name.")
    password: str = Field(..., description="User's password.")
    restaurant_id: UUID = Field(..., description="Associated restaurant ID.")


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: str = Field(..., description="User's email address.")
    password: str = Field(..., description="User's password.")


class ResetPasswordRequest(BaseModel):
    """Request model for resetting user password."""
    password: str = Field(..., description="New password.")


class ChangePasswordRequest(BaseModel):
    """Request model for changing user password."""
    old_password: str = Field(..., description="Current password.")
    new_password: str = Field(..., description="New password.")


class UserResponse(BaseModel):
    """Response model for user details."""
    id: UUID = Field(..., description="User's unique identifier.")
    name: str = Field(..., description="User's full name.")
    email: EmailStr = Field(..., description="User's email address.")
    phone_number: str = Field(..., description="User's phone number.")
    restaurant_id: UUID = Field(..., description="Associated restaurant ID.")


class ErrorResponse(BaseModel):
    """Standard error response model for API errors."""
    error: str = Field(..., description="Error message.")
    status_code: int = Field(..., description="HTTP status code.")

