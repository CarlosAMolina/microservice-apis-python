run-mock-server:
	docker run -p=9002:9002 -v=${PWD}:/workdir apisguru/graphql-faker schema.graphql
