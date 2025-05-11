# Backend Service

This directory contains the backend service for the MRA project. It is built using Python and managed with Poetry for dependency management. The backend provides APIs and services to support the frontend and other components of the application.

## Directory Structure

- **src/**: Contains the main source code for the backend.
  - `main.py`: Entry point for the backend server.
  - `training_creator.py`, `training_manager.py`, `user_manager.py`: Core modules for managing training and user-related functionalities.
  - **chat/**: Contains modules for chat-related functionalities, including OpenAI integration and prompt management.
- **tests/**: Contains unit tests for the backend modules.
- **prisma/**: Contains Prisma schema and migration files for database management.
  - `schema.prisma`: Defines the database schema.
  - `migrations/`: Stores migration files.
- **Taskfile.yml**: Taskfile for managing backend tasks like cleaning, testing, and running the server.
- **poetry.lock** and **pyproject.toml**: Poetry files for dependency management.

## Setup Instructions

1. **Install Dependencies**:
   Run the following command to install all dependencies:
   ```bash
   poetry install
   ```

2. **Database Setup**:
   - Ensure Docker is installed and running.
   - Start the database using Docker Compose:
     ```bash
     docker-compose -f ../compose/docker-compose.yml up -d
     ```
   - Apply Prisma migrations:
     ```bash
     poetry run prisma migrate deploy
     ```

3. **Run the Server**:
   Start the backend server with:
   ```bash
   poetry run python src/main.py
   ```

## Testing

Run the unit tests using:
```bash
poetry run pytest
```

## Linting and Formatting

- Run linters to check code quality:
  ```bash
  poetry run flake8
  poetry run black --check .
  ```
- Format the codebase:
  ```bash
  poetry run black src tests
  ```

## Additional Notes

- Ensure the `.env` file is properly configured with the required environment variables.
- Refer to the `Taskfile.yml` for additional tasks and commands.