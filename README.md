# Microservice APIs

## Introduction

Microservice APIs. Using Python, Flask, FastAPI, OpenAPI and more

This project is the code of the book [Microservice APIs](https://www.manning.com/books/microservice-apis).

## Terminology

## Type system

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
}
```

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


## Run

### GraphQL Faker

```bash
make run-mock-server
```

GraphQL Faker normally runs on port 9002, and it exposes three endpoints:

- /editor: interactive editor to develop the GraphQL API.
- [/graphql](http://localhost:9002/graphql): GraphiQL interface to run queries.
- /voyager: displays the relationships and dependencies of the types in the API.

### Queries

Run the following queries in [GraphiQL](http://localhost:9002/graphql).

### Query without parameters

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

### Query with parameters

```bash
{
  ingredient(id: "asdf") {
    name
  }
}
```

### Fragments

Required when a query returns multiple types. For example, `allProducts()` returns the `Product` union type, which is the combination of the `Cake` and `Beverage` types.

Without fragments, the query will fail, and allow us to query properties that not appear in all types.

#### Inline fragments

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

#### Standalone fragments

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

### Using input parameters

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

## Resources

Book:

https://www.manning.com/books/microservice-apis

Book's code:

https://github.com/abunuwas/microservice-apis/tree/master

GraphQL Faker

https://github.com/graphql-kit/graphql-faker?tab=readme-ov-file
