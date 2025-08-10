# SparkRepo

SparkRepo is a full-stack web application designed to help manage student submissions for project-based learning, such as Scratch or Canva. It provides a simple interface for instructors to create assignment categories and weeks, and for students to submit their work directly without needing to log in.

The project is built with a Vue.js frontend and a Flask (Python) backend.

## Project Structure

- `/client`: Contains the Vue.js frontend application.
- `/server`: Contains the Flask backend API.

## Prerequisites

Before you begin, ensure you have the following installed:

- [Python](https://www.python.org/downloads/) (3.8 or higher)
- [Node.js](https://nodejs.org/en/download/) (16.x or higher)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package installer)
- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) (Node.js package manager)

## Getting Started

Follow these steps to get your development environment set up and running.

### 1. Clone the Repository

First, clone this repository to your local machine:

```sh
git clone <repository-url>
cd SparkRepo
```

### 2. Configure Environment

- Copy example env files and adjust if needed (examples are safe to commit; real envs are ignored by Git):
  - Backend: copy `server/.env.example` to `server/.env` and set values (JWT secret, CORS origins, DB path if overriding)
  - Frontend: copy `client/.env.example` to `client/.env` and set `VITE_API_URL` (default `http://localhost:5000/api`)

### 3. Seed an Admin User (local)

Run this once to ensure you can log into the admin dashboard:

```powershell
cd server
python -m scripts.seed_admin
```

This will create or update the `admin` user with password `admin`.

### 4. Run the Application

Run the backend and frontend in two terminals.

**Terminal 1: Run the Backend (Flask)**

1.  Navigate to the `server` directory.
2.  Execute the run script:
    ```powershell
    .\run_backend.ps1
    ```
    This script will automatically create a Python virtual environment, install dependencies, and start the server.

    The backend API will be running at `http://localhost:5000`.

**Terminal 2: Run the Frontend (Vue)**

1.  Open a new terminal and navigate to the `client` directory:
    ```sh
    cd client
    ```
2.  Execute the run script:
    ```powershell
    .\run_frontend.ps1
    ```
    This script will install Node.js dependencies and start the Vite development server.

    The frontend application will be available at `http://localhost:5173`.

### What the Run Scripts Do

-   `server/run_backend.ps1`:
    -   Checks for a `.venv` virtual environment and creates one if it doesn't exist.
    -   Activates the virtual environment.
    -   Installs Python packages from `requirements.txt`.
    -   Initializes the SQLite database (`sparkrepo.db`) and seeds it with sample data via `seed.py` on the first run.
    -   Starts the Flask development server.

-   `client/run_frontend.ps1`:
    -   Checks for a `node_modules` directory and runs `npm install` if it doesn't exist.
    -   Starts the Vite development server with Hot-Module-Reloading (HMR) enabled.

## API Documentation (high level)

### Available Endpoints

- `GET /api/categories` - List all available categories.
- `GET /api/categories/{id}/weeks` - List all weeks for a category.
- `GET /api/categories/{id}/weeks/{week_number}` - Get a specific week's assignment.
- `POST /api/categories/{id}/weeks/{week_number}/submissions` - Submit a project link for a specific week.
- `GET /api/admin/weeks` - Get all weeks for the admin dashboard.
- `POST /api/admin/categories/{category_id}/weeks` - Add a new week to a category.
- `PUT /api/admin/weeks/{id}` - Update an existing week.
- `GET /api/admin/submissions` - Admin submissions with optional filters (`class_id`, `week_id`, `status`).

See `server/api.py` and `server/admin.py` for more details.

## Database Schema

The application uses SQLite with the following tables:

- **categories**: Stores course categories.
  - `id` (PK)
  - `name`
  - `description`

- **weeks**: Stores weekly assignments for each category.
  - `id` (PK)
  - `category_id` (FK to categories.id)
  - `week_number`
  - `title`
  - `display_name`
  - `description`
  - `assignment_url`
  - `due_date`
  - `is_active`

- **submissions**: Stores project link submissions from students.
  - `id` (PK)
  - `student_name` (String)
  - `week_id` (FK to weeks.id)
  - `project_type`
  - `project_url`
  - `comment`
  - `status`
  - `submitted_at`

- **users**: Stores admin user information.
  - `id` (PK)
  - `username`
  - `email`
  - `password_hash`
  - `is_admin`

## Security & Git Hygiene

- Do not commit real secrets. Real env files (`server/.env`, `client/.env`) are ignored by `.gitignore`.
- SQLite DBs are also ignored; if one was previously tracked (e.g. `server/sparkrepo.db`), remove it from Git with:
  ```powershell
  git rm --cached server/sparkrepo.db
  ```
- Examples (`*.env.example`) remain tracked and safe to share.

## License

This project is licensed under the MIT License.
