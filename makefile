run-mock-server:
	docker run --rm -d -p=9002:9002 -v=${PWD}/src/web:/workdir apisguru/graphql-faker schema.graphql
