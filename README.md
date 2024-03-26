# Microservice APIs

## Introduction

Microservice APIs. Using Python, Flask, FastAPI, OpenAPI and more

This project is the code of the book [Microservice APIs](https://www.manning.com/books/microservice-apis).

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

## Resources

Book:

https://www.manning.com/books/microservice-apis

Book's code:

https://github.com/abunuwas/microservice-apis/tree/master

GraphQL Faker

https://github.com/graphql-kit/graphql-faker?tab=readme-ov-file
