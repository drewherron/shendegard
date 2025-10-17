"""
Shendegard - NLP-Powered Multilingual Threat Intelligence Platform

Main FastAPI application entry point.
"""

from fastapi import FastAPI
from config.settings import settings

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


@app.on_event("startup")
async def startup_event():
    """Application startup tasks."""
    print(f"Starting {settings.app_name} v{settings.version}")
    print(f"Debug mode: {settings.debug}")
    print(f"Documentation available at http://{settings.host}:{settings.port}/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks."""
    print(f"Shutting down {settings.app_name}")


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
