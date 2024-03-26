# Microservice APIs

## Introduction

Microservice APIs. Using Python, Flask, FastAPI, OpenAPI and more

This project is the code of the book [Microservice APIs](https://www.manning.com/books/microservice-apis).

## Theory

### Type system

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

               | [Word] | [Word!] | [Word]! | [Word!]!
---------------|--------|---------|---------|----------
null           | Valid  | Valid   | Invalid | Invalid
[]             | Valid  | Valid   | Valid   | Valid
["word"]       | Valid  | Valid   | Valid   | Valid
[null]         | Valid  | Invalid | Valid   | Invalid
["word", null] | Valid  | Invalid | Valid   | Invalid

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
  LITERS
  KILOGRAMS
  UNITS
}

type IngredientRecipe {
    ingredient: Ingredient!
    quantity: Float!
    unit: MeasureUnit!
}
```

### Queries

Operations to read data.

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

Without fragments, the query will fail, and allow us to query properties that not appear in all types.

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

Call the `products()` query using `ProductsFilter’s` `maxPrice` parameter:

```bash
{
  products(input: {maxPrice: 10}) {
    ...on ProductInterface {
      name
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

## Run

### GraphQL Faker

```bash
make run-mock-server
```

GraphQL Faker normally runs on port 9002, and it exposes three endpoints:

- /editor: interactive editor to develop the GraphQL API.
- [/graphql](http://localhost:9002/graphql): GraphiQL interface to run queries.
- /voyager: displays the relationships and dependencies of the types in the API.

## Resources

Book:

https://www.manning.com/books/microservice-apis

Book's code:

https://github.com/abunuwas/microservice-apis/tree/master

GraphQL Faker

https://github.com/graphql-kit/graphql-faker?tab=readme-ov-file
