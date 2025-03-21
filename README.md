# News API

A RESTful API service for news articles focused on Indian business, using Python (FastAPI) and Elasticsearch as the database.

## Features

- Full-text search for news articles with India and business focus
- Create, retrieve, update, and delete news articles
- Advanced filtering by keywords and industry categories
- Automated news scraper that collects articles from the web
- Industry-specific categorization of news content
- Sorting and pagination of search results
- Docker setup for easy development and deployment

## Architecture

The project consists of three main services:

1. **News API**: FastAPI service providing RESTful endpoints
2. **Elasticsearch**: Search and analytics engine for storing and querying news articles
3. **Data Populator**: Background service that scrapes news articles and populates the database

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Elasticsearch**: Search and analytics engine for storing and querying news articles
- **Docker & Docker Compose**: For containerization and easy setup
- **Pydantic**: Data validation and settings management
- **Newspaper3k**: Article extraction and natural language processing
- **NLTK**: Natural language processing for text analysis
- **Pytest**: For testing

## Project Structure

```
news-api/
├── app/                      # Main application package
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   ├── db/                   # Database related code
│   ├── models/               # Data models
│   └── services/             # Business logic
├── data/                     # Sample data
├── docker/                   # Docker configuration files
│   ├── news-api/             # News API service config
│   ├── data-populator/       # Data populator service config
│   └── commands.sh           # Helper script for Docker commands
├── scripts/                  # Utility scripts
├── tests/                    # Test files
└── ... (configuration files)
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+ (for local development without Docker)

### Quick Start with Docker

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/news-api.git
   cd news-api
   ```

2. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

3. Start all services using Docker Compose:
   ```
   docker compose up -d
   ```

4. The API will be available at `http://localhost:8000`

### Alternative Setup with Separate Services

1. Create the Docker network:
   ```
   docker network create news-network
   ```

2. Start Elasticsearch:
   ```
   cd docker
   docker-compose -f docker-compose.elasticsearch.yml up -d
   ```

3. Start the News API:
   ```
   cd docker
   docker-compose -f docker-compose.news-api.yml up -d
   ```

4. Start the Data Populator:
   ```
   cd docker
   docker-compose -f docker-compose.data-populator.yml up -d
   ```

### Loading Sample Data

To load the sample news articles into Elasticsearch:

```
docker compose exec news-api python -m scripts.index_data
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Key Endpoints

#### News Articles

- `GET /api/news/search?q={query}`: Search for news articles
  - Optional parameters: `keyword`, `industry`, `india_focus`, `business_only`, `page`, `limit`, `sort_by`, `sort_order`
- `GET /api/news/{article_id}`: Get a specific news article
- `POST /api/news`: Create a new news article
- `PUT /api/news/{article_id}`: Update an existing news article
- `DELETE /api/news/{article_id}`: Delete a news article

#### Keywords and Industries

- `GET /api/keywords`: Get the list of available keywords
- `POST /api/keywords/suggest`: Suggest keywords for article content
- `GET /api/industries`: Get the list of industry categories and their keywords

#### Scraper Control

- `POST /api/scraper/run`: Manually trigger the news scraper
- `POST /api/scraper/industry`: Manually trigger the industry-specific scraper

#### Stats

- `GET /api/stats/india-business`: Get statistics about Indian business news articles

## Development

### Setting Up a Local Environment

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run Elasticsearch via Docker:
   ```
   docker compose up elasticsearch
   ```

4. Run the application:
   ```
   uvicorn main:app --reload
   ```

### Debugging with VSCode

This project includes a VSCode launch configuration for debugging. To use it:

1. Open the project in VSCode
2. Navigate to the Debug tab
3. Select "Python: FastAPI" configuration
4. Press F5 or click the green play button

## Managing Docker Services

The project includes helper scripts for managing Docker services:

```bash
# View logs
docker compose logs -f  # All services
docker compose logs -f elasticsearch  # Elasticsearch only
docker compose logs -f news-api       # News API only
docker compose logs -f data-populator # Data Populator only

# Stop services
docker compose down  # Stop all services
```

Or use the commands in `docker/commands.sh` for more options.

## Environment Variables

Key environment variables that can be set in `.env`:

- `DEBUG`: Enable debug mode (`True` or `False`)
- `ELASTICSEARCH_URL`: Elasticsearch connection URL
- `NEWS_INDEX`: Name of the Elasticsearch index for news articles
- `ENABLE_NEWS_SCRAPER`: Enable the news scraper in the API service
- `SCRAPER_INTERVAL_MINUTES`: Interval for periodic scraping
- `SCRAPER_VERIFY_SSL`: Verify SSL certificates when scraping (`True` or `False`)

See `.env.example` for all available options.

## Testing

To run the tests:

```
pytest
```

## Project Focus

This API is specifically designed to focus on Indian business news. The search functionality, data scraper, and article categorization are all optimized to prioritize content related to India and business topics.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Newspaper3k](https://newspaper.readthedocs.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)