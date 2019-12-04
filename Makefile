IMAGE ?= projectq

build:
	docker build -t ${IMAGE} .

run:
	docker run --name projq -d -p 8010:8000 -e DJ_SECRET=<set secret here>  projectq