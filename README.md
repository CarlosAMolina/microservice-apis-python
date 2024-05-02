# Microservice APIs

## Introduction

Microservice APIs. Using Python, Flask, FastAPI, OpenAPI and more

This project is the code of the book [Microservice APIs](https://www.manning.com/books/microservice-apis).

## Theory

### GraphQL

Is a popular protocol for building web APIs.

Advantages:

- Gives API clients full control over the data to fetch.
- Good for situations with highly interconnected data.

### Schema

We use SQL to define schemas for our database tables and we can use GraphQL to write specifications that describe the type of data that can be queried from our servers.


For example, the API specification is the file `src/web/products.graphql`.

The specification defines:

- A collection of object types.
- Queries and mutations.

A GraphQL API specification is called a schema, and it’s written in a standard called Schema Definition Language (SDL). Note that the object types can be called schemas or schema model too.

### Type system (object types and properties)

Each of the resources (entities) managed by the API is modeled as object type.

An object type is a collection of properties.

To define a property we indicate its name and type. The type is defined using GraphQL scalars (String, Int, Float, Boolean, and ID). We can define custom scalars (example: date, URL, email address).

To create a custom scalar, we need to define how the scalar type is validated and serialized in the server implementation.

Example of object type with properties and a custom scalar:

```bash
scalar Datetime

type Cake {
  id: ID!
  name: String!
  price: Float
  available: Boolean!
  scalar Datetime!
  comments: [String!]
}
```

Properties that are collections of items are defined with lists, that are arrays of types, defined with square brackets (`[` and `]`).

The exclamation point `!` means not null. Example of allowed values when using `!` in list properties:

|                | [Word] | [Word!] | [Word]! | [Word!]!
|----------------|--------|---------|---------|----------
| null           | Valid  | Valid   | Invalid | Invalid
| []             | Valid  | Valid   | Valid   | Valid
| ["word"]       | Valid  | Valid   | Valid   | Valid
| [null]         | Valid  | Invalid | Valid   | Invalid
| ["word", null] | Valid  | Invalid | Valid   | Invalid


### Connections between types

#### Using edge properties

Properties that point to another type an connects these types.

Example, connect the `Ingredient` type with the `Supplier` type by adding a property called `supplier` to `Ingredient` that points to `Supplier`.


```bash
type Ingredient {
  id: ID!
  name: String!
  supplier: Supplier!
}

type Supplier {
    id: ID!
    name: String!
}
```

This is an example of one-to-one direct connection.

To create a bidirectional and one-to-many connection modifying the `Supplier` type:

```bash
type Supplier {
    id: ID!
    name: String!
    ingredients: [Ingredient!]!
}
```

#### Using through types

With edge property we know the ingredients of a product but no the quantity of the ingredient, we can create a `throught type` to solve this:

```bash
type IngredientRecipe {
  ingredient: Ingredient!
  quantity: Float!
}

type Cake {
  name: String!
  ingredients: [IngredientRecipe!]!
}
```

### Combine types with unions and interfaces

In GraphQL we can bring various types together under a single type with unions and interfaces. This makes the API easier to consume and maintain.

#### Interfaces

Allow to define common properties of various types.

Example:

```bash
interface ProductInterface {
  id: ID!
  name: String!
  price: Float
}

type Cake implements ProductInterface{
  id: ID!
  name: String!
  price: Float
  hasFilling: Boolean!
}

type Beverage implements ProductInterface {
  id: ID!
  name: String!
  price: Float
  hasServeOnIceOption: Boolean!
}
```

#### Union

Allow to bring various types under the same type.

Example, `Cacke` and `Beverage` can be treated as a single `Product` type:

```bash
type Cake implements ProductInterface {
  id: ID!
  name: String!
}

type Beverage implements ProductInterface {
  id: ID!
  name: String!
}

union Product = Beverage | Cake
```

### Enumerations

Constrain the values.

Example:

```bash
enum MeasureUnit {
  LITRES
  KILOGRAMS
  UNITS
}

type IngredientRecipe {
    ingredient: Ingredient!
    quantity: Float!
    unit: MeasureUnit!
}
```

### Query document

Is all the text written required to run a Query or a Mutation. If we use parametrized queries and mutations (see the corresponding section), the JSON used as input is not part of the query document; in GraphiQL, these mutation parameters are part of the `Query variables` section.

Example:

```bash
mutation {
  addProduct(name: "Mocha", type: beverage, input: {price: 10, size: BIG, ingredients: [{ingredient: 1, quantity: 1, unit: LITRES}]}) {
    ...commonProperties
  }
}

fragment commonProperties on ProductInterface {
  name
}
```

GraphQL queries (queries and mutations) are HTTP requests that uses GET or POST methods with a query document.

If the request is send using:

- GET method, the query document is sent using URL query parameters. The query document must be URL encoded (for example, with cURL you have to use `--data-urlencode`, but Python do it automatically with the `requests` library).
- POST method, the query document is included in the request payload.

### Queries

Operations to read data.

In GraphQL, the query type represents the collection of all queries available in a schema.

Example of queries definition one does take any parameters and the other takes one:

```bash
type Query {
  allProducts: [Products!]!
  products(available: Boolean = true, maxPrice: Float): Product
}
```

Refactor the parameters using input types:

```bash
input ProductsFilter {
  available: Boolean = true
  maxPrice: Float
}

type Query {
  allProducts: [Products!]!
  products(inpunt ProductsFilter): Product
}
```

#### Run Queries

Run the following queries in [GraphiQL](http://localhost:9002/graphql). See the `Run` section to start the server.

#### Query without parameters

```bash
{
  allIngredients {
    name
  }
}
```

#### Query with parameters

```bash
{
  ingredient(id: "asdf") {
    name
  }
}
```

#### Fragments


Required when a query returns multiple types. For example, `allProducts()` returns the `Product` union type, which is the combination of the `Cake` and `Beverage` types.

Without fragments, the query will fail.

Fragments are selections of properties on a specific type. We can request properties that not appear in all types (see the following examples).

Fragments are prefixed by the spread operator (three dots).

##### Inline fragments

Syntax: `... on`.

An inline fragment is an anonymous selection set on a specific type.

```bash
{
  allProducts {
    ...on ProductInterface {
      name
    }
    ...on Cake {
      hasFilling
    }
    ...on Beverage {
      hasCreamOnTopOption
    }
  }
}
```

##### Standalone fragments

It is like refactoring the inline fragment. The queries are more clean.

```bash
{
  allProducts {
    ...commonProperties
    ...cakeProperties
    ...beverageProperties
  }
}

fragment commonProperties on ProductInterface {
  name
}

fragment cakeProperties on Cake {
  hasFilling
}

fragment beverageProperties on Beverage {
  hasCreamOnTopOption
}
```

#### Using input parameters

Input parameters are similar to object types, but they’re meant for use as parameters for a GraphQL query or mutation.

Example:
- query with input type parameters: `products`.
- query with parameter: `product`.

```bash
input ProductsFilter {
    maxPrice: Float
    resultsPerPage: Int = 10
    page: Int = 1
}

type Query {
    products(input: ProductsFilter!): [Product!]!
    product(id: ID!): Product
}
```

Input type parameters requires to use `{` and `}`.

Example. Call the `products()` query using `ProductsFilter’s` `maxPrice` parameter:

```bash
{
  products(input: {maxPrice: 10}) {
    ...on ProductInterface {
      name
    }
  }
}
```

Pagination example:

```bash
{
  products(input: {resultsPerPage: 1, page: 1}) {
    ...on ProductInterface {
      name
    }
  }
}
```

#### Request custom scalar types

Example Datetime:

```bash
{
  allProducts {
    ...on ProductInterface {
      name,
      lastUpdated
    }
  }
}
```

#### Navigating the API Graph

To query a property that points to another object type, we use a nested selector:

Examples:


```bash
{
  allIngredients {
    name
    stock {
      unit
    }
  }
}
```

```bash
{
  allProducts {
    ...on ProductInterface {
      name
      ingredients {
        ingredient {
          name
          supplier {
            name
          }
        }
      }
    }
  }
}
```

This is and advantage over REST where multiple queries would be required.

#### Run multiple queries within a single request

We can run multiple queries within the same request, and the response will contain one dataset for each query.

Example:

```bash
{
  allProducts {
    ...commonProperties
  }
  allIngredients {
    name
  }
}

fragment commonProperties on ProductInterface {
  name
}
```

#### Aliasing the queries

Create aliases for the responses returned by the server means changing the key under which the dataset returned by the server is indexed. This can improve the readability of the results. The previous queries are anonymous queries, where the data returned by the server appears under a key named after the name of the query we’re calling.

Example, rename the results of each query, the result of `allProducts()` appears under the `product` alias, and the result of the `allIngredients()` query appears under the `ingredients` alias:

```bash
{
  products: allProducts {
    ...commonProperties
  }
  ingredients: allIngredients {
    name
  }
}

fragment commonProperties on ProductInterface {
  name
}
```

If you use the same query multiple times in the same request, with different filters, they must be aliased to avoid errors when retrieving duplicated keys.

#### Query with cURL

```bash
curl http://localhost:9002/graphql --data-urlencode 'query={allIngredients{name}}'
```

#### Query with Python

```bash
python src/request.py
```

### Mutations

Mutations are operations to change the state of the server. Returns a scalar or an object.

Example:

```bash
enum ProductType {
  cake
  beverage
}

type Mutation {
  addProduct(
    name: String!
    type: ProductType!
    price: String
  ): Product!
}
```

Refactor the parameters using input types:

```bash
input AddProductsInput {
  type: ProductType!
  price: String
}

enum ProductType {
  cake
  beverage
}

type Mutation {
  addProduct(
    name: String!
    input: AddProductsInput
  ): Product!
}
```

#### Run mutations

To use mutations, start the query document by qualifying the operation as a `mutation`.

##### Mutations that return a scalar

We don't need to use a selection set.

Example. Returns a boolean:

```bash
mutation {
  deleteProduct(id: "asdf")
}
```

##### Mutations that return an object type

We must include a selection set.

For example, `addProduct()` returns a value of type `Product` that is the union of the `Cake` and `Beverage` types, so our selection set must use fragments to indicate which type’s properties we want to include in our return payload, we select the `name``property on the `ProductInterface` type:

```bash
mutation {
  addProduct(name: "Mocha", type: beverage, input: {price: 10, size: BIG, ingredients: [{ingredient: 1, quantity: 1, unit: LITRES}]}) {
    ...commonProperties
  }
}

fragment commonProperties on ProductInterface {
  name,
  id
}
```

### Parametrized queries and mutations

Previosly we pass each value in the parameter of the function, with parametrized queries the query document is easier to read and maintain because we decouple the query/mutation calls from the data.

To work with parametrized queries and mutations:

- First:
  - We create a function wrapper around the query/mutation.
  - The parameterized arguments/variables carry a leading dollar ($) sign.
  - In the wrapper signature, we specify the type of the parametrized arguments. In the following example, the wrapper is `CreateProduct`.
  - The parameters of the query/mutation has been parametrized. See the parameters of the `addProduct` mutation in the following example.
- After that, we assign values for the query/mutation parameters in a query variables object, this is a JSON document.

For example, if we parametrize the `addProduct` mutation call:

```bash
type Mutation {
    addProduct(name: String!, type: ProductType!, input: AddProductInput!): Product!
}
```

The parametrized result is:

```bash
# Query document
mutation CreateProduct(
  $name: String!
  $type: ProductType!
  $input: AddProductInput!
) {
  addProduct(name: $name, type: $type, input: $input) {
    ...commonProperties
  }
}

fragment commonProperties on ProductInterface {
  name
}
# Query variables (in GraphiQL we set these query variables within the Query Variables panel)
{
  "name": "Mocha",
  "type": "beverage",
  "input": {
    "price": 10,
    "size": "BIG",
    "ingredients": [{"ingredient": 1, "quantity": 1, "unit": "LITRES"}]
  }
}
```

We can wrapping more than one queries or mutations within the same query document. In these cases, all the parameterized arguments must be defined within the wrapper’s function signature. Example to create and delete:

```bash
# Query document
mutation CreateAndDeleteProduct(
  $name: String!
  $type: ProductType!
  $input: AddProductInput!
  $id: ID!
) {
  addProduct(name: $name, type: $type, input: $input) {
    ...commonProperties
  }
  deleteProduct(id: $id)
}

fragment commonProperties on ProductInterface {
  name
}
# Query variables
{
  "name": "Mocha",
  "type": "beverage",
  "input": {
    "price": 10,
    "size": "BIG",
    "ingredients": [{"ingredient": 1, "quantity": 1, "unit": "LITRES"}]
  },
  "id": "asdf"
}
```

### Selection set

When a query or mutation returns an object type, the query must include a selection set. This is a list of the properties we want to fetch from the object returned by the query.

### Resolvers

Resolvers are Python functions that implement the logic of a query or mutation.

By convention, we prefix our resolvers’ names with `resolve_`.

A resolver needs to be bound to its corresponding object type, we do it with decorators. Ariadne provides bindable classes for each GraphQL type:

- ObjectType
- QueryType
- MutationType
- UnionType
- InterfaceType
- EnumType

To make Ariadne aware of our resolvers, we need to pass our bindable objects as an array to the `make_executable_schema()` function (see the `schema.py` file).

#### Query resolvers

Resolvers let the server know how to produce a value for a type or an attribute.

Resolvers are Python functions that know how to return a valid payload for a query.

#### Type resolvers

For queries and mutations that return multiple object types, the server can’t determine what types each of the elements in the list are, we have to implement a type resolver, that is a Python function that determines what type an object is, and it returns the name of the type.

The type resolvers are required in queries and mutations that return union types and object types that implement interfaces.

For example, the `allProducts()` query returns the `Product` type, which is a union of the `Beverage` and `Cake` types, both of which implement the `ProductInterface` type. The `resolve_product_type() indicates the type of the object returned by the `resolve_all_products` resolver.

The type resolver function inspect the properties of the received payload (Ariadne guarantees that the first argument in a resolver is an object) to determine its type.

Example in `web/types.py`.

#### Parameters in resolvers

When a Query o Mutation takes parameters Ariadne parse them to the resolvers as keyword arguments.

Ariadne’s resolvers always get two positional parameters by default: `obj` and `info` (see https://ariadnegraphql.org/docs/resolvers.html), when they are not required, we use the python convention `*_` to omit positional parameters.

#### Resolvers for custom scalar types

For example, datetimes are not a default GraphQL scalar type. To handle them by Ariadne we have to implement a resolver for it.

The server must be able to perform these three actions:

- Serialization: when a user request data to the server, each Python type must be converted to strings, numeric, types, etc.
- Deserialization: when a user send data to the server, Ariadne deserializes it into Python types.
- Validation: GraphQL enforces validation of each scalar and type. Ariadne knows how to validate GraphQL’s built-in scalars, custom scalars validation must be defined.

To perform these actions, Ariadne provides the `ScalarType` class:

- Serialization: we use ScalarType’s serializer() decorator. For example to serialize datetime objects into ISO standard date format, we can use the isoformat() method from the datetime Python library.
- Validation and deserialization: `ScalarType` has the `value_parser()` decorator. For example, for Datetime scalars sent by the user, whe use the Python’s `datetime.fromisoformat()` that will raise an exception if invalid value.

#### Field resolvers

Implement resolvers for the fields of an object type is necessary when working with fields that map to other GraphQL types.

For example, the `Products` type has the field `ingredients` which maps to an array of `IngredientRecipe` which has an `ingredient` field, which maps to an `Ingredient` object type.

Imagine that our data has this value:

```bash
ingredients = [
  {
    'ingredient': '602f2ab3-97bd-468e-a88b-bb9e00531fd0',
    'quantity': 100.00,
    'unit': 'LITRES',
  }
```

The `ingredient` points to an ID instead of an `Ingredient` type and the queries, for example the `allProducts()` query, will fail because the form is incorrect. A solution is to modify the products payload in the resolver defined in `queries.py` by replacing the ingredient's ID with the ingredient, but new Python code is required, we have a better solution that makes easy to maintain the code.

With GraphQL we can create resolvers for specific fields of an object. In the previous example, we should create the `resolve_product_ingredients()` resolver for the `ingredients` property of a `Product`, this new resolver returns a valid payload for the ingredients property of a product.

This is a better approach because:

- Every resolver does only one thing.
- We avoid repetition, having a single resolver that takes care of updating the ingredients property in product payloads, we avoid having to perform this operation in every resolver that returns a product type.

As a downside, property resolvers may be more difficult to trace and debug because the error won't appear in the `allProducts()` resolver, we must know that there is a resolver for products’ ingredients.

## Run

### GraphQL Faker

The GraphQL Faker’s mock server only accepts GET requests.

```bash
make run-mock-server
```

GraphQL Faker normally runs on port 9002, and it exposes three endpoints:

- /editor: interactive editor to develop the GraphQL API.
- [/graphql](http://localhost:9002/graphql): GraphiQL interface to run queries.
- /voyager: displays the relationships and dependencies of the types in the API.

## Endpoints

```bash
{
  allIngredients {
    id
    name
    stock {
      quantity
      unit
    }
    products {
      ... on ProductInterface {
        id
        name
        price
        size
        available
        lastUpdated
      },
      ... on Beverage {
        hasCreamOnTopOption
        hasServeOnIceOption
      }
      ... on Cake {
        hasFilling
        hasNutsToppingOption
      }
    }
    supplier {
      id
      name
      address
      contactNumber
      email
    }
    description
    lastUpdated
  }
}
```

## Resources

[Book](https://www.manning.com/books/microservice-apis)

[Book's code](https://github.com/abunuwas/microservice-apis/tree/master)

[GraphQL Faker](https://github.com/graphql-kit/graphql-faker?tab=readme-ov-file)

[Python frameworks](https://graphql.org/code/):

- The Ariadne framework, to build an API. Is one of the most popular Python GraphQL libraries. It follows a schema-first approach, which means we first design the API, and then we implement the server against the specification. It can handle schema, request a response validations directly using the specification.

Python clients:

- [gpl](https://github.com/graphql-python/gql)

