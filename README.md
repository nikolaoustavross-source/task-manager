# TaskManager

A full stack task management web application built with Flask, MySQL, Docker, and Nginx.

## Stack
- **Backend:** Python / Flask + SQLAlchemy + Flask-Login
- **Database:** MySQL 8.0
- **Frontend:** HTML / CSS / JavaScript (Jinja2 templates)
- **Proxy:** Nginx
- **Containerisation:** Docker + Docker Compose
- **External API:** OpenWeatherMap

## Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- A free [OpenWeatherMap API key](https://openweathermap.org/api)

## Demo Account

A demo account with example tasks is available on the live deployment:

- **URL:** http://134.209.82.95
- **Username:** stavros123
- **Password:** 12345678

Or register your own account to start fresh.

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/task-manager.git
cd task-manager

# 2. Create your .env from the example
cp .env.example .env
# Edit .env and fill in your values (SECRET_KEY, passwords, API key)

# 3. Build and start all containers
docker compose up --build -d

# 4. Open in browser
open http://localhost
```

## Stopping

```bash
docker compose down          # stop containers, keep data
docker compose down -v       # stop containers AND delete database volume
```

## Project Structure

```
task-manager/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # SQLAlchemy models (User, Task)
│   ├── weather.py           # OpenWeatherMap API helper
│   ├── routes/
│   │   ├── auth.py          # Register / login / logout / profile
│   │   ├── tasks.py         # CRUD task routes
│   │   └── api.py           # JSON REST API endpoints
│   ├── templates/           # Jinja2 HTML templates
│   └── static/              # CSS and JS
├── nginx/
│   └── nginx.conf           # Nginx reverse proxy config
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── run.py
└── .env.example
```

## API Endpoints

All endpoints require an active login session.

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/api/tasks` | List all your tasks |
| POST | `/api/tasks` | Create a task (JSON body) |
| GET | `/api/tasks/<id>` | Get one task |
| PATCH | `/api/tasks/<id>` | Update a task |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/stats` | Get task counts |

## Deployment (DigitalOcean)

See the full report for step-by-step deployment instructions. In short:

```bash
# On your Droplet (Ubuntu 22.04)
sudo apt update && sudo apt install -y docker.io docker-compose-plugin
git clone https://github.com/YOUR_USERNAME/task-manager.git
cd task-manager
cp .env.example .env   # edit with production values
docker compose up --build -d
```
