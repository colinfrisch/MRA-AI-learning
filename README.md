# MRA (My React App)

This project consists of a React frontend and a Flask backend with a MySQL database.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Docker](https://docs.docker.com/get-docker/) >= 27.0
  - Required for running the database locally
- [Poetry](https://python-poetry.org/docs/#installation)
  - For Python package management
- [Task](https://taskfile.dev/installation/)
  - For running project commands
- [Node.js and npm](https://nodejs.org/) (LTS version recommended)
  - For running the frontend

## Project Structure

- `src/frontend/`: React frontend application
- `src/server/`: Flask backend server
- `prisma/`: Database schema and migrations
- `compose/`: Docker compose files for local development

## First-Time Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MRA
   ```

2. Initialize the project (this will set up both frontend and backend):
   ```bash
   task init
   ```
   This command will:
   - Create necessary environment files
   - Install Python dependencies
   - Set up the database
   - Install frontend dependencies

3. Create a `.env` file (if not created automatically) with:
   ```
   DATABASE_URL="mysql://local_user:local_password@127.0.0.1:3306/mra_db"
   ```

## Running the Application

1. Start both frontend and backend:
   ```bash
   task run
   ```

   This will start:
   - MySQL database in Docker
   - Flask backend server on port 8080
   - React frontend on port 3000

2. Or run components separately:
   ```bash
   # Run just the database
   task run-database
   
   # Run just the backend
   task run-backend
   
   # Run just the frontend
   task run-frontend
   ```

## Development Commands

- Clean the environment:
  ```bash
  task clean
  ```

- Run tests:
  ```bash
  task test
  ```

- Database commands:
  ```bash
  task prisma-generate     # Generate Prisma client
  task prisma-deploy      # Deploy migrations
  task mysql-prompt      # Open MySQL prompt
  ```

## Troubleshooting

1. If the database connection fails:
   - Ensure Docker is running
   - Check if the database container is up with `docker ps`
   - Try restarting the database: `task stop-database && task run-database`

2. If frontend dependencies are missing:
   - Run `task setup-frontend`

3. If backend dependencies are missing:
   - Run `poetry install`

## Contributing

Please ensure you have installed the recommended VSCode extensions:
- Pylance
- Prisma
- ESLint
- Prettier
