import logging
from blog.celery import celery
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage

logger = logging.getLogger(__name__)


@celery.task
def send_email(email, username):
    context = {
        'username': username
    }
    try:
        message = BaseEmailMessage(
            template_name='emails/email.html', context=context)
        message.send([email])
    except (BadHeaderError, Exception) as e:
        logger.error(f'something went wrong with the email {e}')
