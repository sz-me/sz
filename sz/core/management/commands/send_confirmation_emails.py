# -*- coding: utf-8 -*-
from django.core.management.base import NoArgsCommand
from sz.core.services.email import ConfirmationEmailService


class Command(NoArgsCommand):
    confirmation_email_service = ConfirmationEmailService()

    def handle_noargs(self, **options):
        self.confirmation_email_service.send_confirmation_emails()
