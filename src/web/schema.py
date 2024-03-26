from pathlib import Path

from ariadne import make_executable_schema

from web.queries import query

schema_str = (Path(__file__).parent / "products.graphql").read_text()
schema = make_executable_schema(schema_str, [query])
