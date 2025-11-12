from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_background(subject, message, recipient):
    send_mail(
        subject,
        message,
        None,
        [recipient],
        fail_silently=False,
    )
