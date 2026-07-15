# Moose OS Backend

A **production-ready FastAPI backend** powering the [Moose OS](https://github.com/Alejandro-Bernal/moose-os-frontend) CLI-inspired portfolio application. This server demonstrates modern Python web development practices with async support, database migrations, email integration, and comprehensive API design.

---

## Project Overview

Moose OS is a unique, terminal-inspired portfolio platform where visitors can interact with a command-line interface to explore projects and submit inquiries. The backend API manages contact submissions, follow-up requests, and delivers professional email notifications through Resend.

**Why this project is interesting:**

- Built with **FastAPI** for high performance and async-first development
- Production-ready architecture with **PostgreSQL** and **Alembic** migrations
- RESTful API design with proper request validation and error handling
- Rate limiting and security best practices
- Comprehensive logging for production monitoring

---

## 🛠 Tech Stack

| Category             | Technology                        |
| -------------------- | --------------------------------- |
| **Framework**        | FastAPI 0.100+                    |
| **Runtime**          | Python 3.13                       |
| **Database**         | PostgreSQL 16                     |
| **ORM**              | SQLAlchemy 2.0 (async)            |
| **Migrations**       | Alembic                           |
| **Email**            | Resend API                        |
| **Rate Limiting**    | Slowapi                           |
| **Containerization** | Docker & Docker Compose           |
| **Async**            | AsyncPG (async PostgreSQL driver) |

---

## ✨ Key Features

✅ **FastAPI Best Practices**

- Async/await for non-blocking I/O
- Pydantic models for request/response validation
- Automatic OpenAPI documentation (Swagger UI)
- Type hints throughout

✅ **Database Architecture**

- Async SQLAlchemy for high-concurrency applications
- Alembic version control for schema migrations
- Proper foreign key relationships
- Model-driven development with migration safety

✅ **Production Ready**

- Rate limiting to prevent abuse
- Structured logging for monitoring
- Environment-based configuration
- Comprehensive error handling

✅ **Email Integration**

- Professional email delivery via Resend
- Contact routing and follow-up management
- Template-ready for customization

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.13+ (for local development)

### Setup & Run

**1. Clone and configure:**

```bash
git clone https://github.com/Alejandro-Bernal/moose-os-backend.git
cd moose-os-backend
cp .env.example .env  # Configure your environment
```

**2. Start with Docker:**

```bash
docker-compose up -d
```

The API will be available at `http://localhost:8000`

**3. View API Documentation:**

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📊 API Endpoints

### Contact Submissions

- `POST /api/inquiries/submit` - Submit a new contact inquiry
- `GET /api/inquiries/{id}` - Retrieve inquiry details
- `GET /api/inquiries` - List all inquiries

### Follow-up Requests

- `POST /api/inquiries/{id}/followup` - Submit follow-up to original inquiry
- `GET /api/inquiries/{id}/followups` - List follow-ups for an inquiry

Full API documentation available at `/docs` when server is running.

---

## 🏗 Project Structure

```
moose-os-backend/
├── app/
│   ├── main.py              # FastAPI app initialization
│   ├── config.py            # Configuration management
│   ├── database.py          # SQLAlchemy setup & session management
│   ├── security.py          # API key validation
│   ├── limiter.py           # Rate limiting configuration
│   ├── models/              # SQLAlchemy ORM models
│   │   ├── contact_submission.py
│   │   └── follow_up_request.py
│   ├── api/
│   │   └── routes/
│   │       └── inquiries.py  # API endpoints
│   └── services/
│       └── email.py         # Email delivery service
├── alembic/                 # Database migrations
│   ├── versions/            # Migration files
│   └── env.py              # Migration configuration
├── docker-compose.yml       # Container orchestration
├── Dockerfile              # Application container
└── requirements.txt        # Python dependencies
```

---

## 🔧 Development

### Local Development Setup

**1. Create virtual environment:**

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```

**2. Install dependencies:**

```bash
pip install -r requirements.txt
```

**3. Run database migrations:**

```bash
docker-compose exec api alembic upgrade head
```

**4. Start the development server:**

```bash
docker-compose up -d
```

### Database Migrations

**View current migration status:**

```bash
docker-compose exec api alembic current
```

**Create a new migration:**

```bash
docker-compose exec api alembic revision --autogenerate -m "description"
```

**Apply all pending migrations:**

```bash
docker-compose exec api alembic upgrade head
```

---

## 🔐 Environment Variables

```env
# Database
DATABASE_URL=postgresql+asyncpg://user:password@db:5432/moose_os
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_secure_password
POSTGRES_DB=moose_os

# API Security
API_KEY=your_secure_api_key

# Email Service
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=noreply@yourdomain.com
CONTACT_ROUTING_EMAIL=contact@yourdomain.com
```

---

## 📈 Performance & Scalability

- **Async-First**: All I/O operations are non-blocking for optimal throughput
- **Connection Pooling**: SQLAlchemy manages database connections efficiently
- **Rate Limiting**: Configurable rate limits prevent abuse and DDoS attacks
- **Containerized**: Docker deployment ensures consistency across environments
- **Horizontal Scaling**: Stateless design allows easy scaling with load balancers

---

## 🧪 Testing

_(Add tests as you expand the project)_

```bash
# Run tests
docker-compose exec api pytest

# With coverage
docker-compose exec api pytest --cov=app
```

---

## 📋 Production Deployment

For production deployment:

1. **Use environment secrets** instead of `.env` files
2. **Enable HTTPS/TLS** with a reverse proxy (Nginx/Caddy)
3. **Configure CORS** appropriately for your frontend domain
4. **Monitor with logging** and APM tools
5. **Scale horizontally** with container orchestration (Kubernetes)
6. **Run database backups** regularly

See `DEPLOYMENT.md` for detailed production setup (coming soon).

---

## 🐛 Troubleshooting

**Database connection issues:**

```bash
# Check if containers are running
docker-compose ps

# View logs
docker-compose logs db
docker-compose logs api
```

**Migrations failing:**

```bash
# Check migration status
docker-compose exec api alembic current

# View migration history
docker-compose exec api alembic history
```

---

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)
- [Pydantic Data Validation](https://docs.pydantic.dev/)

---

## 📄 License

This project is part of my portfolio. Feel free to explore, learn, and use as a reference.

---

## 🤝 Let's Connect

I'm passionate about backend development and building scalable systems. If you'd like to discuss this project or opportunities:

- 💼 [LinkedIn](https://www.linkedin.com/in/alejandro-bernal-cruz)
- 🐙 [GitHub](https://github.com/Alejandro-Bernal)
- 📧 contact@bernalforge.dev

---

**Built with ❤️ by Alejandro Bernal**
