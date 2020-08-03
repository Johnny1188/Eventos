from __future__ import absolute_import, unicode_literals
from celery import shared_task 
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

# SENDING EMAILS
#   - what_happend parameter can have these pre-defined values:
#       "new credit"
#       ""
@shared_task
def sendEmail(what_happened, recipient_email="jsobotka@centum.cz"):
    print(recipient_email)
    send_mail(what_happened,
            'Here is the message.',
            settings.EMAIL_HOST_USER,
            [recipient_email],
            fail_silently=False)
    return