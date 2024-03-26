run-mock-server:
	docker run -d -p=9002:9002 -v=${PWD}:/workdir apisguru/graphql-faker schema.graphql
