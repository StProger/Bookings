from pydantic import EmailStr

from app.tasks.celery import celery

from PIL import Image

from pathlib import Path

from app.tasks.email_templates import create_booking_confirmation_template

from app.config import settings

import smtplib


@celery.task
def process_pic(
        path: str
):

    im_path = Path(path)
    im = Image.open(path)

    res_im_1000_500 = im.resize((1000, 500))
    res_im_200_100 = im.resize((200, 100))

    res_im_1000_500.save(f"app/static/images/resized_1000_500_{im_path.name}")
    res_im_200_100.save(f"app/static/images/resized_200_100_{im_path.name}")


@celery.task
def send_booking_confirmation_email(
        booking: dict,
        email_to: EmailStr
):

    email_to_mock = settings.SMTP_USER
    msg_content = create_booking_confirmation_template(
        booking, email_to_mock
    )

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:

        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(msg_content)
