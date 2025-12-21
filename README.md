# SparkRepo

SparkRepo is a full-stack web application designed to help manage student submissions for classes that use Scratch or Canva. It provides a simple interface for instructors to view student projects, track submissions, and manage classes.

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

### 2. Configure the Backend

Navigate to the server directory and set up the environment variables.

1.  **Go to the `server` directory:**
    ```sh
    cd server
    ```

2.  **Create a `.env` file:**
    Copy the example environment file:
    ```sh
    cp .env.example .env
    ```

3.  **Generate a JWT Secret Key:**
    Run the following command to generate a secure secret key:
    ```sh
    python -c "import secrets; print(secrets.token_hex(32))"
    ```

4.  **Update the `.env` file:**
    Open the `.env` file and paste the generated key as the value for `JWT_SECRET_KEY`.

    ```
    JWT_SECRET_KEY=your_generated_secret_key_here
    ```

### 3. Run the Application

You need to run both the backend and frontend servers simultaneously in two separate terminals.

**Terminal 1: Run the Backend (Flask)**

1.  Make sure you are in the `server` directory:
    ```powershell
    cd server
    ```
2.  Ensure dependencies are installed (first run only):
    ```powershell
    python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt
    ```
3.  Start the backend using Flask CLI:
    ```powershell
    flask run
    ```
    The backend API will be running at `http://localhost:5000`.

**Terminal 2: Run the Frontend (Vue)**

1.  Open a new terminal and navigate to the `client` directory:
    ```sh
    cd client
    ```
2.  Install dependencies and start Vite dev server:
    ```powershell
    npm install
    npm run dev
    ```

    The frontend application will be available at `http://localhost:5173`.

### Notes

- Backend uses Flask CLI. Ensure `FLASK_APP=app:create_app` is set (already in `server/.env`).
- Frontend uses Vite. Use `npm run dev` in `client`.



### Backend Deployment

1. Set up a virtual environment on your VM:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

2. Configure a production WSGI server (Gunicorn recommended):
   ```
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 'app:create_app()'
   ```

3. Set up a reverse proxy with Nginx or Apache to forward requests to the Flask application.

### Frontend Deployment

1. Build the Vue.js application:
   ```
   cd client
   npm run build
   ```

2. Copy the contents of the `dist` directory to your web server's static files directory.

3. Configure your web server to serve the static files and proxy API requests to the Flask backend.

## API Documentation

### Available Endpoints

- `GET /api/categories` - List all available categories
- `GET /api/categories/{id}` - Get details for a specific category
- `GET /api/categories/{id}/weeks` - List all weeks for a category
- `GET /api/categories/{id}/weeks/{week}` - Get a specific week's assignment
- `POST /api/categories/{id}/weeks/{week}/submissions` - Submit or update a project link for a week
- `GET /api/students` - List all students
- `GET /api/students/{id}/submissions` - Get all submissions for a student

Admin-only endpoints are available under `/api/admin` (weeks and submissions management). See the comments in `server/api.py` and `server/admin.py` for detailed request/response examples for each endpoint.

## Database Schema

The application uses SQLite with the following tables:

- **categories**: Stores information about each category (e.g., Scratch, Canva)
  - id (PK)
  - name
  - description
  - created_at

- **weeks**: Stores weekly assignments for each category
  - id (PK)
  - category_id (FK to categories.id)
  - week_number
  - title
  - description
  - assignment_url
  - due_date
  - created_at

- **students**: Stores student information
  - id (PK)
  - name
  - email
  - class_id (FK to classes.id)
  - created_at

- **submissions**: Stores project link submissions
  - id (PK)
  - student_id (FK to students.id)
  - week_id (FK to weeks.id)
  - project_url
  - comment
  - submitted_at

## License

This project is licensed under the MIT License.
