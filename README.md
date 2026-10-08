# AWS Route 53 Clone — Scaler SDE Full-Stack Assignment

A functional, locally runnable clone of the AWS Route 53 management experience. The project focuses on the requested Route 53 workflows rather than real DNS operations: mocked authentication, persistent Hosted Zones, DNS record CRUD, search/filtering, pagination, modals, notifications, and AWS-style navigation.

## Stack
- **Frontend:** Next.js 15 + React 19 + TypeScript
- **Backend:** FastAPI + SQLAlchemy
- **Database:** SQLite
- **UI:** Custom CSS + Lucide icons

## Project structure
```text
frontend/                    Next.js application
backend/                     FastAPI application
  app/
    main.py                  App startup, middleware and router registration
    database.py              SQLite engine and database session
    models.py                SQLAlchemy database models
    schemas.py               API request/response schemas
    routers/
      auth.py                Login, logout and current-user APIs
      hosted_zones.py        Hosted Zone CRUD APIs
      records.py             DNS Record CRUD APIs
    services/
      auth.py                Session/authentication logic
      hosted_zones.py        Hosted Zone business logic
      records.py             DNS Record business logic
      seed.py                First-run demo data
    utils/
      validation.py          Domain and record validation/normalization
```

## Quick start

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows CMD: .venv\Scripts\activate.bat
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Backend API documentation is available at **http://localhost:8000/docs**.

### 2. Frontend
Open a second terminal:
```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**.

### Demo login
- Username: `demo`
- Password: any non-empty value

The assignment specifies mocked authentication, so there is deliberately no real password-management system.

## Implemented
- Mock login/logout/session persistence using an HttpOnly cookie and server-side SQLite session
- Hosted Zone list, search, create, edit, delete
- DNS record list, search, type filter, create, edit, delete
- A, AAAA, CNAME, TXT, MX, NS, PTR, SRV, CAA record types
- Persistent SQLite data
- AWS-console-style top bar, service navigation, tables, forms, alerts, badges, modals and toast notifications
- Pagination for Hosted Zones and DNS records
- Responsive layout
- Seed data for a realistic first-run demo
- API validation and useful error responses
- FastAPI Swagger documentation at `/docs`
- Placeholder-ready navigation for mocked AWS sections

## Architecture
```text
Browser
   ↓
Next.js / React / TypeScript
   ↓ REST API
FastAPI routers
   ↓
Service layer
   ↓
SQLAlchemy models
   ↓
SQLite
```

The frontend does not access SQLite directly. Authentication and all mutations go through the backend API. The backend is intentionally split into routers, services, schemas, models, and database setup so each module has a focused responsibility without introducing unnecessary enterprise-level abstraction.

## API overview
- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/hosted-zones?search=`
- `POST /api/hosted-zones`
- `PUT /api/hosted-zones/{id}`
- `DELETE /api/hosted-zones/{id}`
- `GET /api/hosted-zones/{id}/records?search=&record_type=&page=&page_size=` (paginated response)
- `POST /api/hosted-zones/{id}/records`
- `PUT /api/hosted-zones/{id}/records/{record_id}`
- `DELETE /api/hosted-zones/{id}/records/{record_id}`

## Database schema
`users` → mocked application users.

`hosted_zones` → domain name, generated Route 53-style zone ID, public/private type, comment, and record count.

`dns_records` → record name, type, TTL, value, routing policy and foreign key to hosted zone. Deleting a hosted zone removes its associated records.

`sessions` → HttpOnly-cookie session token, user reference and expiration.

## Validation and behavior
- Domain names are normalized to lowercase and trailing dots are removed.
- Duplicate Hosted Zones are rejected case-insensitively.
- Hosted Zone type is restricted to Public or Private.
- DNS record types are restricted to the assignment's supported types.
- Blank record names and values are rejected.
- TTL is restricted to a sensible range.
- DNS record results are paginated with a bounded page size.
- Session expiration is checked server-side.

## Testing performed
The backend was regression-tested after the refactor for:
- authentication and session persistence
- Hosted Zone create/search/delete
- case-insensitive duplicate detection
- DNS Record create/update/delete
- whitespace-only record-value validation
- record search and pagination
- hosted-zone cascade deletion
- logout/session invalidation
- SQLite persistence and seeded data

## Design notes
The assignment asks for a Route 53 experience and specifically says the goal is to feel like Route 53 rather than a generic CRUD application. The implementation therefore uses an AWS-console-inspired dark global navigation bar, left service navigation, AWS-like table controls, compact typography, primary action hierarchy, inline search/filter controls, information banners and modal forms.

No actual DNS queries, AWS credentials, IAM calls, or Route 53 API calls are made.

## Production improvements
For a production system, replace mocked authentication with AWS Cognito/OIDC, use PostgreSQL, add Alembic migrations, add RBAC, CSRF protection, structured logging, automated tests, rate limiting, and deploy the frontend/API separately behind HTTPS.
