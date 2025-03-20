# News API

A RESTful API service for news articles using Python (FastAPI) and Elasticsearch as the database.

## Features

- Search for news articles with full-text search capabilities
- Create, retrieve, update, and delete news articles
- Sorting and pagination of search results
- Docker setup for easy development and deployment

## Tech Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Elasticsearch**: Search and analytics engine for storing and querying news articles
- **Docker & Docker Compose**: For containerization and easy setup
- **Pydantic**: Data validation and settings management
- **Pytest**: For testing

## Project Structure

```
news-api/
├── .vscode/                  # VSCode configuration
├── app/                      # Main application package
│   ├── api/                  # API endpoints
│   ├── core/                 # Core functionality
│   ├── db/                   # Database related code
│   ├── models/               # Data models
│   └── services/             # Business logic
├── data/                     # Sample data
├── scripts/                  # Utility scripts
├── tests/                    # Test files
└── ... (configuration files)
```

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/news-api.git
   cd news-api
   ```

2. Create a `.env` file from the example:
   ```
   cp .env.example .env
   ```

3. Start the application with Docker Compose:
   ```
   docker compose up
   ```

4. The API will be available at `http://localhost:8000`

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

- `GET /api/news/search?q={query}`: Search for news articles
- `GET /api/news/{article_id}`: Get a specific news article
- `POST /api/news`: Create a new news article
- `PUT /api/news/{article_id}`: Update an existing news article
- `DELETE /api/news/{article_id}`: Delete a news article

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

## Testing

To run the tests:

```
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)