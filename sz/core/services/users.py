# -*- coding: utf-8 -*-
from sz.core.models import User, RegistrationProfile
from sz.core.services.email import EmailService


class RegistrationService(object):
    confirmation_email_subject_template = (
        'registration/confirmation_email_subject.txt'
    )
    confirmation_email_message_template = (
        'registration/confirmation_email_message.txt'
    )

    def __init__(self):
        self.email_service = EmailService()

    def register(self, email, style, password):
        user = RegistrationProfile.objects.create_unverified_user(
            email, password, style)
        profile = user.registrationprofile_set.all()[0]
        self.email_service.send_template_message(
            self.confirmation_email_subject_template,
            self.confirmation_email_message_template,
            dict(confirmation_key=profile.confirmation_key),
            [user]
        )
        return user

    def confirm(self, confirmation_key):
        return RegistrationProfile.confirm_email(confirmation_key)