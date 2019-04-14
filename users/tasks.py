import smtplib

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from defrag.settings.celery import app
from users.models import User


@app.task(bind=True, max_retries=3)
def invite_email(self, invitee_emails, referee_id, host):
    """Celery Task that sends invitation email to new invitee."""
    try:
        referee = User.objects.get(id=referee_id)
        subject = "Welcome"
        email_message = render_to_string('emails/invite_email.html', {
            'referee': referee, 'host': host + "/users/",
            'credits': settings.REFERRAL_CREDITS
        })
        message = EmailMessage(subject, email_message,
                               settings.DEFAULT_FROM_EMAIL,
                               invitee_emails)
        message.content_subtype = "html"
        message.send(fail_silently=False)
    except smtplib.SMTPAuthenticationError as smtpauth:
        print(smtpauth.message)
    except Exception as e:
        self.retry(countdown=2)
        print(e.message)
