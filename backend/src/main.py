from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database.core import create_db_and_tables 

from src.logging import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kortly application")
    logger.info("Creating database tables if they do not exist")
    create_db_and_tables()
    logger.info("Kortly application is ready to serve requests")
    yield
    logger.info("Shutting down Kortly application")

app = FastAPI(title="Kortly",
            description="A URL shortening service built with FastAPI",
            version="1.0.0",
            lifespan=lifespan)


@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to Kortly!"}