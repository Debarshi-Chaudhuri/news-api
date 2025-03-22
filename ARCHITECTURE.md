# Architecture & Tech Stack

This document provides a comprehensive overview of the News API's architecture and technology choices.

## System Architecture

The News API is built using a microservices-based architecture consisting of three primary services that work together to provide a complete system for collecting, storing, and retrieving news articles.

### Architecture Diagram

```
┌───────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│                   │     │                  │     │                 │
│   News API        │◄────┤  Elasticsearch   │◄────┤  Data Populator │
│   (FastAPI)       │     │  (Search Engine) │     │  (Scraper)      │
│                   │     │                  │     │                 │
└─────────┬─────────┘     └──────────────────┘     └─────────────────┘
          │
          │
          ▼
┌─────────────────────┐
│                     │
│   DynamoDB          │
│   (User Subscrip.)  │
│                     │
└─────────────────────┘
          │
          │
          ▼
┌─────────────────────┐
│                     │
│   Event Service     │
│   (WebEngage)       │
│                     │
└─────────────────────┘
```

### Components

1. **News API Service (FastAPI)**
   - Provides RESTful API endpoints for clients
   - Handles article CRUD operations
   - Manages user subscriptions
   - Implements business logic for search and filtering

2. **Elasticsearch**
   - Stores news articles in a searchable index
   - Provides full-text search capabilities
   - Handles complex queries and filtering
   - Enables fast retrieval of articles

3. **Data Populator Service**
   - Scrapes news articles from various sources
   - Processes and categorizes articles
   - Indexes articles in Elasticsearch
   - Runs on a scheduled basis to keep content fresh

4. **DynamoDB**
   - Stores user subscription information
   - Provides fast key-value access for user data
   - Scales horizontally for subscription management

5. **Event Service Integration**
   - Tracks user events and subscriptions
   - Integrates with external analytics systems
   - Enables user engagement tracking

### Data Flow

1. **Article Collection**
   - Data Populator scrapes web sources for news articles
   - Articles are processed, categorized, and tagged
   - Articles are indexed in Elasticsearch with metadata

2. **Article Retrieval**
   - Clients query the News API with search parameters
   - API translates requests into Elasticsearch queries
   - Elasticsearch executes search and returns matches
   - API formats and returns results to clients

3. **User Subscriptions**
   - Users subscribe via API endpoints
   - Subscription data is stored in DynamoDB
   - Event tracking data is sent to Event Service
   - Notifications can be triggered based on subscriptions

## Technology Stack

### Backend Framework

- **FastAPI**: A modern, high-performance Python web framework for building APIs
  - Automatic OpenAPI/Swagger documentation
  - Data validation with Pydantic
  - Async support for high concurrency
  - Type hints for better code quality

### Databases

- **Elasticsearch (7.x+)**: Search engine for storing and querying news articles
  - Full-text search capabilities
  - Complex query support
  - Faceting and aggregation for analytics
  - Scalable document storage

- **Amazon DynamoDB**: NoSQL database for user subscriptions
  - Key-value storage for fast retrieval
  - Highly available and scalable
  - Pay-per-request pricing model

### Web Scraping & Processing

- **Newspaper3k**: Article extraction library
  - Extracts article content from HTML
  - Identifies article metadata
  - Basic natural language processing

- **NLTK**: Natural Language Toolkit for text processing
  - Used for keyword extraction
  - Text summarization support
  - Language identification

- **Beautiful Soup**: HTML parsing library
  - Used for scraping search results
  - Extracts links from web pages

### Containerization

- **Docker**: Container runtime
  - Consistent development and production environments
  - Isolated services
  - Easy deployment

- **Docker Compose**: Multi-container orchestration
  - Service definition and configuration
  - Network management
  - Volume management for persistence

### AI Integration

- **Claude API (Anthropic)**: AI-powered article summarization
  - Generates concise article summaries
  - Extracts key points from lengthy content
  - Language understanding capabilities

### Event Tracking

