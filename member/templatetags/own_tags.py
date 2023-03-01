from django import template
from random import choice

from member.models import Person

register = template.Library()

@register.simple_tag
def count_members() -> int:
    return Person.objects.count()   #is active

@register.simple_tag
def family_quote() -> str:

    quote = ["Family is not an important thing. It's everything.", "The family is one of nature's masterpieces.",
             "A happy family is but an earlier heaven.", "Family means no one gets left behind or forgotten.",
             "In family life, love is the oil that eases friction, the cement that binds closer together, and the music that brings harmony.",
             "The love of family and the admiration of friends is much more important than wealth and privilege."]


    return choice(quote)

