# from uuid import UUID

# from pydantic import BaseModel, EmailStr, Field, field_validator


# class USERROLES:
#     ADMIN = "admin"


# class CreateUserRequest(BaseModel):
#     first_name: str
#     last_name: str
#     email: EmailStr  # This will validate email format
#     password: str = Field(..., min_length=8)  # Minimum password length

#     @field_validator("password")
#     def password_strength(cls, v):
#         """Validate password strength"""
#         if len(v) < 8:
#             raise ValueError("Password must be at least 8 characters")
#         return v


# class Token(BaseModel):
#     access_token: str
#     refresh_token: str
#     token_type: str
#     expires_in: int  # seconds until access token expires


# class TokenData(BaseModel):
#     user_id: str | None = None

#     def get_uuid(self) -> UUID | None:
#         if self.user_id:
#             return UUID(self.user_id)
#         return None


# class ForgotPasswordRequest(BaseModel):
#     email: EmailStr


# class RefreshTokenRequest(BaseModel):
#     refresh_token: str


# class ResetForgetPassword(BaseModel):
#     secret_token: str
#     new_password: str = Field(..., min_length=8)
#     confirm_password: str = Field(..., min_length=8)

#     @field_validator("new_password")
#     def password_strength(cls, v):
#         """Validate password strength"""
#         if len(v) < 8:
#             raise ValueError("Password must be at least 8 characters")
#         return v

#     @field_validator("confirm_password")
#     def passwords_match(cls, v, info):
#         if "new_password" in info.data and v != info.data["new_password"]:
#             raise ValueError("Passwords do not match")
#         return v
