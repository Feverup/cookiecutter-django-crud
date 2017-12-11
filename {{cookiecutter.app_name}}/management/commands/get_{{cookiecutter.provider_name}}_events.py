# -*- coding: utf-8 -*-
"""This command generates and stores Ingresso events from the ingresso client.
"""
from __future__ import absolute_import, unicode_literals, print_function

from django.core.management.base import BaseCommand

from {{cookiecutter.app_name}}.services import {{cookiecutter.provider_name_capitalized}}Service


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Getting {cookiecutter.provider_name_capitalized}} Events...')

        return {{cookiecutter.provider_name_capitalized}}Service().sync_events()
