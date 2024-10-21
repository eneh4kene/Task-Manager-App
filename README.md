# Task Manager App

This is a full-stack Task Manager application. The backend is built with Python using FastAPI, while the frontend is under development using React. The app aims to manage tasks efficiently with user authentication and task tracking features.

## Project Structure

```plaintext
Task Manager App/
│
├── backend/
│   ├── alembic/                  # Alembic migrations folder
│   ├── app/
│   │   ├── auth.py               # Authentication logic
│   │   ├── database.py           # Database connection setup
│   │   ├── main.py               # Entry point for the FastAPI app
│   │   ├── models.py             # SQLAlchemy models for users and tasks
│   │   ├── schemas.py            # Pydantic schemas
│   │   ├── tasks.py              # Task-related business logic
│   │   ├── users.py              # User-related business logic
│   └── .env                      # Environment variables (not included in Git)
│
├── frontend/                     # React frontend (in development)
│
├── .dockerignore                 # Files to ignore in Docker
├── docker-compose.yml            # Docker Compose configuration
├── Dockerfile                    # Dockerfile for containerizing the backend
├── requirements.txt              # Python dependencies
└── .gitignore                    # Files to exclude from version control
```

## Features

- **FastAPI Backend**: A lightweight and efficient Python web framework.
- **Task Management**: CRUD operations for tasks.
- **User Authentication**: JWT-based authentication for secure login.
- **PostgreSQL Database**: Persistent data storage using PostgreSQL.
- **Alembic Migrations**: Database migrations using Alembic.

## Prerequisites

- [Python 3.9+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Docker](https://www.docker.com/get-started) (optional, for running via Docker)
- Node.js (for the frontend)

## Backend Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/eneh4kene/Task-Manager-App.git
   cd Task-Manager-App/backend
   ```

2. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:

   ```bash
   DATABASE_URL=postgresql://user:password@localhost/taskmanager
   SECRET_KEY=your_secret_key
   ```

5. Apply migrations to the database:

   ```bash
   alembic upgrade head
   ```

6. Start the FastAPI server:

   ```bash
   uvicorn app.main:app --reload
   ```

## Docker Setup (Optional)

1. Ensure Docker is installed and running on your machine.
2. Run the app using Docker Compose:

   ```bash
   docker-compose up --build
   ```

## Frontend Setup

The frontend is currently being developed using React. Once ready, instructions for setting up and running the frontend will be provided.
