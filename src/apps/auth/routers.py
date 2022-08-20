import uuid

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Query, Body
from fastapi.security import OAuth2PasswordRequestForm

from src.apps.auth.schemas import Token, VerificationOut, Msg, EmailRecover, ResetPassword, GoogleToken
from src.apps.auth.send_email import send_reset_password_email
from src.apps.auth.services import create_access_token, registration_user, verify_registration_user, \
    generate_password_reset_token, verify_password_reset_token, google_auth
from src.apps.user.schemas import UserOut, UserIn, GoogleUserCreate
from src.apps.auth.services import authenticate_user
from src.apps.user.services import UserService


auth_router = APIRouter()


@auth_router.post('/sign-up/', response_model=Msg)
async def user_registration(new_user: UserIn, task: BackgroundTasks):
    """ Регистрация пользователя """
    user = await registration_user(new_user, task)
    if user:
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        return {"msg": f"A confirmation message has been sent to {new_user.email}"}


@auth_router.get("/confirm-email/", response_model=Msg)
async def confirm_email(token: uuid.UUID = Query(title='Token for verification email')):
    if await verify_registration_user(token):
        return {"msg": "Success verify email"}
    else:
        raise HTTPException(status_code=404, detail="Not found")


@auth_router.post('/login/',  response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/password-recover/", response_model=Msg)
async def recover_password(email: EmailRecover, task: BackgroundTasks):
    """ Password Recovery """
    user = await UserService.get_user_by_email(email.email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    password_reset_token = generate_password_reset_token(email.email)
    task.add_task(
        send_reset_password_email, email_to=user.email, username=user.username, token=password_reset_token
    )
    return {"msg": f"Message to password recovering has been sent to {email.email}"}


@auth_router.get("/reset-password/", response_model=Msg)
async def reset_password(
    token: str = Query(default=..., title='token to reset password'),
    new_password: ResetPassword = Body(default='somepass', title='new password', example={'new_password': 'somepass'}),
):
    """ Reset password """
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = await UserService.get_user_by_email(email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    await UserService.change_password(user, new_password)
    return {"msg": "Password updated successfully"}


# @auth_router.get('/sign-up/google/page/')
# async def google_auth_page(request: Request):
#     return templates.TemplateResponse("google_login.html", {"request": request})


@auth_router.post('/sign-up/google/', response_model=GoogleToken)
async def create_google_user(user: GoogleUserCreate):
    user_id, token = await google_auth(user)
    return GoogleToken(id=user_id, token=token)
