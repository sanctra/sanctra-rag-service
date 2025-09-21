IMAGE=us-central1-docker.pkg.dev/sanctra-prod/sanctra-docker/sanctra-rag-service:dev

build:
	docker build -t $(IMAGE) .

push:
	docker push $(IMAGE)

run:
	docker run --rm -p 8082:8080 --env-file .env $(IMAGE)
