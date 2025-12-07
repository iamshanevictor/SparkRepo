"""Database schema initialization for SparkRepo.

This script helps initialize the Supabase database with the required schema.
Run this after setting up Supabase to create all necessary tables.
"""

import os
import sys
from dotenv import load_dotenv
from supabase_client import get_supabase_admin

load_dotenv()

# SQL schema for all tables
SCHEMA_SQL = """
-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    email VARCHAR(100) UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Weeks table
CREATE TABLE IF NOT EXISTS weeks (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    display_name VARCHAR(100),
    description TEXT,
    assignment_url VARCHAR(255),
    due_date TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(category_id, week_number)
);

-- Submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id BIGINT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    student_name VARCHAR(100) NOT NULL,
    week_id BIGINT NOT NULL REFERENCES weeks(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL DEFAULT 'scratch',
    project_url VARCHAR(255) NOT NULL,
    comment TEXT,
    admin_comment TEXT,
    status VARCHAR(20) DEFAULT 'submitted',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_by BIGINT REFERENCES users(id)
);

-- Create indexes for common queries
CREATE INDEX IF NOT EXISTS idx_weeks_category ON weeks(category_id);
CREATE INDEX IF NOT EXISTS idx_submissions_week ON submissions(week_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
"""


def initialize_database():
    """Initialize the database schema."""
    try:
        client = get_supabase_admin()
        
        print("Attempting to initialize database schema...")
        print("Note: Supabase doesn't support direct SQL execution via the Python client.")
        print("\nPlease follow these steps to set up your database:")
        print("\n1. Go to your Supabase project: https://app.supabase.com/")
        print("2. Navigate to the 'SQL Editor' section")
        print("3. Click 'New Query'")
        print("4. Copy and paste the following SQL:")
        print("\n" + "="*60)
        print(SCHEMA_SQL)
        print("="*60)
        print("\n5. Execute the query")
        print("\nAlternatively, you can use the Supabase CLI or REST API.")
        print("For more information: https://supabase.io/docs/guides/database")
        
        # Try to verify connection
        response = client.table('categories').select('*').limit(1).execute()
        if response.data is not None:
            print("\n✓ Database connection successful!")
            return True
        else:
            print("\n✗ Could not verify database connection")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        print("\nPlease ensure:")
        print("- SUPABASE_URL is set")
        print("- SUPABASE_SERVICE_KEY is set")
        print("- Your database is accessible")
        return False


if __name__ == '__main__':
    # Check environment variables
    if not os.getenv('SUPABASE_URL') or not os.getenv('SUPABASE_SERVICE_KEY'):
        print("❌ Missing environment variables!")
        print("Please set SUPABASE_URL and SUPABASE_SERVICE_KEY in your .env file")
        sys.exit(1)
    
    success = initialize_database()
    sys.exit(0 if success else 1)
