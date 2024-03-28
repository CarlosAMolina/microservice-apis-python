# This file contains resolvers for object types, custom scalar types, and object properties.

from datetime import datetime
import copy

from ariadne import InterfaceType
from ariadne import ObjectType
from ariadne import UnionType
from ariadne import ScalarType

from web import data

product_type = UnionType("Product")
ingredient_type = ObjectType("Ingredient")
product_interface = InterfaceType("ProductInterface")
datetime_scalar = ScalarType("Datetime")


@product_type.type_resolver
def resolve_product_type(obj, *_):
    if "hasFilling" in obj:
        return "Cake"
    return "Beverage"


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


@ingredient_type.field("products")
def resolve_ingredient_products(ingredient, _):
    return [product for product in data.products if product["id"] in ingredient["products"]]


@ingredient_type.field("supplier")
def resolve_ingredient_suppliers(ingredient, _):
    if ingredient.get("supplier") is not None:
        for supplier in data.suppliers:
            if supplier["id"] == ingredient["supplier"]:
                return supplier
