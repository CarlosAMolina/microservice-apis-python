from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query
from web.mutations import mutation
from web import types as custom_types

schema_str = (Path(__file__).parent / "products.graphql").read_text()
blindable_objects = [
    custom_types.datetime_scalar,
    custom_types.ingredient_type,
    custom_types.product_interface,
    custom_types.product_type,
    query,
    mutation,
]
schema = make_executable_schema(schema_str, blindable_objects)
