from django import template

register = template.Library()

@register.simple_tag
def active(request, pattern):
    if request.resolver_match and request.resolver_match.url_name == pattern:
        return "bg-gray-800 text-white"
    return "text-gray-400 hover:bg-gray-800"
