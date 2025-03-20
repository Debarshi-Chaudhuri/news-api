import uvicorn
from app.api.routes import app
from app.core.config import settings
from app.db.elasticsearch import init_elasticsearch, create_index_if_not_exists

@app.on_event("startup")
async def startup_event():
    init_elasticsearch()
    
    await create_index_if_not_exists()
  

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host=settings.HOST, 
        port=settings.PORT,
        reload=settings.DEBUG
    )