# -*- coding: utf-8 -*-
import datetime
from collections import Iterable

from django.core.mail import send_mail
from django.template.loader import render_to_string

from sz.settings import DEFAULT_FROM_EMAIL
from sz.core.models import User, RegistrationProfile


class EmailService:

    def send(self, subject, message, recipients,
             sender=DEFAULT_FROM_EMAIL):
        if not isinstance(recipients, Iterable):
            recipients = (recipients,)
        email = lambda recipient: (
            recipient.email if isinstance(recipient, User) else recipient
        )
        return send_mail(
            subject,
            message,
            sender,
            map(email, recipients)
        )

    def send_template_message(self, subject_template, message_template,
                              context, recipients, sender=DEFAULT_FROM_EMAIL):
        subject = render_to_string(subject_template, context)
        subject = ''.join(subject.splitlines())
        message = render_to_string(message_template, context)
        return self.send(subject, message, recipients, sender)


class ConfirmationEmailService:
    email_service = EmailService()
    confirmation_email_subject_template = (
        'registration/confirmation_email_subject.txt'
    )
    confirmation_email_message_template = (
        'registration/confirmation_email_message.txt'
    )

    def send_confirmation_email(self, user):
        profile = user.registrationprofile_set.all()[0]
        self.email_service.send_template_message(
            self.confirmation_email_subject_template,
            self.confirmation_email_message_template,
            dict(confirmation_key=profile.confirmation_key),
            [user]
        )

    def send_confirmation_emails(self):
        profiles_for_sending = RegistrationProfile.objects.filter(
            is_sending_email_required=True
        )
        for profile in profiles_for_sending:
            try:
                self.send_confirmation_email(profile.user)
                profile.is_sending_email_required=False
            except Exception as exception:
                #TODO: Пишем в лог, что всё плохо
                print(
                    '[{0:%y-%m-%d %H:%M:%S}] Confirmation key for {1} '
                    'is not sent'.format(
                        datetime.datetime.now(),  profile.user)
                )
                print exception
