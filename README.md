# Link Of API Deployed On Render

https://fastapi-api-3yil.onrender.com

# FastAPI Social Media API

A modern, production-ready REST API built with **FastAPI** for a social media platform. Features secure user authentication, post management, voting system, rate limiting, and comprehensive test coverage.

## Features

- **User Authentication** - JWT-based OAuth2 authentication with password hashing
- **Post Management** - Create, read, update, and delete posts with search functionality
- **User Management** - User registration, profile management, and account deletion
- **Voting System** - Like/vote on posts with vote aggregation
- **Rate Limiting** - Token bucket rate limiter to prevent abuse
- **Database** - PostgreSQL with SQLModel ORM and Alembic migrations
- **Testing** - Comprehensive pytest test suite with fixtures
- **Docker** - Production and development Docker configurations
- **CORS** - Cross-Origin Resource Sharing enabled for frontend integration
- **API Documentation** - Auto-generated Swagger/OpenAPI documentation
- **Production Ready** - Deployed on Render with production configurations

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) - Modern async web framework
- **Database ORM**: [SQLModel](https://sqlmodel.tiangolo.com/) - SQL databases with Python objects
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens) with [python-jose](https://github.com/mpdavis/python-jose)
- **Password Hashing**: [Bcrypt](https://github.com/pyca/bcrypt)
- **Migrations**: [Alembic](https://alembic.sqlalchemy.org/)
- **Testing**: [Pytest](https://pytest.org/)
- **Async Driver**: [AsyncPG](https://magicstack.github.io/asyncpg/)
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Docker & Docker Compose (optional, for containerized deployment)
- pip or pipenv for dependency management

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ramchandrasinh/fastapi-project
cd fastapi
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Setup Environment Variables

Create a `.env` file in the root directory:

```bash
# Database Configuration
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/fastapi_db
DATABASE_USERNAME=your_db_user
DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD=your_db_password
DATABASE_NAME=fastapi_db

# Authentication
SECRET_KEY=your-secret-key-here-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_CAPACITY=60
RATE_LIMIT_REFILL_RATE=1.0
```

### 5. Database Setup

```bash
# Create PostgreSQL database
createdb fastapi_db

# Run migrations
alembic upgrade head
```

### 6. Run Development Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📚 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login and get JWT token |

### Posts
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/posts` | Get all posts (with pagination & search) |
| POST | `/posts` | Create a new post |
| GET | `/posts/{id}` | Get a specific post |
| PUT | `/posts/{id}` | Update a post |
| DELETE | `/posts/{id}` | Delete a post |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/users` | Create new user account |
| GET | `/users/{id}` | Get user profile |
| PUT | `/users/{id}` | Update user profile |
| DELETE | `/users/{id}` | Delete user account |

### Votes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/votes` | Vote on a post(dir=1) or Remove vote from a post(dir=0) |

## 🔑 Authentication

The API uses JWT (JSON Web Tokens) for authentication:

1. **Register** a new user via `/users`
2. **Login** via `/auth/login` to get access token
3. Include token in request headers: `Authorization: Bearer <token>`

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_posts.py

# Run with verbose output
pytest -v
```

### Test Files
- `test_auth.py` - Authentication endpoints
- `test_posts.py` - Post management endpoints
- `test_users.py` - User management endpoints
- `test_votes.py` - Voting system endpoints
- `test_rate_limiter.py` - Rate limiting functionality

## 🐳 Docker Deployment

### Development with Docker

```bash
docker-compose up -d
```

### Production Deployment

```bash
docker-compose -f docker-compose-prod.yml up -d
```

The containers will:
- Build the FastAPI application
- Setup PostgreSQL database
- Run migrations automatically
- Expose the API on the configured port

## 🗄️ Database Migrations

### Create New Migration

```bash
alembic revision --autogenerate -m "description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migrations

```bash
alembic downgrade -1
```

### View Migration History

```bash
alembic current
alembic history
```

## 📁 Project Structure

```
.
├── alembic/                    # Database migrations
│   ├── versions/              # Migration scripts
│   ├── env.py                 # Migration environment
│   └── script.py.mako         # Migration template
├── app/                        # Application package
│   ├── __init__.py
│   ├── main.py                # FastAPI app initialization
│   ├── config.py              # Configuration and settings
│   ├── database.py            # Database connection
│   ├── model.py               # SQLModel models (Post, User, Vote)
│   ├── schemas.py             # Pydantic schemas
│   ├── oauth2.py              # JWT authentication logic
│   ├── rate_limiter.py        # Rate limiting implementation
│   ├── utils.py               # Utility functions
│   └── routers/               # API route handlers
│       ├── auth.py            # Authentication routes
│       ├── post.py            # Post CRUD routes
│       ├── user.py            # User management routes
│       └── vote.py            # Voting routes
├── tests/                      # Test suite
│   ├── conftest.py            # Pytest configuration and fixtures
│   ├── test_auth.py
│   ├── test_posts.py
│   ├── test_users.py
│   ├── test_votes.py
│   └── test_rate_limiter.py
├── .env                        # Environment variables
├── .env.example                # Example environment file
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image configuration
├── docker-compose.yml          # Development compose config
├── docker-compose-prod.yml     # Production compose config
├── alembic.ini                 # Alembic configuration
├── render.yaml                 # Render deployment config
└── README.md                   # This file
```

## ⚙️ Configuration

Key configuration options in `config.py`:

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `database_url` | str | - | PostgreSQL connection string |
| `secret_key` | str | - | JWT signing key (keep secret!) |
| `algorithm` | str | HS256 | JWT algorithm |
| `access_token_expire_minutes` | int | 100 | Token expiration time |
| `rate_limit_enabled` | bool | true | Enable rate limiting |
| `rate_limit_capacity` | int | 60 | Rate limit capacity (requests) |
| `rate_limit_refill_rate` | float | 1.0 | Token refill rate per second |

## ⚡ Rate Limiting

The API implements a **Token Bucket Rate Limiter** to prevent abuse:

- **Capacity**: 60 requests per minute (configurable)
- **Refill Rate**: 1 request per second
- **Exempt Paths**: `/docs`, `/redoc`, `/openapi.json`

When rate limit is exceeded, the API returns `429 Too Many Requests`.

## 🔄 CORS Configuration

Currently enabled for development. Update `app/main.py` for production:

```python
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
```

## 📝 Database Models

### Post
```python
- id: int (Primary Key)
- title: str
- content: str
- published: bool
- created_at: datetime
- owner_id: int (Foreign Key → User)
```

### User
```python
- id: int (Primary Key)
- email: str (Unique)
- password: str (Hashed)
- created_at: datetime
```

### Vote
```python
- user_id: int (Primary Key, Foreign Key → User)
- post_id: int (Primary Key, Foreign Key → Post)
```

## 🚀 Deployment

### Deploy to Render

The project includes `render.yaml` for easy deployment:

```bash
# Push to GitHub
git push origin main

# Deploy via Render dashboard or CLI
render deploy
```

### Environment Variables for Production

Set these on your hosting platform:
- `DATABASE_URL` - Production database URL
- `SECRET_KEY` - Strong, random secret key
- `ALGORITHM` - JWT algorithm (HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration
- `RATE_LIMIT_ENABLED` - Enable rate limiting
- `RATE_LIMIT_CAPACITY` - Rate limit capacity

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Check PostgreSQL is running
psql postgres -U postgres

# Verify connection string in .env
# Format: postgresql+asyncpg://user:password@host:port/dbname
```

### Migration Errors
```bash
# Reset migrations (development only!)
alembic downgrade base
alembic upgrade head
```

### Tests Failing
```bash
# Ensure test database exists and is fresh
pytest --tb=short -v
```

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👤 Author

Ramchandrasinh Gohil

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Last Updated**: 2026-06-16