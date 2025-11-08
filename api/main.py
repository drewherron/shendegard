"""
Shendegard - NLP-Powered Multilingual Threat Intelligence Platform

Main FastAPI application entry point.
"""

import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.debug else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/app.log')
    ]
)

logger = logging.getLogger(__name__)

# Application metadata
app = FastAPI(
    title=settings.app_name,
    description="""
    **Shendegard** is an NLP-powered multilingual threat intelligence platform that combines
    traditional IOC lookup with deployed machine learning models for entity extraction,
    threat classification, and automated analysis.

    ## Features

    * **IOC Lookup**: Query threat intelligence APIs (VirusTotal, AbuseIPDB, OTX)
    * **NLP Entity Extraction**: Extract IOCs, threat actors, and malware families from text
    * **Multilingual Support**: Process Arabic, German, and English content
    * **MITRE ATT&CK Mapping**: Automated TTP classification from threat descriptions
    * **Threat Scoring**: Aggregate threat intelligence from multiple sources

    ## API Categories

    * **Health**: System health and status endpoints
    * **IOC Lookup**: Domain, IP, hash, and URL reputation checks
    * **NLP**: Entity extraction and text analysis
    * **Search**: Query collected threat intelligence data
    """,
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "Shendegard Project",
        "url": "https://github.com/yourusername/shendegard",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add request processing time to response headers."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}"

    # Log request
    logger.info(
        f"{request.method} {request.url.path} - "
        f"Status: {response.status_code} - "
        f"Time: {process_time:.4f}s"
    )

    return response


@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    logger.info(f"Starting {settings.app_name} v{settings.version}")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Documentation available at http://{settings.host}:{settings.port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    logger.info(f"Shutting down {settings.app_name}")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": settings.app_name,
        "version": settings.version,
        "description": "NLP-powered multilingual threat intelligence platform",
        "documentation": f"http://{settings.host}:{settings.port}/docs",
        "status": "operational"
    }
