import pytest
from fastapi.testclient import TestClient
from app.models.news import NewsArticleCreate

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
async def test_search_news(test_client, es_client):
    # Create a test article
    article = {
        "title": "Test Article",
        "content": "This is a test article content",
        "summary": "Test summary",
        "author": "Test Author",
        "source": "Test Source",
        "published_date": "2023-01-01T00:00:00Z",
        "categories": ["Test"],
        "tags": ["test"],
        "url": "https://example.com/test",
        "created_at": "2023-01-01T00:00:00Z",
        "updated_at": "2023-01-01T00:00:00Z"
    }
    
    response = await es_client.index(
        index="test_news",
        document=article,
        refresh=True
    )
    
    # Test search
    search_response = test_client.get("/api/news/search?q=test")
    assert search_response.status_code == 200
    data = search_response.json()
    assert data["total"] >= 1
    assert len(data["articles"]) >= 1
    assert data["articles"][0]["title"] == "Test Article"

@pytest.mark.asyncio
async def test_create_and_get_news(test_client):
    # Create a new article
    article_data = {
        "title": "New Test Article",
        "content": "This is new test content",
        "summary": "New test summary",
        "author": "New Author",
        "tags": ["new", "test"]
    }
    
    create_response = test_client.post(
        "/api/news",
        json=article_data
    )
    assert create_response.status_code == 201
    created_article = create_response.json()
    article_id = created_article["id"]
    
    # Get the created article
    get_response = test_client.get(f"/api/news/{article_id}")
    assert get_response.status_code == 200
    retrieved_article = get_response.json()
    assert retrieved_article["id"] == article_id
    assert retrieved_article["title"] == article_data["title"]
    assert retrieved_article["content"] == article_data["content"]

@pytest.mark.asyncio
async def test_update_news(test_client, es_client):
    # Create a test article
    article = {
        "title": "Update Test Article",
        "content": "This is an article to update",
        "summary": "Update test summary"
    }
    
    response = await es_client.index(
        index="test_news",
        document=article,
        refresh=True
    )
    article_id = response["_id"]
    
    # Update the article
    update_data = {
        "title": "Updated Article Title",
        "summary": "Updated summary"
    }
    
    update_response = test_client.put(
        f"/api/news/{article_id}",
        json=update_data
    )
    assert update_response.status_code == 200
    updated_article = update_response.json()
    assert updated_article["id"] == article_id
    assert updated_article["title"] == update_data["title"]
    assert updated_article["summary"] == update_data["summary"]
    assert updated_article["content"] == article["content"]  # Content didn't change

@pytest.mark.asyncio
async def test_delete_news(test_client, es_client):
    # Create a test article
    article = {
        "title": "Delete Test Article",
        "content": "This is an article to delete"
    }
    
    response = await es_client.index(
        index="test_news",
        document=article,
        refresh=True
    )
    article_id = response["_id"]
    
    # Delete the article
    delete_response = test_client.delete(f"/api/news/{article_id}")
    assert delete_response.status_code == 200
    
    # Try to get the deleted article
    get_response = test_client.get(f"/api/news/{article_id}")
    assert get_response.status_code == 404