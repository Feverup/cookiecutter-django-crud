from decimal import Decimal

from braces.views import GroupRequiredMixin
from django.conf import settings
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.functional import cached_property
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django_object_actions import DjangoObjectActions

from b2b.forms import TemplateSessionTermsForm
from core.models.partner import Partner
from core.models.place import City
from {{cookiecutter.app_name}} import models
from {{cookiecutter.app_name}}.filters import CanSell{{cookiecutter.provider_name_capitalized}}PlansListFilter
from {{cookiecutter.app_name}}.services import {{cookiecutter.provider_name_capitalized}}Service
from {{cookiecutter.app_name}}.tasks import import_sessions_for_plan


class {{cookiecutter.provider_name_capitalized}}GroupRequiredMixin(GroupRequiredMixin):
    group_required = [u"Operations", u"Content"]


@admin.register(models.{{cookiecutter.model_name}})
class {{cookiecutter.model_name}}Admin({{cookiecutter.provider_name_capitalized}}GroupRequiredMixin, DjangoObjectActions,
                         admin.ModelAdmin):
    group_required = [u"Operations", u"Content"]

    list_display = [
        'id', '{{cookiecutter.provider_name}}_id', 'event_title', 'can_sell',
        'place_name', 'city_name', 'country_name'
    ]

    list_filter = [
        'city_name', 'country_name', CanSell{{cookiecutter.provider_name_capitalized}}PlansListFilter
    ]

    search_fields = [
        'event_title', 'place_name', 'city_name', 'country_name', 'id',
        '{{cookiecutter.provider_name}}_id'
    ]
    change_actions = ['import_to_fever']

    def changelist_view(self, request, extra_context=None):
        """ Set default values for filters """
        q = request.GET.copy()
        if 'can_sell' not in request.GET:
            q['can_sell'] = '0'  # default value to show sellable events
        request.GET = q
        request.META['QUERY_STRING'] = request.GET.urlencode()

        return super({{cookiecutter.model_name}}Admin, self).changelist_view(
            request, extra_context=extra_context)

    def get_model_perms(self, request):
        return {}

    def import_to_fever(self, request, obj):
        return HttpResponseRedirect(
            reverse('{{cookiecutter.app_name}}:import-plans', args=(obj.id,))
        )

    import_to_fever.label = _('Import to fever')


class PlanDetail({{cookiecutter.provider_name_capitalized}}GroupRequiredMixin, DetailView):
    template_name = 'admin/{{cookiecutter.app_name}}/plan_detail.html'
    pk_url_kwarg = 'plan_id'
    context_object_name = '{{cookiecutter.provider_name}}_plan_detail'
    queryset = models.{{cookiecutter.model_name}}.objects.all()

    def get_context_data(self, **kwargs):
        context = super(PlanDetail, self).get_context_data(**kwargs)

        context['default_city_code'] = {{cookiecutter.default_city}}
        context['terms_form'] = TemplateSessionTermsForm(
            initial=settings.{{cookiecutter.provider_name|upper}}_API_DEFAULT_TERMS)
        return context

    @cached_property
    def cities(self):
        return City.objects.all()

    def post(self, request, *args, **kwargs):
        service = {{cookiecutter.provider_name_capitalized}}Service()
        partner = Partner.objects.get(id=service.defaut_partner_id)
        city = City.objects.get(code=request.POST.get('city_code'))
        imported_main_plan = self.get_object().import_plan(city, partner)
        self.update_terms(imported_main_plan, request.POST)
        link = reverse('admin:core_mainplan_change',
                       args=(imported_main_plan.id,))

        import_sessions_for_plan.delay(imported_main_plan.id)

        return HttpResponseRedirect(link)

    @staticmethod
    def update_terms(main_plan, post_data):
        template_session = main_plan.templatesession

        rsvp_fee = post_data.get('commission_rsvp_fee').strip()
        paid_percentage = post_data.get('commission_paid_percentage').strip()
        paid_fee = post_data.get('commission_paid_fee').strip()
        vat_percentage = post_data.get('vat_percentage').strip()
        kind_of_payment = post_data.get('kind_of_payment').strip()

        new_terms = {
            'commission_rsvp_fee':
                Decimal(rsvp_fee) if len(rsvp_fee) > 0 else None,
            'commission_paid_percentage':
                Decimal(paid_percentage) if len(paid_percentage) > 0 else None,
            'commission_paid_fee':
                Decimal(paid_fee) if len(paid_fee) > 0 else None,
            'vat_percentage':
                Decimal(vat_percentage) if len(vat_percentage) > 0 else None,
            'kind_of_payment': kind_of_payment
        }

        template_session.terms.update(new_terms)
        template_session.save()
