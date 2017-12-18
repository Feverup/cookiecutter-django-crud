# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

import logging

from celery.decorators import task

from core.models.plan import Plan, MainPlan
from {{cookiecutter.app_name}}.models import {{cookiecutter.model_name}}
from {{cookiecutter.app_name}}.services import {{cookiecutter.provider_name_capitalized}}Service


logger = logging.getLogger(__name__)


@task(queue="{{cookiecutter.provider_name}}")
def update_available_tickets_for_session(session_id):
    """
    Update number of available tickets for a session
    """
    plan = Plan.objects.filter(id=session_id).first()
    if plan:
        plan.update_available_tickets()
        return True
    return False


@task(queue="{{cookiecutter.provider_name}}")
def import_sessions_for_plan(main_plan_id):
    """
    Update number of available tickets for a session
    """
    main_plan = MainPlan.objects.filter(id=main_plan_id).first()
    if main_plan:
        {{cookiecutter.provider_name_capitalized}}Service().update_sessions(main_plan)
        return True
    return False


@task(queue="{{cookiecutter.provider_name}}")
def import_new_sessions_for_existing_plans():
    """
    Updates existing plans with new sessions if available, and updates availability for existing sessions
    """
    service = {{cookiecutter.provider_name_capitalized}}Service()
    main_plans = MainPlan.objects.filter(provider_name=MainPlan.PROVIDER_{{cookiecutter.provider_name|upper}}).all()

    for main_plan in main_plans:
        service.update_sessions(main_plan)

@task(queue="{{cookiecutter.provider_name}}")
def check_{{cookiecutter.provider_name}}_plans_sellable_status():
    """
    Checks {{cookiecutter.provider_name}} plans to see if they have at least one sellable session
    """
    service = {{cookiecutter.provider_name_capitalized}}Service()
    {{cookiecutter.provider_name}}_events = {{cookiecutter.model_name}}.objects.all()

    for {{cookiecutter.provider_name}}_event in {{cookiecutter.provider_name}}_events:
        service.update_sellable_status({{cookiecutter.provider_name}}_event)
