# First create the network (only needed once)
docker network create news-network

# Run Elasticsearch Service
cd docker
docker compose -f docker-compose.elasticsearch.yml up -d

# Run News API Service
cd docker
docker compose -f docker-compose.news-api.yml up -d

# Run Data Populator Service
cd docker
docker compose -f docker-compose.data-populator.yml up -d

# Run All Services Together
cd docker
docker compose up -d

# Build and run specific services
cd docker
docker compose -f docker-compose.elasticsearch.yml up -d --build  # Elasticsearch
docker compose -f docker-compose.news-api.yml up -d --build       # News API
docker compose -f docker-compose.data-populator.yml up -d --build # Data Populator

# Stop services
cd docker
docker compose down  # Stop all services
docker compose -f docker-compose.elasticsearch.yml down  # Stop Elasticsearch
docker compose -f docker-compose.news-api.yml down       # Stop News API
docker compose -f docker-compose.data-populator.yml down # Stop Data Populator

# View logs
cd docker
docker compose logs -f  # All services
docker compose logs -f elasticsearch  # Elasticsearch only
docker compose logs -f news-api       # News API only
docker compose logs -f data-populator # Data Populator only