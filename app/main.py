from fastapi import FastAPI
from app.api.icp import router as icp_router
from app.info.appconfig import settings, add_cors_middleware

app = FastAPI()

add_cors_middleware(app)
app.include_router(icp_router, prefix='/icp')

@app.get("/")
async def root():
    return {"message": "Hello World"}
