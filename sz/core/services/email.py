# -*- coding: utf-8 -*-
from collections import Iterable

from django.core.mail import send_mail
from django.template.loader import render_to_string

from sz.settings import DEFAULT_FROM_EMAIL
from sz.core.models import User


class EmailService:

    send_mail = send_mail

    def send(self, subject, message, recipients,
             sender=DEFAULT_FROM_EMAIL):
        if not isinstance(recipients, Iterable):
            recipients = (recipients,)
        email = lambda recipient: (
            recipient.email if isinstance(recipient, User) else recipient
        )
        return  self.send_mail(
            subject, message, sender,
            map(email, recipients)
        )

    def send_template_message(self, subject_template, message_template,
                              context, recipients, sender=DEFAULT_FROM_EMAIL):
        subject = render_to_string(subject_template, context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, context)
        return  self.send(subject, message, recipients, sender)
