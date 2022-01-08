import random
import string
from random import randint
from django.utils.text import slugify

def number_generator(size=10, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def order_id_generator(instance):
    order_id = number_generator()
    klass = instance.__class__

    qs_exists = klass.objects.filter(
        order_id=order_id
    ).exists()

    if qs_exists:
        return order_id_generator(instance)

    return order_id

def order_number_generator(instance):
    order_number = f"#FB{number_generator(size=6)}"
    klass = instance.__class__

    qs_exists = klass.objects.filter(
        order_id=order_number
    ).exists()

    if qs_exists:
        return order_number_generator(instance)

    return order_number


def product_id_generator(instance):
    product_id = number_generator()
    klass = instance.__class__

    qs_exists = klass.objects.filter(
        product_id=product_id
    ).exists()

    if qs_exists:
        return product_id_generator(instance)

    return product_id