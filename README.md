# 🐳 Nginx + Gunicorn + Docker Configuration for Django

[![Docker](https://img.shields.io/badge/Docker-29-2496ED?logo=docker)](https://www.docker.com/)
[![Nginx](https://img.shields.io/badge/Nginx-1.27-009639?logo=nginx)](https://nginx.org/)
[![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2-499848?logo=gunicorn)](https://gunicorn.org/)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A production-ready **Nginx + Gunicorn + Docker** configuration for Django applications with PostgreSQL, Redis, and Celery support.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration Files](#configuration-files)
- [Docker Services](#docker-services)
- [Running the Application](#running-the-application)
- [Nginx Configuration](#nginx-configuration)
- [Gunicorn Configuration](#gunicorn-configuration)
- [Docker Configuration](#docker-configuration)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This repository contains a complete **production-ready Docker setup** for Django applications using:

- **Nginx** – Reverse proxy, load balancer, and static file server
- **Gunicorn** – Production-grade WSGI server for Django
- **Docker** – Containerized environment for consistent deployment
- **PostgreSQL** – Production database
- **Redis** – Cache and Celery broker
- **Celery** – Asynchronous task processing

---



---

## 📦 Technology Stack

| Category | Technology | Version |
|----------|-----------|---------|
| **Container** | Docker, Docker Compose | 29.0, 3.8 |
| **Web Server** | Nginx | 1.27 (Alpine) |
| **WSGI Server** | Gunicorn | 21.2 |
| **Backend** | Python, Django | 3.13, 4.2 |
| **Database** | PostgreSQL | 15 (Alpine) |
| **Cache & Queue** | Redis, Celery | 7, 5.3 |
| **Monitoring** | Flower | 2.0 |

---

## 📋 Prerequisites

- [Docker](https://www.docker.com/) (29.0+)
- [Docker Compose](https://docs.docker.com/compose/) (3.8+)
- [Git](https://git-scm.com/)

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/nginx-gunicorn-django.git
cd nginx-gunicorn-django

Build and Run

# Build and start all containers
docker compose up -d --build

# Run migrations
docker compose exec web python manage.py migrate

# Create superuser
docker compose exec web python manage.py createsuperuser

# Collect static files
docker compose exec web python manage.py collectstatic --noinput

📄 Configuration Files
Nginx Configuration (docker/nginx/nginx.conf)

upstream django_app {
    server web:8000;
}

server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://django_app;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}


┌─────────────────────────────────────────────────────────────────────────┐
│                    Docker Network (inventory_network)                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────────┐│
│  │   nginx     │    │   web      │    │   celery_worker             ││
│  │   Port 80   │◄──►│  Port 8000 │    │   (Background Tasks)        ││
│  └─────────────┘    └─────────────┘    └─────────────────────────────┘│
│          │                  │                         │                │
│          │                  ▼                         │                │
│          │         ┌─────────────┐                    │                │
│          └────────►│   flower    │                    │                │
│                    │  Port 5555  │                    │                │
│                    └─────────────┘                    │                │
│                           │                           │                │
│          ┌────────────────┼───────────────────────────┘                │
│          │                │                                           │
│          ▼                ▼                                           │
│  ┌─────────────┐  ┌─────────────┐                                    │
│  │     db      │  │   redis     │                                    │
│  │  Port 5432  │  │  Port 6379  │                                    │
│  └─────────────┘  └─────────────┘                                    │
│                                                                       │
└─────────────────────────────────────────────────────────────────────────┘
