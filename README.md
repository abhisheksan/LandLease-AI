# LandLease AI

LandLease AI is a proof-of-concept geospatial lease intelligence platform for upstream oil and gas. Users can upload oil & gas lease PDFs, extract and review structured lease terms, map lease locations, overlay public well data, and view operational risk analytics.

## Phase 1 Overview

- **Frontend:** React (Vite)  
- **Backend:** FastAPI (Python 3.10+)  
- **Database:** PostgreSQL 15 + PostGIS  
- **Dev environment:** Docker Compose  
- **Core features:**  
  - JWT user auth (email/pass)
  - Upload lease PDF, extract text & fields (AI/rule-based)
  - Review/edit lease fields
  - Lease geolocation (point)
  - Map with leases, nearby PA wells, dashboard/risk
  - Local only, no cloud dependencies

## Directory structure

```
LandLease AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   ├── workers/
│   │   ├── db/
│   │   └── main.py
│   ├── scripts/
│   │   └── import_wells.py
│   ├── tests/
│   └── data/
│       └── sample_wells/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   ├── components/
│   │   ├── api/
│   │   ├── hooks/
│   │   ├── types/
│   │   ├── map/
│   │   └── dashboard/
├── sample_leases/
├── docker-compose.yml
└── README.md
```

## Phase 1 Build Steps

- Backend skeleton (FastAPI)
- Database schema migration (PostgreSQL/PostGIS)
- Auth (JWT, bcrypt; backend + frontend pages)
- Frontend skeleton (React app with page structure)
- PDF upload, storage, status
- Text extraction (normal, OCR fallback)
- Lease field extraction
- Lease review page (editable)
- Lease list page
- Well data import (script)
- PostGIS setup
- Map page
- Nearby wells query
- Dashboard/risk metrics
- Testing
- Docker Compose setup

## Attribution

All code and work are the original creation of the LandLease AI author.

## License

TBD

---
See this document and project for more detailed implementation guidance.