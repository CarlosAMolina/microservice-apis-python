import random
import string

from ariadne import QueryType, make_executable_schema
from ariadne.asgi import GraphQL

# A resolver needs to be bound to its corresponding object type.
# Ariadne provides bindable classes for each GraphQL type: ObjectType,
# QueryType, MutationType, UnionType, InterfaceType and EnumType.
query = QueryType()


@query.field("hello")
def resolve_hello(*_):
    """
    Positional params, see https://ariadnegraphql.org/docs/resolvers.html.
    The `*_` is a python convention to ignore a list of positional params.
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(10))


schema = """
type Query {
        hello: String
    }
"""

# To make Ariadne aware of our resolvers, we need to pass our bindable objects as an array to the
# make_executable_schema() function.
server = GraphQL(make_executable_schema(schema, [query]), debug=True)