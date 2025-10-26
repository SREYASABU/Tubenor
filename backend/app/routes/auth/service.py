# import os
# from datetime import datetime, timedelta, timezone
# from typing import Annotated
# from uuid import UUID, uuid4

# import jwt
# from database.core import DbSession
# from entities.user import User
# from fastapi import BackgroundTasks, Depends, HTTPException, Request, status
# from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from jwt import PyJWTError
# from passlib.context import CryptContext
# from sqlalchemy.exc import IntegrityError
# from utils.exceptions import AuthenticationError
# from utils.logger import get_service_logger

# from routes.auth.models import (
#     USERROLES,
#     CreateUserRequest,
#     ForgotPasswordRequest,
#     ResetForgetPassword,
#     Token,
#     TokenData,
# )

# logger = get_service_logger("auth")

# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM", "HS256")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
# REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

# oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
# bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# def verify_password(plain_password: str, hashed_password: str) -> bool:
#     return bcrypt_context.verify(plain_password, hashed_password)


# def get_password_hash(password: str) -> str:
#     return bcrypt_context.hash(password)


# def authenticate_user(email: str, password: str, db: DbSession) -> User | bool:
#     user = db.query(User).filter(User.email == email).first()
#     if not user or not verify_password(password, user.password):
#         logger.warning(f"Authentication failed: {email}")
#         return False
#     return user


# def create_user(create_user_request: CreateUserRequest, db: DbSession):
#     logger.info(f"Creating user: {create_user_request.email}")
#     try:
#         create_user_model = User(
#             id=uuid4(),
#             email=create_user_request.email,
#             first_name=create_user_request.first_name,
#             last_name=create_user_request.last_name,
#             password=get_password_hash(create_user_request.password),
#         )
#         db.add(create_user_model)
#         db.commit()
#         logger.info(f"Successfully created user: {create_user_request.email}")
#     except IntegrityError:
#         db.rollback()
#         logger.warning(f"User already exists: {create_user_request.email}")
#         raise HTTPException(
#             status_code=status.HTTP_409_CONFLICT,
#             detail="User with this email already exists",
#         )
#     except Exception as e:
#         db.rollback()
#         logger.error(f"Failed to create user {create_user_request.email}: {str(e)}")
#         raise
#     return {"message": "User Created Successfully"}


# def create_access_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
#     encode = {
#         "sub": email,
#         "id": str(user_id),
#         "type": "access",
#         "exp": datetime.now(timezone.utc) + expires_delta,
#     }
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# def create_refresh_token(email: str, user_id: UUID, expires_delta: timedelta) -> str:
#     encode = {
#         "sub": email,
#         "id": str(user_id),
#         "type": "refresh",
#         "exp": datetime.now(timezone.utc) + expires_delta,
#     }
#     return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession
# ) -> Token:
#     user = authenticate_user(form_data.username, form_data.password, db)
#     if not user:
#         raise AuthenticationError()

#     access_token = create_access_token(
#         user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     refresh_token = create_refresh_token(
#         user.email, user.id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
#     )

#     return Token(
#         access_token=access_token,
#         refresh_token=refresh_token,
#         token_type="bearer",
#         expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # convert to seconds
#     )


# def verify_token(token: str, token_type: str = "access"):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         user_id: str = payload.get("id")
#         token_type_from_payload: str = payload.get("type")

#         # Verify token type matches expected type
#         if token_type_from_payload != token_type:
#             logger.warning(
#                 f"Token type mismatch: expected {token_type}, got {token_type_from_payload}"
#             )
#             raise AuthenticationError("Invalid token type")

#         return TokenData(user_id=user_id)
#     except PyJWTError as e:
#         logger.warning(f"Token verification failed: {str(e)}")
#         raise AuthenticationError()


# def refresh_access_token(refresh_token: str, db: DbSession) -> Token:
#     try:
#         # Verify refresh token
#         token_data = verify_token(refresh_token, token_type="refresh")

#         # Get user from database to ensure they still exist
#         user = db.query(User).filter(User.id == token_data.get_uuid()).first()
#         if not user:
#             logger.warning(f"User not found for token refresh: {token_data.user_id}")
#             raise AuthenticationError("User not found")

#         # Create new tokens
#         new_access_token = create_access_token(
#             user.email, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#         )
#         new_refresh_token = create_refresh_token(
#             user.email, user.id, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
#         )

#         logger.info(f"Token refreshed for user: {user.email}")
#         return Token(
#             access_token=new_access_token,
#             refresh_token=new_refresh_token,
#             token_type="bearer",
#             expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
#         )
#     except Exception as e:
#         logger.warning(f"Token refresh failed: {str(e)}")
#         raise AuthenticationError("Invalid refresh token")


# def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]) -> TokenData:
#     return verify_token(token)


# CurrentUser = Annotated[TokenData, Depends(get_current_user)]


# def get_user_details(db: DbSession):
#     return {
#         "user_id": "test_user_id",
#         "first_name": "test_user_name",
#         "last_name": "test_user_name",
#         "email": "test_user@example.com",
#         "role": USERROLES.ADMIN,
#     }


# def get_all_users(db: DbSession, sort_order: str, limit: int, offset: int):
#     return [
#         {
#             "user_id": "test_user_id",
#             "first_name": "test_user_name",
#             "last_name": "test_user_name",
#             "email": "test_user@example.com",
#             "role": USERROLES.ADMIN,
#         }
#     ]


# def forgot_password(
#     fpr: ForgotPasswordRequest,
#     background_tasks: BackgroundTasks,
#     request: Request,
#     db: DbSession,
# ):
#     logger.info(f"Password reset request for: {fpr.email}")
#     # TODO: Implement actual password reset logic
#     logger.info(f"Password reset email would be sent to: {fpr.email}")
#     return {
#         "message": "An email with a password reset link will be sent if the user exists in our system."
#     }


# def reset_password(rfp: ResetForgetPassword, db: DbSession):
#     logger.info("Password reset attempt")
#     # TODO: Implement actual password reset logic
#     logger.info("Password reset completed")
#     return {"message": "Password reset successfully"}
