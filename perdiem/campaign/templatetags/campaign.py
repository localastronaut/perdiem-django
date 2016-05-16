"""
:Created: 15 May 2016
:Author: Lucas Connors

"""

from django import template


register = template.Library()


@register.filter
def percentage_roi(campaign, percentage):
    return campaign.percentage_roi(percentage)
