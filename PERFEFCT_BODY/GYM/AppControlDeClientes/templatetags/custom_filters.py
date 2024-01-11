from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter(name='replace_comma')
def replace_comma(value):
    return str(value).replace(',', '.')

@register.simple_tag(name='get_comida_image')
def get_comida_image(tiempo):
    if tiempo == 2:
        return static("assets/img/dietas/hora-de-comer.png")
    elif tiempo == 4:
        return static("assets/img/dietas/Pollo.png")
    elif tiempo == 6:
        return static("assets/img/dietas/cena.png")
    else:
        return static("assets/img/dietas/hora-de-la-merienda.png")
