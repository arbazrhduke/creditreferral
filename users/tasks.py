from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from users.models import User


def invite_email(invitee_emails, referee_id, host):
    referee = User.objects.get(id=referee_id)
    subject = "Welcome"
    email_message = render_to_string('emails/invite_email.html', {
        'referee': referee, 'host': host+"/users/", 'credits': settings.REFERRAL_CREDITS
    })
    message = EmailMessage(subject, email_message, settings.DEFAULT_FROM_EMAIL,
                           invitee_emails)
    message.content_subtype = "html"
    message.send(fail_silently=False)
