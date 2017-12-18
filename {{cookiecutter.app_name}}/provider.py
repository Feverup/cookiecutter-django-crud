from core.models.invitation import Ticket
from {{cookiecutter.app_name}}.services import {{cookiecutter.provider_name_capitalized}}Service
from {{cookiecutter.app_name}}.tasks import update_available_tickets_for_session
from providers import AbstractProvider


class {{cookiecutter.provider_name_capitalized}}Provider(AbstractProvider):
    """{{cookiecutter.provider_name_capitalized}} Ticketing Provider"""

    def __init__(self, *args, **kwargs):
        super({{cookiecutter.provider_name_capitalized}}Provider, self).__init__(*args, **kwargs)

        self.service = {{cookiecutter.provider_name_capitalized}}Service()

    def available_tickets(self, plan):
        return self.service.get_available_tickets(plan)

    def has_available_tickets(self, plan):
        """
        Checks if plan is available

        :param plan: Plan object
        :returns: True if available
        """
        return bool(
            not plan.sold_out and
            plan.available_tickets and
            plan.available_tickets >= plan._allowed_num_tickets_lower
        )

    def check_attend_parameters(self, user, plan, action, num_tickets=1):
        """
        Checks additional parameters for attend

        :param user: User object
        :param plan: Plan object
        :param action: attend or unattend
        :returns: True
        """
        raise NotImplementedError

    def void_booking(self, *args, **kwargs):
        """
        Void the booking and returns the tickets to the inventory.

        :returns: False
        """
        # TODO implement if this specific provider allows refunds.
        # Otherwise just remove this comment and leave it as is
        return False

    def book(self, user, plan, num_tickets=1, *args, **kwargs):
        """
        Books tickets for a plan
        """

        # TODO specific provider book logic

    def pre_booking_actions(self, user, plan, *args, **kwargs):
        """Performs required actions before booking the plan

        :param user: User object
        :param plan: Plan object
        :returns: True if actions performed successfully, False otherwise
        """

        # TODO specific provider pre book/reservation logic
        return True

    def refund_ticket(self, ticket, *args, **kwargs):
        """Refunds a cancelled or returned ticket

        :param Ticket ticket: The ticket to try to refund
        :returns: False
        """
        # TODO implement if this specific provider allows refunds.
        # Otherwise just remove this comment and leave it as is

        return False

    def attend_session(self, user, plan, num_tickets=1, *args, **kwargs):
        """Performs attend action for user to plan

        :param user: User object
        :param plan: Plan object
        :param num_tickets: number of tickets
        :returns: True if attend ok
        """
        # TODO specific attend logic. We will rarely take providers with free
        # plans but implement this method if needed. Otherwise leave it as is
        raise False

    def post_booking_actions(self, user, plan, num_tickets=1, *args, **kwargs):
        update_available_tickets_for_session.delay(plan.id)

        # Update Ticket
        ticket = Ticket.objects.filter(owner=user).order_by(
            'purchase_time').last()

        self.update_ticket_extra_data(ticket, plan)

    def update_ticket_extra_data(self, ticket, plan):
        # TODO include provider specific data in the ticket extra field
        # this includes all required data to display on the confirmation email
        # like seats, confirmation id, selfprint url...
        pass

    def unattend_session(self, user, plan):
        """Performs unattend action for user from plan

        :param user: User object
        :param plan: Plan object
        :returns: True if unattend ok
        """
        # TODO implement provider specific logic if we support free events
        # Otherwise leave it as is
        return False
