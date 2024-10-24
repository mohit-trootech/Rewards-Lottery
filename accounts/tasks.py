from celery import shared_task
from utils.constants import CeleryTasks, MailTemplates
import logging

logger = logging.getLogger(__name__)


@shared_task
def user_registration_success_mail(email, username):
    """
    send mail to user for successfull registration
    """
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.conf import settings

    sender = settings.EMAIL_HOST_USER
    receiver = email
    subject = CeleryTasks.REGISTRATION_SUCCESS_MAIL.value.format(username=username)
    text_template = render_to_string(
        MailTemplates.REGISTRATION_TXT.value, context={"username": username}
    )
    html_template = render_to_string(
        MailTemplates.REGISTRATION_HTML.value, context={"username": username}
    )
    msg = EmailMultiAlternatives(
        subject=subject, from_email=sender, to=[receiver], body=text_template
    )
    msg.attach_alternative(html_template, CeleryTasks.TEXT_HTML.value)
    msg.send()
    logger.info(subject)
    return CeleryTasks.REGISTRATION_MAIL_SUCCESS.value
