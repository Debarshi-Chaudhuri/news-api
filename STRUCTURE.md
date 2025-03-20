## Project Structure

```
news-api/
├── .vscode/                  # VSCode configuration
│   └── launch.json           # VSCode debugger configuration
├── app/                      # Main application package
│   ├── __init__.py           # Package initialization
│   ├── api/                  # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py         # API routes definitions
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── config.py         # Application configuration
│   │   └── security.py       # Security-related functionality
│   ├── db/                   # Database related code
│   │   ├── __init__.py
│   │   ├── elasticsearch.py  # Elasticsearch client setup
│   │   └── repositories.py   # Data access layer
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   └── news.py           # News article model
│   └── services/             # Business logic
│       ├── __init__.py
│       └── news_service.py   # News service functionality
├── data/                     # Sample data for populating the database
│   └── sample_news.json      # Sample news articles
├── scripts/                  # Utility scripts
│   ├── __init__.py
│   └── index_data.py         # Script to index sample data into Elasticsearch
├── tests/                    # Test files
│   ├── __init__.py
│   ├── conftest.py           # Pytest configuration
│   ├── test_api.py           # API tests
│   └── test_services.py      # Service tests
├── .env.example              # Example environment variables
├── .gitignore                # Git ignore file
├── main.py                   # Application entry point
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation

```