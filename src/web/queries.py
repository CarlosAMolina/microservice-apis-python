from itertools import islice

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

 
@query.field('products')
def resolve_products(*_, input: "ProductsFilter" = None):
    """
    input type is ProductsFilter, see products.graphql
    """
    # Copy the products list.
    filtered = [product for product in data.products]
    if input is None:
        return filtered
    filtered = [
        product for product in filtered
        if product['available'] is input['available']
    ]
    if input.get('minPrice') is not None:
        filtered = [
            product for product in filtered
            if product['price'] >= input['minPrice']
        ]
    if input.get('maxPrice') is not None:
        filtered = [
            product for product in filtered
            if product['price'] <= input['maxPrice']
        ]
    filtered.sort(
        key=lambda product: product.get(input['sortBy'], 0),
        reverse=input['sort'] == 'DESCENDING'
    )
    return get_page(filtered, input['resultsPerPage'], input['page'])


def get_page(items, items_per_page, page):
    page = page - 1
    start = items_per_page * page if page > 0 else page
    stop = start + items_per_page
    return list(islice(items, start, stop))

