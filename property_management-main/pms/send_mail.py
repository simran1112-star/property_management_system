from django.core.mail import send_mail as sm
from django.conf import settings

# To Send Email
def send_customise_mail(subject, body, email_id):
    res = sm(
        subject=subject,
        message=body,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[email_id],
        fail_silently=False,
    )

    return res
