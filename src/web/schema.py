from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query
from web.mutations import mutation
from web import types as custom_types

schema_str = (Path(__file__).parent / "products.graphql").read_text()
blindable_objects = [query, mutation, custom_types.product_type, custom_types.datetime_scalar]
schema = make_executable_schema(schema_str, blindable_objects)
