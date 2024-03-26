from ariadne import make_executable_schema
from ariadne.asgi import GraphQL

schema = """
  type Query {
    hello: String
  }
"""

server = GraphQL(make_executable_schema(schema), debug=True)
