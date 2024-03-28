from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query
from web.mutations import mutation
from web.types import product_type

schema_str = (Path(__file__).parent / "products.graphql").read_text()
blindable_objects = [query, mutation, product_type]
schema = make_executable_schema(schema_str, blindable_objects)
