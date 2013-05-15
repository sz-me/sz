# -*- coding: utf-8 -*-
from sz.core.models import User, RegistrationProfile
from sz.core.services.email import EmailService


class RegistrationService(object):
    email_service = EmailService()

    def register(self, email, style, password):
        user = RegistrationProfile.objects.create_unverified_user(
            email, password, style)
        # TODO: Отправка письма
        return user

    def confirm(self, confirmation_key):
        return RegistrationProfile.confirm_email(confirmation_key)