# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals, print_function

from django.apps import AppConfig
from django.conf import settings


class {{cookiecutter.provider_name_capitalized}}ProviderConfig(AppConfig):
    """
    Configuration params for {{cookiecutter.app_name}}
    """

    name = '{{cookiecutter.app_name}}'
    verbose_name = '{{cookiecutter.provider_name_capitalized}} Provider'

    partner_id = settings.{{cookiecutter.provider_name|upper}}_PARTNER_ID
