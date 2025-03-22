```

news-api/
├── app/                      # Main application package
│   ├── api/                  # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py         # API routes definitions
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── background.py     # Background task management
│   │   ├── config.py         # Application configuration
│   │   ├── constants.py      # Application constants
│   │   ├── nltk_init.py      # NLTK resource management
│   │   ├── security.py       # API key authentication
│   │   ├── url_utils.py      # URL handling utilities
│   │   └── utils.py          # General utilities
│   ├── db/                   # Database layer
│   │   ├── __init__.py
│   │   ├── dynamodb.py       # DynamoDB client setup
│   │   ├── elasticsearch.py  # Elasticsearch client setup
│   │   ├── news_repository.py # News data access
│   │   └── user_repository.py # User data access
│   ├── models/               # Data models
│   │   ├── __init__.py
│   │   ├── news.py           # News article models
│   │   ├── user.py           # User subscription models
│   │   └── responses/        # API response models
│   │       ├── __init__.py
│   │       └── news.py       # News response models
│   └── services/             # Business logic
│       ├── __init__.py
│       ├── event_service.py  # Event tracking service
│       ├── news_service.py   # News article operations
│       ├── scraper_service.py # News scraping functionality
│       ├── summarizer_service.py # Article summarization
│       └── user_subscription_service.py # User subscription management
├── data/                     # Sample data
│   └── sample_news.json      # Sample news articles
├── docker/                   # Docker configuration
│   ├── news-api/             # News API service
│   │   └── Dockerfile        # News API container definition
│   ├── data-populator/       # Data populator service
│   │   └── Dockerfile        # Data populator container definition
│   ├── dynamodb/             # DynamoDB service
│   │   └── Dockerfile        # DynamoDB container definition
│   ├── docker-compose.elasticsearch.yml # Elasticsearch service definition
│   ├── docker-compose.news-api.yml      # News API service definition
│   ├── docker-compose.data-populator.yml # Data populator service definition
│   ├── docker-compose.dynamodb.yml      # DynamoDB service definition
│   └── commands.sh           # Helper script for Docker commands
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
├── requirements.txt          # Project dependencies
├── README.md                 # Project documentation
├── STRUCTURE.md              # This file - project structure documentation
└── ARCHITECTURE.md           # Architecture and tech stack documentation

```