- **WebEngage Integration**: User event tracking
  - Subscription events
  - User profile management
  - Analytics capabilities

## Design Patterns & Principles

### Repository Pattern

The application uses the repository pattern to separate data access logic from business logic:

- **NewsRepository**: Handles CRUD operations for news articles
- **UserSubscriptionRepository**: Manages user subscription data

### Service Layer Pattern

Business logic is encapsulated in service classes:

- **NewsService**: Article operations and search
- **ScraperService**: Web scraping functionality
- **SummarizerService**: Article summarization
- **EventService**: Event tracking
- **UserSubscriptionService**: Subscription management

### Dependency Injection

FastAPI's dependency injection system is used for:

- Database connections
- API key authentication
- Configuration settings

### Separation of Concerns

The application is structured to separate different responsibilities:

- **Models**: Data representation
- **Repositories**: Data access
- **Services**: Business logic
- **API Routes**: Request handling
- **Background Tasks**: Asynchronous processing

## Scalability Considerations

### Horizontal Scaling

- **Stateless API Service**: Can be scaled horizontally
- **Elasticsearch Cluster**: Supports multi-node configuration
- **DynamoDB**: Auto-scaling capabilities

### Background Processing

- Asynchronous scraping tasks
- Non-blocking I/O with async/await
- Task queue for heavy processing

### Query Optimization

- Efficient Elasticsearch mapping
- Custom analyzers for Indian business context
- Strategic indexing of frequently searched fields

## Security Aspects

### API Authentication

- API Key authentication system
- Role-based access control (RBAC) capability

### Data Protection

- Input validation using Pydantic models
- Protection against common web vulnerabilities
- Secure handling of sensitive user data

### Environment Configuration

- Secrets management via environment variables
- Configuration isolation between environments
- No hardcoded credentials

## Deployment Architecture

### Docker-based Deployment

```
┌─────────────────────────────────────────────────────────┐
│                       Docker Host                       │
│                                                         │
│  ┌─────────────┐  ┌───────────────┐  ┌───────────────┐  │
│  │             │  │               │  │               │  │
│  │  News API   │  │ Elasticsearch │  │Data Populator │  │
│  │  Container  │  │   Container   │  │   Container   │  │
│  │             │  │               │  │               │  │
│  └─────────────┘  └───────────────┘  └───────────────┘  │
│                                                         │
│  ┌─────────────┐  ┌───────────────┐                     │
│  │             │  │               │                     │
│  │  DynamoDB   │  │   Volumes     │                     │
│  │  Container  │  │  (Persistent) │                     │
│  │             │  │               │                     │
│  └─────────────┘  └───────────────┘                     │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Network Configuration

- Internal Docker network for service communication
- Exposed ports for external access
- Reverse proxy capability for production

### Persistence

- Docker volumes for Elasticsearch data
- Docker volumes for DynamoDB data (local development)
- AWS DynamoDB for production

## Monitoring & Logging

### Logging

- Structured logging with Python's logging module
- Log levels for different environments
- Service identification in logs

### Health Checks

- API health endpoint (/health)
- Docker health checks for containers
- Database connection validation

## Integration Points

### External Services

- **Claude API**: For article summarization
- **WebEngage**: For event tracking
- **News Sources**: Web scraping targets

### API Consumers

- Web applications
- Mobile applications
- Integration with other services

## Future Architecture Considerations

### Potential Enhancements

1. **Caching Layer**
   - Redis for frequently accessed data
   - Query result caching

2. **Message Queue**
   - RabbitMQ/Kafka for reliable event processing
   - Decoupling services further

3. **Serverless Functions**
   - AWS Lambda for specific processing tasks
   - Reduced operational overhead

4. **Content Delivery Network (CDN)**
   - Caching static content
   - Reducing latency for global users

5. **Machine Learning Pipeline**
   - Enhanced article categorization
   - Personalized news recommendations
   - Sentiment analysis of articles

### Scaling Strategy

- Containerized deployment to Kubernetes
- Autoscaling based on load
- Multi-region deployment for global reach