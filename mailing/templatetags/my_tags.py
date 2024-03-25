import os

from django import template

from config.settings import BASE_DIR

register = template.Library()


@register.simple_tag()
def mediapath(val):
    if val:
        # print(os.path.join(BASE_DIR, 'media', val))
        # return os.path.join(BASE_DIR, 'media', val)
        # print(BASE_DIR)
        # print(os.path.join("media", val))
        # return f'{os.path.join("media", val)}'
        return f'/media/{val}'
    return '/media/barbrady.jpg'
