from celery import shared_task
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage


@shared_task
def send_email(email, username):
    context = {
        'username': username
    }
    try:
        message = BaseEmailMessage(
            template_name='emails/email.html', context=context)
        message.send([email])
    except BadHeaderError:
        print('Error sending email')
