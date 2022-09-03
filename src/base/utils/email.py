# import logging
# import emails
# from emails.template import JinjaTemplate
#
# from src.config import settings
#
# password_reset_jwt_subject = "preset"
#
#
# def send_email(email_to: str, subject_template="", html_template="", environment={}):
#     """Отправка email"""
#     assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
#     message = emails.Message(
#         subject=JinjaTemplate(subject_template),
#         html=JinjaTemplate(html_template),
#         mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
#     )
#     smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
#     if settings.SMTP_TLS:
#         smtp_options["tls"] = True
#     if settings.SMTP_USER:
#         smtp_options["user"] = settings.SMTP_USER
#     if settings.SMTP_PASSWORD:
#         smtp_options["password"] = settings.SMTP_PASSWORD
#     response = message.send(to=email_to, render=environment, smtp=smtp_options)
#     logging.info(f"send email result: {response}")
#     print("***********************AAAAAA", smtp_options)
#
#
# import smtplib
#
#
# def send_mail(email_to: str, template=""):
#     sender = settings.SMTP_USER
#     receiver = email_to
#     message = f"""\
#     Subject: Hi Mailtrap
#     To: {receiver}
#     From: {sender}
#     """
#     with smtplib.SMTP("smtp.mailtrap.io", 587) as server:
#         response1 = server.login("210c43833d13b4", "8a000ba8101a81")
#         response = server.sendmail(sender, receiver, message)
#         print(response1, response)
#
#     print(sender, receiver, message)


from sendgrid import SendGridAPIClient

from sendgrid.helpers.mail import Mail

from dotenv import load_dotenv

import os


load_dotenv()

# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
def send_mail(email_to: str, subject: '', template: ''):
    try:
        message = Mail(
            from_email=os.environ.get('EMAILS_FROM_EMAIL'),
            to_emails=email_to,
            subject=subject,
            html_content=template
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))  #os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response, '****')
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)