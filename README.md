# Workout Tracking API

This is a clean-architecture-based API for tracking workout progress.

## Technical Stack
- **Framework**: FastAPI
- **Database**: SQLite (SQLAlchemy Async)
- **Dependency Management**: uv
- **Admin Interface**: SQLAdmin

## Setup

1. **Install uv**:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Sync project**:
   ```bash
   uv sync
   ```

3. **Environment Setup**:
   Ensure you have a `.env` file in the root directory:
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./workout.db
   ```

4. **Create Superuser**:
   To access the admin panel, create an administrator account:
   ```bash
   PYTHONPATH=src uv run scripts/create_superuser.py
   ```

## Running the Application

Use the VS Code debugger or run directly:
```bash
PYTHONPATH=src .venv/bin/uvicorn workout_tracking.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.
The Admin panel is located at `http://127.0.0.1:8000/admin`.
