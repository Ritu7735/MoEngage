# brewery/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def average(queryset, field_name):
    total = sum(getattr(obj, field_name) for obj in queryset)
    count = queryset.count()
    return total / count if count > 0 else 0
