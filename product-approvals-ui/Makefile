# Build the Docker image with Docker Compose
build:
	docker-compose build

# Run the Docker container with Docker Compose
run:
	HOSTNAME="http://host.docker.internal:3301" docker-compose up -d

# Push the Docker image to container registry
push:
	docker-compose push

# Deploy the Docker image to Cloud Run
deploy: build push
	gcloud run deploy product-approvals-ui \
		--project international-public-sector \
		--image gcr.io/international-public-sector/product-approvals-ui \
		--platform managed \
		--region me-central1 \
		--set-env-vars "$(shell paste -sd, .env),HOSTNAME=https://permits-api-gf3dkeclfa-ww.a.run.app"

# Stop and remove the Docker container with Docker Compose
stop:
	docker-compose down

# View logs from the container with Docker Compose
logs:
	docker-compose logs -f

# Remove all containers, networks, and images managed by Compose
clean:
	docker-compose down --rmi all

# Access the container's shell
shell:
	docker-compose exec frontend /bin/sh
