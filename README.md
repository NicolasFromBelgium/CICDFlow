# CICDFlow – Complete TDD + DevOps CI/CD Project

**Objective:**  
Build a basic web application (homepage + secure login system) following **Test Driven Development (TDD)** principles and implementing a **complete DevOps CI/CD pipeline** using GitHub Actions.

## Tech Stack
- **Backend**: FastAPI (Python 3.12)
- **Authentication**: fastapi-users + JWT + bcrypt
- **Database**: PostgreSQL
- **Testing**: pytest + httpx (pure TDD approach)
- **Containerization**: Docker + docker-compose
- **CI/CD**: GitHub Actions (lint → tests → build → push → deploy)
- **Environments**: dev (local) → test → UA (Raspberry Pi + Cloudflare Tunnel)

## How to Use This Repository
1. `git clone https://github.com/NicolasFromBelgium/CICDFlow.git`
2. `cp .env.example .env` and fill in your environment variables
3. `docker compose up --build`
4. Open http://localhost:8000/docs

**Follow this repository step by step** → use all available resources (documentation, workflows, tests) → **complete your first full CI/CD pipeline**.

## Conditions
Have a functional server or cloud access

## Next Steps in This Repository
- Step 1: Project structure + first TDD test (login)
- Step 2: GitHub Actions pipeline
- Step 3: Automatic deployment to Raspberry Pi

We will build it together — cleanly and professionally.

Last update: 27/02/2026
