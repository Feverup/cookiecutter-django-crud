# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import logging
from datetime import timedelta

from django.apps import apps
from django.conf import settings
from django.utils.timezone import now
from psycopg2.extras import NumericRange
from pyticketswitch import Client
from pyticketswitch.customer import Customer

from core.models.plan import Plan
from {{cookiecutter.app_name}}.models import {{cookiecutter.model_name}}
from {{cookiecutter.app_name}}.serializers import {{cookiecutter.provider_name_capitalized}}Serializer


config = apps.get_app_config('{{cookiecutter.app_name}}')
logger = logging.getLogger(__name__)


class {{cookiecutter.provider_name_capitalized}}Service(object):
    """Singleton to be used as base for the {{cookiecutter.provider_name_capitalized}} service, generic
    definitions are configured here"""

    def __init__(self):
        self.serializer = {{cookiecutter.provider_name_capitalized}}Serializer()
        self.defaut_partner_id = config.partner_id

    def sync_events(self):
        # TODO logic for prefetching all events from the provider into
        # our database.
        # Flow is, fetching events one by one, passing them through the
        # serializer to convert into our internal model, and then saving them
        pass

    def update_sessions(self, imported_main_plan):
        {{cookiecutter.provider_name}}_event = imported_main_plan.provider_extra

        # TODO fetch the sessions for the main plan from the third party API
        # creating new ones and updating existing ones (Availability, price..)

    def get_available_tickets(self, plan):
        # TODO return the available tickets for a session, as provided
        # by the API
        return 0

    def update_sellable_status(self, {{cookiecutter.provider_name}}_event):
        # TODO Calculate if this event can be sold. Reasons why it might not
        # be sellable anymore is lack of sessions, lack of valid delivery
        # options, or other restrictions
        pass
