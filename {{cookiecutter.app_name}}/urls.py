# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from django.conf.urls import url
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView

from . import admin as views


# place app url patterns here
urlpatterns = [
    url(r'^admin/providers/{{cookiecutter.provider_name}}/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'admin:{{cookiecutter.app_name}}_{{cookiecutter.provider_name}}event_changelist'
            )
        ),
        name='{{cookiecutter.provider_name}}'),
    url(r'^admin/providers/{{cookiecutter.provider_name}}/plans/(?P<plan_id>\w+)/$',
        admin.site.admin_view(views.PlanDetail.as_view()),
        name='import-plans'),
]
