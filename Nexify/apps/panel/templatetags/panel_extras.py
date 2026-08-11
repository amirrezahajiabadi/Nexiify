# -*- coding: utf-8 -*-
"""فیلترهای سفارشی پنل ادمین."""

from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    """دسترسی به مقدار دیکشنری با کلید متغیر: {{ dict|get_item:var }}"""
    try:
        return mapping.get(key, 0)
    except AttributeError:
        return 0
