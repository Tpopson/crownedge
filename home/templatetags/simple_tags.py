from django import template 
from django.urls import reverse


register = template.Library()


@register.simple_tag()
def intralink(main, link):
    return reverse(main) + '#' + link 















