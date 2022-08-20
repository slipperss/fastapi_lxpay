from src.config import settings
from src.base.utils.email import send_mail


def send_new_account_email(email_to: str, username: str, token: str):
    """ Отправка письма при создании пользователя """
    # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "email_verification.html") as f:
    #     template_str = f.read()

    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    link = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/auth/confirm-email/?token={token}"

    template = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <meta http-equiv="X-UA-Compatible" content="IE=edge">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <link rel="stylesheet" href="css/style.css">
          <link rel="shortcut icon" href="img/shortcut.png" type="image/x-icon">
          <title>Loong</title>
        </head>
        <body>
            <div style="align-items: center; justify-content: center; flex-direction: column;">
                <h3> Account Verification </h3>
                <br>
                <p> Hi! "{username}" Thanks for choosing {project_name}, please
                click on the link below to verify your account</p>
        <br>
                <a style="display:block; width:300px; margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                 href={link}>
                    Verify your email
                <a>
        <br>
                <p style="display:block;margin-top:1rem;">If you did not register for LXPay,
                please kindly ignore this email and nothing will happen. Thanks<p>
            </div>
        </body>
        </html>
    """

    send_mail(
        email_to=email_to,
        subject=subject,
        template=template,
    )

def send_reset_password_email(email_to: str, username: str, token: str):
    """ Отправка письма при сбросе пароля """
    # with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
    #     template_str = f.read()

    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {username}"

    if hasattr(token, "decode"):
        use_token = token.decode()
    else:
        use_token = token
        new_password = 'some_new_pass'
    link = f"http://{settings.SERVER_HOST}:{settings.SERVER_PORT}/api/auth/reset-password/?token={use_token}"#&new_password={new_password}"

    template = f"""
            <!DOCTYPE html>
            <html>
            <head>
              <meta charset="UTF-8">
              <meta http-equiv="X-UA-Compatible" content="IE=edge">
              <meta name="viewport" content="width=device-width, initial-scale=1.0">
              <link rel="stylesheet" href="css/style.css">
              <link rel="shortcut icon" href="img/shortcut.png" type="image/x-icon">
              <title>{project_name}</title>
            </head>
            <body>
                <div style="align-items: center; justify-content: center; flex-direction: column;">
                    <h3> Password recovering </h3>
                    <br>
                    <p> Hi! "{username}"
                    click on the link below to reset password</p>
            <br>
                    <a style="display:block; width:300px; margin-top:1rem; padding: 1rem; border-radius: 0.5rem; font-size: 1rem; text-decoration: none; background: #0275d8; color: white;"
                     href={link}>
                        Reset password
                    <a>
            <br>
                    <p style="display:block;margin-top:1rem;">
                    If you didn't want to change your password or change your mind, just ignore this message.. Thanks
                    <p>
                </div>
            </body>
            </html>
        """

    send_mail(
        email_to=email_to,
        subject=subject,
        template=template
    )