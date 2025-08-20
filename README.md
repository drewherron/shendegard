# Shendegard

A simple API that takes IOCs (domains, IPs, hashes, URLs) and checks them against multiple threat intelligence sources.

## What it does

- Query VirusTotal, AbuseIPDB, and AlienVault OTX from a single API
- Cache results with Redis to avoid redundant lookups
- Return standardized threat scores and metadata
- Handle rate limiting so you don't hit API limits

## Basic usage

```
GET /check/domain/example.com
GET /check/ip/1.2.3.4
GET /check/hash/d41d8cd98f00b204e9800998ecf8427e
```

## Setup

Containerized with Docker. Just add API keys to the config and run `docker-compose up`.

But... not yet. It's still under construction.

I'm planning on this being the foundation for a larger threat intelligence platform.
