from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query
from web.types import product_type

schema_str = (Path(__file__).parent / "products.graphql").read_text()
blindable_object = [query, product_type]
schema = make_executable_schema(schema_str, blindable_object)
