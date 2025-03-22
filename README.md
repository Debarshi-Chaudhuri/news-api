# 📰 News API

A powerful RESTful API service for India-focused business news, built with FastAPI and Elasticsearch. Designed for speed, scalability, and precision in delivering targeted news content.

## ✨ Features

- **Advanced Search**: Full-text search with India and business focus
- **Content Management**: Create, retrieve, update, and delete news articles
- **Smart Filtering**: Filter by keywords, industry categories, and relevance
- **Automated News Collection**: Background service scrapes and categorizes news
- **Industry Categorization**: News content organized by business sectors
- **User Subscriptions**: DynamoDB-backed subscription management
- **Event Tracking**: Integration with event tracking services
- **Claude AI Integration**: Automated article summarization (optional)
- **Containerized**: Docker-based development and deployment

## 🏗️ System Architecture

The project consists of three main services:

1. **News API**: FastAPI service providing RESTful endpoints
2. **Elasticsearch**: Search engine for storing and querying news articles
3. **Data Populator**: Background service that scrapes and indexes articles

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Setup with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/news-api.git
   cd news-api
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker compose up -d
   ```

4. **Load sample data** (optional)
   ```bash
   docker compose exec news-api python -m scripts.index_data
   ```

The API will be available at `http://localhost:8000`

### Alternative Setup for Individual Services

1. **Create network and start Elasticsearch**
   ```bash
   docker network create news-network
   docker compose -f docker/docker-compose.elasticsearch.yml up -d
   ```

2. **Start the News API**
   ```bash
   docker compose -f docker/docker-compose.news-api.yml up -d
   ```

3. **Start the Data Populator**
   ```bash
   docker compose -f docker/docker-compose.data-populator.yml up -d
   ```

## 📚 API Documentation

Once running, access the API documentation at:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Key Endpoints

#### News Articles
- `GET /api/news/search?q={query}` - Search for news articles
- `GET /api/news/{article_id}` - Get specific article
- `POST /api/news` - Create article
- `PUT /api/news/{article_id}` - Update article
- `DELETE /api/news/{article_id}` - Delete article

#### Keywords and Industries
- `GET /api/keywords` - List available keywords
- `POST /api/keywords/suggest` - Suggest keywords for content
- `GET /api/industries` - List industry categories

#### User Subscriptions
- `GET /api/users/subscriptions/{mobile_number}` - Get subscription
- `POST /api/users/subscriptions` - Create subscription
- `PUT /api/users/subscriptions/{mobile_number}` - Update subscription
- `DELETE /api/users/subscriptions/{mobile_number}` - Delete subscription

#### Other
- `POST /api/scraper/run` - Trigger news scraper
- `GET /api/stats/india-business` - Get news statistics

## 💻 Development

### Local Setup

1. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Elasticsearch via Docker**
   ```bash
   docker compose up elasticsearch
   ```

4. **Start the application**
   ```bash
   uvicorn main:app --reload
   ```

### Debugging

This project includes a VSCode launch configuration. To use it:
1. Open the project in VSCode
2. Go to the Debug tab
3. Select "Python: FastAPI" configuration
4. Press F5 or click the green play button

## 🔧 Configuration

Key environment variables (set in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `False` |
| `ELASTICSEARCH_URL` | Elasticsearch connection URL | `http://localhost:9200` |
| `NEWS_INDEX` | Name of the Elasticsearch index | `news` |
| `ENABLE_NEWS_SCRAPER` | Enable the news scraper | `False` |
| `DYNAMODB_ENDPOINT` | DynamoDB endpoint | `http://localhost:9000` |
| `CLAUDE_API_KEY` | Anthropic Claude API key | `""` |
| `ENABLE_AUTO_SUMMARIZATION` | Enable auto-summarization | `False` |

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

## 📋 Project Structure

See [STRUCTURE.md](STRUCTURE.md) for a detailed project structure overview.

## 🏛️ Architecture Details

See [ARCHITECTURE.md](ARCHITECTURE.md) for a detailed architecture and technology stack overview.

## 💼 Project Focus

This API is specifically designed to focus on Indian business news. The search functionality, data scraper, and article categorization are all optimized to prioritize content related to India and business topics.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/)
- [Elasticsearch](https://www.elastic.co/elasticsearch/)
- [Newspaper3k](https://newspaper.readthedocs.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Docker](https://www.docker.com/)
- [AWS DynamoDB](https://aws.amazon.com/dynamodb/)
- [Anthropic Claude](https://www.anthropic.com/claude)