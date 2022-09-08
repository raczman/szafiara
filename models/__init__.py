from collections import namedtuple

Item = namedtuple("Item", ['make', 'name', 'price', 'price_alt', 'discount', 'url', 'image', 'shop', 'sizes'])

__all__ = ['Item']