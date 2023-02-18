from django.core.mail import EmailMessage


def send_email(data):
    """
    Форма подтверждения с кодом.
    """
    email = EmailMessage(
        subject=data['email_subject'],
        body=data['email_body'],
        to=[data['email_to']],
    )
    email.send(fail_silently=False)
