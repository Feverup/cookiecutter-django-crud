Settings to paste on local_settings.j2
Fill default terms as required

##################################################
#                {{cookiecutter.provider_name|upper}}
##################################################
{{cookiecutter.provider_name|upper}}_PARTNER_ID = {{ {{cookiecutter.provider_name}}.default_partner_id }}
{{cookiecutter.provider_name|upper}}_CONTRACT_ID = '{{ {{cookiecutter.provider_name}}.default_contract_id }}'
{{cookiecutter.provider_name|upper}}_API_SUGAR_CRM_ID = '{{ {{cookiecutter.provider_name}}.default_crm_partner_id }}'
{{cookiecutter.provider_name|upper}}_API_DEFAULT_TERMS = {
    'commission_rsvp_fee': None,
    'commission_paid_percentage': 20,
    'commission_paid_fee': None,
    'vat_percentage': None,
    'kind_of_payment': 'pay_total_purchases',
}

Settings to paste on settings.py

##################################################
#                {{cookiecutter.provider_name|upper}}
##################################################
{{cookiecutter.provider_name|upper}}_PARTNER_ID = 1234
{{cookiecutter.provider_name|upper}}_CONTRACT_ID = 'put crm contract id here'
{{cookiecutter.provider_name|upper}}_API_SUGAR_CRM_ID = 'put crm partner id here'
{{cookiecutter.provider_name|upper}}_API_DEFAULT_TERMS = {
    'commission_rsvp_fee': None,
    'commission_paid_percentage': 20,
    'commission_paid_fee': None,
    'vat_percentage': None,
    'kind_of_payment': 'pay_total_purchases',
}

Block for defaults main.yml file

ingresso:
    default_partner_id: 1234
    default_contract_id: contractidfromcrm
    default_crm_partner_id: partneridfromcrm