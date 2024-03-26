from pathlib import Path

# TODO import random
# TODO import string

# TODO from ariadne import QueryType
from ariadne import make_executable_schema
from ariadne.asgi import GraphQL

# TODO # A resolver needs to be bound to its corresponding object type.
# TODO # Ariadne provides bindable classes for each GraphQL type: ObjectType,
# TODO # QueryType, MutationType, UnionType, InterfaceType and EnumType.
# TODO query = QueryType()


# TODO @query.field("hello")
# TODO def resolve_hello(*_):
# TODO     """
# TODO     Positional params, see https://ariadnegraphql.org/docs/resolvers.html.
# TODO     The `*_` is a python convention to ignore a list of positional params.
# TODO     """
# TODO     return "".join(random.choice(string.ascii_letters) for _ in range(10))


schema_str = (Path(__file__).parent / "web/products.graphql").read_text()
schema = make_executable_schema(schema_str)

# TODO # To make Ariadne aware of our resolvers, we need to pass our bindable objects as an array to the
# TODO # make_executable_schema() function.
# TODO schema = make_executable_schema(schema_str, [query])

server = GraphQL(schema, debug=True)
