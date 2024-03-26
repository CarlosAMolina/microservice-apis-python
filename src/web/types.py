# This file contains resolvers for object types, custom scalar types, and object properties.

from ariadne import UnionType

product_type = UnionType("Product")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if "hasFilling" in obj:
        return "Cake"
    return "Beverage"
