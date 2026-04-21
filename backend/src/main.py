from fastapi import FastAPI
from src.logging import logger



app = FastAPI(title="Kortly",
            description="A URL shortening service built with FastAPI",
            version="1.0.0")


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Kortly!"}