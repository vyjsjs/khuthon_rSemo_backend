# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

FastAPI + Supabase backend for "문화 정류장" (Culture Bus Stop) — a 2026 Khuthon hackathon project.

## Commands

```bash
# Install dependencies
pip install fastapi supabase python-dotenv uvicorn

# Run development server
uvicorn app.main:app --reload

# Health check
curl http://localhost:8000/
# DB connection test
curl http://localhost:8000/test-db
```

No `requirements.txt` exists yet — dependencies are `fastapi`, `supabase`, `python-dotenv`, `uvicorn`.

## Environment Variables

A `.env` file is required at the project root with:
```
SUPABASE_URL=<your-supabase-project-url>
SUPABASE_KEY=<your-supabase-anon-or-service-key>
```

The `.env` file is gitignored; never commit credentials.

## Architecture

**Entry point**: [app/main.py](app/main.py) — creates the `FastAPI` app instance and registers routers.

**Database**: [app/database.py](app/database.py) — initializes a singleton `supabase: Client` instance loaded from env vars. Import it everywhere DB access is needed: `from app.database import supabase`.

**Planned layered structure** (directories exist but are empty):
- [app/routers/](app/routers/) — API route modules, each covering a resource domain
- [app/schemas/](app/schemas/) — Pydantic request/response models
- [app/services/](app/services/) — business logic, calls Supabase via the singleton client
- [app/utils/](app/utils/) — shared helper functions

**Pattern**: routers import from services, services import from `app.database`, schemas are used for input validation and response serialization. Keep business logic out of routers.
