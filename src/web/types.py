# This file contains resolvers for object types, custom scalar types, and object properties.

from datetime import datetime
import copy

from ariadne import InterfaceType
from ariadne import UnionType
from ariadne import ScalarType

from web import data

product_type = UnionType("Product")
product_interface = InterfaceType("ProductInterface")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if "hasFilling" in obj:
        return "Cake"
    return "Beverage"


datetime_scalar = ScalarType("Datetime")


@datetime_scalar.serializer
def serialize_datetime_scalar(date) -> str:
    return date.isoformat()


@datetime_scalar.value_parser
def parse_datetime_scalar(date):
    return datetime.fromisoformat(date)


@product_interface.field("ingredients")
def resolve_product_ingredients(product, _):
    recipe = [copy.copy(ingredient) for ingredient in product.get("ingredients", [])]
    for ingredient_recipe in recipe:
        for ingredient in data.ingredients:
            if ingredient["id"] == ingredient_recipe["ingredient"]:
                ingredient_recipe["ingredient"] = ingredient
    return recipe
