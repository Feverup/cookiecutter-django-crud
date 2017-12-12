# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function

from django.contrib import admin


class CanSell{{cookiecutter.provider_name_capitalized}}PlansListFilter(admin.SimpleListFilter):
    """Class to filter sellable {{cookiecutter.provider_name}} events"""

    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = 'Can Sell'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'can_sell'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            (2, 'All plans'),
            (1, 'No'),
            (0, 'Yes'),
        )

    def queryset(self, request, queryset):
        # Compare the requested value
        # to decide how to filter the queryset.
        if self.value() == '0':  # Sellable Plans
            return queryset.filter(can_sell=True)
        if self.value() == '1':  # Yet-to-occur plans
            return queryset.filter(can_sell=False)

        # everything
        return queryset
