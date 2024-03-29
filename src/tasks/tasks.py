import smtplib
from email.message import EmailMessage

from celery import Celery

from config import REDIS_HOST
from config import SMTP_PASSWORD
from config import SMTP_USER

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker=f"redis://{REDIS_HOST}:6379")


def get_email_template_after_registration(
    subject: str, email_to: str, token, username: str
):
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = SMTP_USER
    email["To"] = email_to

    email.set_content(
        "<div>"
        f'<h1 style="color: yellow;">Здравствуйте, {username}, а вот ваш jwt-токен </h1><h1>{token}</h1>'
        '<img src="https://www.advgazeta.ru/upload/iblock/eb9/nyuansy_sverkhurochnoy_raboty_1.jpg" width="600">'
        "</div>",
        subtype="html",
    )
    return email


def get_email_template_reset_password(subject: str, email_to: str, token):
    email = EmailMessage()
    email["Subject"] = subject
    email["From"] = SMTP_USER
    email["To"] = email_to

    email.set_content(
        "<div>"
        f"<h1>Видимо вы забыли пароль Для вас reset-token </h1><h1>{token}</h1>"
        "</div>",
        subtype="html",
    )
    return email


@celery.task
def send_registration_email(subject: str, email_to: str, token, username: str):
    email = get_email_template_after_registration(subject, email_to, token, username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


@celery.task
def send_reset_email(subject: str, email_to: str, token):
    email = get_email_template_reset_password(subject, email_to, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
