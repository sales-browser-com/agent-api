# agent-api-main/app/main.py
from fastapi import FastAPI
from app.api.icp import router as icp_router
from app.api.search import router as search_router # Import the new search router
from app.info.appconfig import settings, add_cors_middleware

app = FastAPI()

add_cors_middleware(app)

app.include_router(icp_router, prefix='/icp', tags=['ICP Agent'])
app.include_router(search_router, prefix='/search', tags=['Search Agent']) # Add the search router

@app.get("/")
async def root():
    return {"message": "Hello World - ICP and Search Agents API"}