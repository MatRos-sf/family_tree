from django import template

from member.models import Person

register = template.Library()

@register.simple_tag
def count_members() -> int:
    return Person.objects.count()   #is active

