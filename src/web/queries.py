from ariadne import QueryType

from web import data

query = QueryType()


@query.field("allIngredients")
def resolve_all_ingredients(*_):
    """
    Positional params: see https://ariadnegraphql.org/docs/resolvers.html.
    The `*_` is a python convention to ignore a list of positional params.
    """
    return data.ingredients


@query.field("allProducts")
def resolve_all_products(*_):
    return data.products
