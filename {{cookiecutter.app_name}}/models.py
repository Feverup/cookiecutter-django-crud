# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import datetime
import uuid
from decimal import Decimal
from logging import getLogger

from django.conf import settings
from django.db import models
from pysugarcrm import sugar_api

from core.models.place import Place
from core.models.plan import MainPlan, TemplateSession
from galleries.models import Gallery


logger = getLogger(__name__)


class {{cookiecutter.model_name}}(models.Model):
    """Specialization Class to be used in MainPlan.provider_extra"""

    class Meta:
        app_label = "{{cookiecutter.app_name}}"

    id = models.AutoField(auto_created=True, primary_key=True, serialize=False,
                          verbose_name='ID')
    {{cookiecutter.provider_name}}_id = models.TextField(unique=True)
    event_title = models.TextField()
    city_name = models.TextField(null=True)
    city_code = models.TextField(null=True)
    country_name = models.TextField(null=True)
    country_code = models.TextField(null=True)
    place_name = models.TextField()
    place_latitude = models.FloatField(null=True)
    place_longitude = models.FloatField(null=True)
    can_sell = models.BooleanField(default=True)

    def import_plan(self, city, partner):
        """Creates and stores a Fever MainPlan from the {{cookiecutter.provider_name_capitalized}} event
        data associated to the specified city and partner"""

        main_plan = MainPlan.objects.create(
            provider_extra=self,
            name=self.event_title,
            provider_name=MainPlan.PROVIDER_{{cookiecutter.provider_name|upper}},
            hidden_feed=True,
            partner=partner,
            contract_id=settings.{{cookiecutter.provider_name|upper}}_CONTRACT_ID,
            gallery=Gallery.objects.create()
        )

        # Create Session Template
        template_session = TemplateSession()
        template_session.ticket_price = Decimal(10.0)
        template_session.duration = datetime.timedelta(hours=2)
        template_session.main_plan = main_plan
        template_session.save()
        template_session.terms.update(settings.{{cookiecutter.provider_name|upper}}_API_DEFAULT_TERMS)
        template_session.save()

        place = Place.objects.filter(name=self.place_name).first()
        if not place:
            place = Place.objects.create(
                city=city,
                name=self.place_name, )
            if self.place_latitude is not None \
                and self.place_longitude is not None:
                place.longitude = self.place_longitude
                place.latitude = self.place_latitude
                place.save()

        template_session.places.add(place)

        main_plan.places.add(place)
        main_plan.cities.add(city)

        try:
            self.register_place_in_crm(place, city)
        except UnboundLocalError:
            # CRM connection failed here, log error and keep moving
            logger.error(
                "Fatal error connecting to SugarCRM updating information for"
                "the new {{cookiecutter.provider_name_capitalized}} place with id {} .".format(place.id)
            )

        return main_plan

    @staticmethod
    def register_place_in_crm(place, city):
        # Create Place in CRM
        with sugar_api(
            url=settings.SUGARCRM_KEYS['url'],
            login_path=settings.SUGARCRM_KEYS['login_path'],
            base_path=settings.SUGARCRM_KEYS['base_path'],
            username=settings.SUGARCRM_KEYS['username'],
            password=settings.SUGARCRM_KEYS['password'],
            platform='fever-{}'.format(uuid.uuid4().hex)
        ) as api:
            place_data = {
                'name': place.name,
                'venue_address_street_c': place.address,
                'venue_address_postalcode_c': place.zip_code,
                'city_c': '{}-{}'.format(city.country, city.code),
                'capacity_c': 100,
                'longitude_c': place.longitude,
                'latitude_c': place.latitude,
                'fever_id_c': place.id,
                'draft_c': False,
                'no_metrostation_c': True,
            }
            raw_data = api.post(
                '/fever_venue_addressses',
                place_data
            )

            try:
                place_sugar_id = raw_data['id']
                logger.info(
                    'place {place_id} with sugar id {place_sugar_id} '
                    'successfully created'.format(
                        place_id=place.id,
                        place_sugar_id=place_sugar_id
                    )
                )
            except AttributeError:
                logger.exception(
                    'Error creating place in SugarCRM',
                    extra={
                        'place': place,
                        'response': raw_data,
                        'place_sugar_id': raw_data.get('id')
                        }
                )
            else:
                raw_data = api.post(
                    '/Accounts/{% raw % }{{% endraw %}{{cookiecutter.provider_name}}{% raw % }_sugar_id}{% endraw %}/link/accounts_fever_venue'
                    '_addressses_2/{% raw % }{place_sugar_id}{% endraw % }'.format(
                        {{cookiecutter.provider_name}}_sugar_id=settings.{{cookiecutter.provider_name|upper}}_API_SUGAR_CRM_ID,
                        place_sugar_id=place_sugar_id
                    ),
                )

                # Get {{cookiecutter.provider_name_capitalized}} partner record id
                partner_record = (
                    raw_data['record']
                    if 'record' in raw_data else None
                )
                partner_record_id = (
                    partner_record.get('id', None)
                    if partner_record else None
                )

                # Get place record id
                place_record = (
                    raw_data['related_record']
                    if 'related_record' in raw_data else None
                )
                place_record_id = (
                    place_record.get('id', None)
                    if place_record else None
                )

                if partner_record_id != settings.{{cookiecutter.provider_name|upper}}_API_SUGAR_CRM_ID or \
                        place_record_id != place_sugar_id:
                    logger.error(
                        'Error associating place to {{cookiecutter.provider_name_capitalized}} partner',
                        extra={
                            'place': place,
                            'response': raw_data,
                            'place_sugar_id': place_sugar_id,
                            '{{cookiecutter.provider_name}}_sugar_id': settings.{{cookiecutter.provider_name|upper}}_API_SUGAR_CRM_ID,
                        }
                    )

                logger.info(
                    'place {place_id} with sugar id {place_sugar_id} '
                    'successfully linked to {{cookiecutter.provider_name_capitalized}} partner'.format(
                        place_id=place.id,
                        place_sugar_id=place_sugar_id
                    )
                )
