from celery import shared_task

from .utils import send_email


@shared_task()
def send_activation_email(user, token):
    subject = "Verify your email"
    content = f"{user.id}{token}"
    recipient = user.email
    send_email(subject, content, recipient)


@shared_task()
def send_employee_setup_email(user, token):
    subject = "Setup your account"
    content = f"{user.id}{token}"
    recipient = user.email
    send_email(subject, content, recipient)


@shared_task()
def send_password_reset_email(user, token):
    subject = "Password reset link"
    content = f"{user.id}{token}"
    recipient = user.email
    send_email(subject, content, recipient)
