"""
:Created: 12 March 2016
:Author: Lucas Connors

"""

import mock

from perdiem.tests import PerDiemTestCase


class CampaignAdminWebTestCase(PerDiemTestCase):

    def get200s(self):
        return [
            '/admin/campaign/',
            '/admin/campaign/campaign/',
            '/admin/campaign/campaign/add/',
            '/admin/campaign/campaign/{campaign_id}/change/'.format(campaign_id=self.campaign.id),
            '/admin/campaign/investment/',
            '/admin/campaign/revenuereport/',
            '/admin/campaign/revenuereport/add/',
            '/admin/campaign/revenuereport/{revenue_report_id}/change/'.format(revenue_report_id=self.revenue_report.id),
        ]

    def testCampaignRaisingZeroIsAlreadyFunded(self):
        self.campaign.amount = 0
        self.campaign.save()
        self.assertEquals(self.campaign.percentage_funded(), '100')


class CampaignWebTestCase(PerDiemTestCase):

    @mock.patch('pinax.stripe.webhooks.Webhook.validate')
    @mock.patch('pinax.stripe.views.Webhook.extract_json')
    @mock.patch('stripe.Charge.create')
    @mock.patch('stripe.Customer.create')
    def testInvestInCampaign(self, mock_stripe_customer_create, mock_stripe_charge_create, mock_pinax_stripe_webhook_extract_json, mock_pinax_stripe_webhook_validate):
        # Mock responses from Stripe
        mock_stripe_customer_create.return_value = {
            'account_balance': 0,
            'business_vat_id': None,
            'created': 1462665000,
            'currency': None,
            'default_source': 'card_2CXngrrA798I5wA01wQ74iTR',
            'delinquent': False,
            'description': None,
            'discount': None,
            'email': self.USER_EMAIL,
            'id': 'cus_2Pc8xEoaTAnVKr',
            'livemode': False,
            'metadata': {},
            'object': 'customer',
            'shipping': None,
            'sources': {
                'data': [
                    {
                        'address_city': None,
                        'address_country': None,
                        'address_line1': None,
                        'address_line1_check': None,
                        'address_line2': None,
                        'address_state': None,
                        'address_zip': None,
                        'address_zip_check': None,
                        'brand': 'Visa',
                        'country': 'US',
                        'customer': 'cus_2Pc8xEoaTAnVKr',
                        'cvc_check': 'pass',
                        'dynamic_last4': None,
                        'exp_month': 5,
                        'exp_year': 2019,
                        'fingerprint': 'Lq9DFkUmxf7xWHkn',
                        'funding': 'credit',
                        'id': 'card_2CXngrrA798I5wA01wQ74iTR',
                        'last4': '4242',
                        'metadata': {},
                        'name': self.USER_EMAIL,
                        'object': 'card',
                        'tokenization_method': None,
                    },
                ],
                'has_more': False,
                'object': 'list',
                'total_count': 1,
                'url': '/v1/customers/cus_2Pc8xEoaTAnVKr/sources',
            },
            'subscriptions': {
                'data': [],
                'has_more': False,
                'object': 'list',
                'total_count': 0,
                'url': '/v1/customers/cus_2Pc8xEoaTAnVKr/subscriptions',
            },
        }
        mock_stripe_charge_create.return_value = {
            'amount': 235,
            'amount_refunded': 0,
            'application_fee': None,
            'balance_transaction': 'txn_Sazj9jMCau62PxJhOLzBXM3p',
            'captured': True,
            'created': 1462665010,
            'currency': 'usd',
            'customer': 'cus_2Pc8xEoaTAnVKr',
            'description': None,
            'destination': None,
            'dispute': None,
            'failure_code': None,
            'failure_message': None,
            'fraud_details': {},
            'id': 'ch_Upra88VQlJJPd0JxeTM0ZvHv',
            'invoice': None,
            'livemode': False,
            'metadata': {},
            'object': 'charge',
            'order': None,
            'paid': True,
            'receipt_email': None,
            'receipt_number': None,
            'refunded': False,
            'refunds': {
                'data': [],
                'has_more': False,
                'object': 'list',
                'total_count': 0,
                'url': '/v1/charges/ch_Upra88VQlJJPd0JxeTM0ZvHv/refunds',
            },
            'shipping': None,
            'source': {
                'address_city': None,
                'address_country': None,
                'address_line1': None,
                'address_line1_check': None,
                'address_line2': None,
                'address_state': None,
                'address_zip': None,
                'address_zip_check': None,
                'brand': 'Visa',
                'country': 'US',
                'customer': 'cus_2Pc8xEoaTAnVKr',
                'cvc_check': None,
                'dynamic_last4': None,
                'exp_month': 5,
                'exp_year': 2019,
                'fingerprint': 'Lq9DFkUmxf7xWHkn',
                'funding': 'credit',
                'id': 'card_2CXngrrA798I5wA01wQ74iTR',
                'last4': '4242',
                'metadata': {},
                'name': self.USER_EMAIL,
                'object': 'card',
                'tokenization_method': None,
            },
            'source_transfer': None,
            'statement_descriptor': None,
            'status': 'succeeded',
        }
        mock_pinax_stripe_webhook_extract_json.return_value = {
            'id': 'evt_t00Xx8V4jXhLUbUGPbpUkJlk',
            'object': 'event',
            'api_version': '2015-09-08',
            'created': 1462665020,
            'livemode': False,
            'pending_webhooks': 1,
            'request': 'req_x74Pcl1YdSdR67',
            'type': 'charge.succeeded',
            'data': {
                'object': {
                    'application_fee': None,
                    'livemode': False,
                    'currency': 'usd',
                    'invoice': None,
                    'fraud_details': {},
                    'id': 'ch_Upra88VQlJJPd0JxeTM0ZvHv',
                    'captured': True,
                    'receipt_number': None,
                    'destination': None,
                    'statement_descriptor': None,
                    'source': {
                        'address_state': None,
                        'last4': '4242',
                        'dynamic_last4': None,
                        'address_zip_check': None,
                        'address_country': None,
                        'id': 'card_2CXngrrA798I5wA01wQ74iTR',
                        'address_line2': None,
                        'address_line1': None,
                        'funding': 'credit',
                        'metadata': {},
                        'cvc_check': 'pass',
                        'exp_month': 5,
                        'tokenization_method': None,
                        'address_line1_check': None,
                        'brand': 'Visa',
                        'object': 'card',
                        'fingerprint': 'Lq9DFkUmxf7xWHkn',
                        'exp_year': 2019,
                        'address_zip': None,
                        'customer': 'cus_2Pc8xEoaTAnVKr',
                        'address_city': None,
                        'name': self.USER_EMAIL,
                        'country': 'US',
                    },
                    'balance_transaction': 'txn_Sazj9jMCau62PxJhOLzBXM3p',
                    'source_transfer': None,
                    'receipt_email': None,
                    'metadata': {},
                    'status': 'succeeded',
                    'amount_refunded': 0,
                    'description': None,
                    'refunded': False,
                    'object': 'charge',
                    'paid': True,
                    'failure_code': None,
                    'customer': 'cus_2Pc8xEoaTAnVKr',
                    'refunds': {
                        'has_more': False,
                        'total_count': 0,
                        'object': 'list',
                        'data': [],
                        'url': '/v1/charges/ch_Upra88VQlJJPd0JxeTM0ZvHv/refunds',
                    },
                    'created': 1462665020,
                    'failure_message': None,
                    'shipping': None,
                    'amount': 235,
                    'dispute': None,
                    'order': None,
                },
            },
        }

        # User sends payment to Stripe
        self.assertResponseRenders('/artist/{slug}/'.format(slug=self.artist.slug))
        self.assertResponseRenders(
            '/payments/charge/{campaign_id}/'.format(campaign_id=self.campaign.id),
            status_code=205,
            method='POST',
            data={'card': 'tok_6WqQnRecbRRrqvrdT1XXGP1d', 'num_shares': 1,}
        )

        # Then Stripe responds confirming that the payment succeeded
        self.assertResponseRenders('/payments/webhook/', method='POST')
