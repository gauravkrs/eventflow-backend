# EventFlow Backend

A collaborative event management system with features like role-based access control, versioning, change tracking, and conflict resolution.

## 🚀 Features

- ✅ User registration and login with JWT
- ✅ Role-based access (Owner, Editor, Viewer)
- ✅ Full CRUD for events
- ✅ Support for recurring events
- ✅ Conflict detection
- ✅ Share events with granular permissions
- ✅ Version history and rollback
- ✅ Changelog with diff
- ✅ Batch event creation
- ✅ Token refresh and logout

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM
- **Alembic** – Database migrations
- **PostgreSQL** – Database
- **Pydantic** – Data validation
- **JWT (python-jose)** – Authentication
- **Uvicorn** – ASGI server

## ✅ Alembic Setup Recap

1. **Install Alembic** (already in `requirements`)
2. **Run:** `alembic init alembic`
3. **Update `alembic.ini`:**
```ini
sqlalchemy.url = postgresql://user:password@localhost:5432/eventflow

## 📦 Installation

```bash
git clone https://github.com/your-username/eventflow-backend.git
cd eventflow-backend

# If using Poetry
poetry install

# Or using pip
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python main.py
