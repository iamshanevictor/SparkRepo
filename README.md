# SparkRepo

A full-stack web application for managing student submissions in Scratch and Canva design classes. Features student project submission forms and admin dashboard for instructors.

## Tech Stack

- **Frontend**: Vue.js 3 + Vite
- **Backend**: Flask (Python) + Firebase Firestore
- **Authentication**: JWT tokens
- **Database**: Google Cloud Firestore

## Project Structure

```
SparkRepo/
├── client/          # Vue.js frontend
│   ├── src/         # Source code
│   ├── public/      # Static assets
│   └── package.json # Dependencies
├── server/          # Flask backend
│   ├── *.py         # Python modules
│   ├── scripts/     # Database seeding
│   ├── .env         # Environment variables
│   └── requirements.txt # Dependencies
└── README.md        # This file
```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Firebase project with Firestore enabled

### 1. Clone Repository

```bash
git clone <repository-url>
cd SparkRepo
```

### 2. Backend Setup

```bash
cd server

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Firebase credentials

# Run backend
flask --app app:create_app run
```

### 3. Frontend Setup

```bash
cd client

# Install dependencies
npm install

# Run frontend
npm run dev
```

### 4. Seed Database (Optional)

```bash
cd server
python -m scripts.seed_firestore
```

## Usage

### Student Interface
- Visit `http://localhost:5173`
- Browse categories and weeks
- Submit projects via upload forms

### Admin Interface
- Login at `http://localhost:5173/admin/login`
- Default credentials: `admin` / `admin123`
- View and manage all submissions
- Update week assignments

## Environment Variables

### server/.env
```env
FLASK_APP=app:create_app
FLASK_ENV=development
JWT_SECRET_KEY=your-secret-key
FIREBASE_SERVICE_ACCOUNT_PATH=serviceAccountKey.json
ADMIN_PASSWORD=admin123
CORS_ORIGINS=http://localhost:5173
```

## Firebase Setup

1. Create a Firebase project
2. Enable Firestore database
3. Create a service account and download credentials as `server/serviceAccountKey.json`
4. Update `FIREBASE_SERVICE_ACCOUNT_PATH` in `.env`

## API Endpoints

- `GET /api/categories` - List categories
- `GET /api/categories/{id}/weeks` - List weeks for category
- `POST /api/categories/{id}/weeks/{num}/submissions` - Submit project
- `POST /api/auth/login` - Admin login
- `GET /api/admin/weeks` - Admin: List all weeks
- `GET /api/admin/submissions` - Admin: List all submissions

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request
