# -*- coding: utf-8 -*-


from __future__ import absolute_import, unicode_literals, print_function

from providers.payments import BraintreePaymentMixin
from providers.views import ProviderPurchaseView
from .provider import {{cookiecutter.provider_name_capitalized}}Provider


class {{cookiecutter.provider_name_capitalized}}ProviderPurchaseView(
    BraintreePaymentMixin,
    ProviderPurchaseView
):
    provider = {{cookiecutter.provider_name_capitalized}}Provider

    def __init__(self, *args, **kwargs):
        super({{cookiecutter.provider_name_capitalized}}ProviderPurchaseView, self).__init__(self, *args,
                                                           **kwargs)

    def pre_book(self):
        return self.provider.pre_booking_actions(self.current_user,
                                                 self.session,
                                                 num_tickets=self.ticket_number)


class {{cookiecutter.provider_name_capitalized}}IframeView(object):
    pass
