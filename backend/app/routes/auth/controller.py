# from typing import Annotated

# from database.core import DbSession
# from fastapi import APIRouter, BackgroundTasks, Depends, Request, status
# from fastapi.security import OAuth2PasswordRequestForm
# from utils.logger import get_controller_logger
# from utils.rate_limiter import limiter

# from routes.auth import models, service

# logger = get_controller_logger("auth")
# router = APIRouter(prefix="/auth", tags=["auth"])


# @router.post("/register", status_code=status.HTTP_201_CREATED)
# @limiter.limit("5/hour")
# async def create_user(
#     request: Request, create_user_request: models.CreateUserRequest, db: DbSession
# ):
#     logger.info(f"User registration attempt: {create_user_request.email}")
#     try:
#         result = service.create_user(create_user_request, db)
#         logger.info(f"Successfully registered user: {create_user_request.email}")
#         return result
#     except Exception as e:
#         logger.error(f"Registration failed for {create_user_request.email}: {str(e)}")
#         raise


# @router.post("/token", response_model=models.Token)
# async def login_for_access_token(
#     form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: DbSession
# ):
#     logger.info(f"Login attempt: {form_data.username}")
#     try:
#         result = service.login_for_access_token(form_data, db)
#         logger.info(f"Successful login: {form_data.username}")
#         return result
#     except Exception:
#         logger.warning(f"Failed login: {form_data.username}")
#         raise


# @router.get("/verify-token/{token}")
# async def verify_user_token(token: str):
#     try:
#         return service.verify_token(token)
#     except Exception as e:
#         logger.warning(f"Token verification failed: {str(e)}")
#         raise


# @router.post("/forgot-password")
# async def forgot_password(
#     background_tasks: BackgroundTasks,
#     fpr: models.ForgotPasswordRequest,
#     request: Request,
#     db: DbSession,
# ):
#     logger.info(f"Password reset request: {fpr.email}")
#     try:
#         result = service.forgot_password(fpr, background_tasks, request, db)
#         return result
#     except Exception as e:
#         logger.error(f"Password reset failed for {fpr.email}: {str(e)}")
#         raise


# @router.post("/reset-password", status_code=status.HTTP_200_OK)
# async def reset_password(rfp: models.ResetForgetPassword, db: DbSession):
#     logger.info("Password reset attempt")
#     try:
#         return service.reset_password(rfp, db)
#     except Exception as e:
#         logger.error(f"Password reset failed: {str(e)}")
#         raise


# @router.post("/refresh", response_model=models.Token)
# async def refresh_token(refresh_request: models.RefreshTokenRequest, db: DbSession):
#     logger.info("Token refresh attempt")
#     try:
#         result = service.refresh_access_token(refresh_request.refresh_token, db)
#         logger.info("Token refreshed successfully")
#         return result
#     except Exception as e:
#         logger.warning(f"Token refresh failed: {str(e)}")
#         raise
