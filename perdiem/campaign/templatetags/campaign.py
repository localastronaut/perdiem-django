"""
:Created: 15 May 2016
:Author: Lucas Connors

"""

from django import template


register = template.Library()


@register.filter
def percentage_roi(campaign, percentage):
    return campaign.amount * (percentage / campaign.fans_percentage)
