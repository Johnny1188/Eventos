from __future__ import absolute_import, unicode_literals

from celery import shared_task

# sending email saying that the specific user has received 1 credit
@shared_task
def sendEmail(user_id):
    print("Email sent to "+str(user_id))
    return("Success")