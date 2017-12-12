# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import logging

from {{cookiecutter.app_name}}.models import {{cookiecutter.model_name}}


default_app_config = '{{cookiecutter.app_name}}.apps.{{cookiecutter.provider_name_capitalized}}ProviderConfig'
logger = logging.getLogger(__name__)


class {{cookiecutter.provider_name_capitalized}}Serializer(object):
    """Serializer from {{cookiecutter.provider_name}} events to our models """

    @staticmethod
    def from_{{cookiecutter.provider_name}}_client_event({{cookiecutter.provider_name_}}_client_event,
        existing_{{cookiecutter.provider_name}}_event=None, **kwargs):
        """Converts an event from the {{cookiecutter.provider_name}} client into a {{cookiecutter.model_name}} instance
        It does NOT save the generated event on the DB.

        Args:
            {{cookiecutter.provider_name}}_client_event: The event data as provided by the {{cookiecutter.provider_name_capitalized}} client

        Returns:
            {{cookiecutter.provider_name}}_event: The {{cookiecutter.model_name}} instance generated with the client data
        """

        {{cookiecutter.provider_name}}_event = existing_{{cookiecutter.provider_name}}_event or {{cookiecutter.model_name}}()
        {{cookiecutter.provider_name}}_event.can_sell = True

        return {{cookiecutter.provider_name_capitalized}}_event
