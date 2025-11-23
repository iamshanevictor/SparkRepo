-- Initial database schema for SparkRepo
-- Run this in your Supabase SQL Editor to create all necessary tables

-- Enable UUID extension (if needed)
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Categories table
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    email VARCHAR(100) UNIQUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Weeks table
CREATE TABLE IF NOT EXISTS weeks (
    id SERIAL PRIMARY KEY,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
    week_number INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    display_name VARCHAR(100),
    description TEXT,
    assignment_url VARCHAR(255),
    due_date TIMESTAMP WITH TIME ZONE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(category_id, week_number)
);

-- Submissions table
CREATE TABLE IF NOT EXISTS submissions (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(100) NOT NULL,
    week_id INTEGER NOT NULL REFERENCES weeks(id) ON DELETE CASCADE,
    project_type VARCHAR(50) NOT NULL DEFAULT 'scratch',
    project_url VARCHAR(255) NOT NULL,
    comment TEXT,
    admin_comment TEXT,
    status VARCHAR(20) DEFAULT 'submitted',
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_modified TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    modified_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_weeks_category_id ON weeks(category_id);
CREATE INDEX IF NOT EXISTS idx_weeks_category_week ON weeks(category_id, week_number);
CREATE INDEX IF NOT EXISTS idx_submissions_week_id ON submissions(week_id);
CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create a function to automatically update last_modified timestamp
CREATE OR REPLACE FUNCTION update_last_modified()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_modified = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers to automatically update last_modified
CREATE TRIGGER update_weeks_last_modified
    BEFORE UPDATE ON weeks
    FOR EACH ROW
    EXECUTE FUNCTION update_last_modified();

CREATE TRIGGER update_submissions_last_modified
    BEFORE UPDATE ON submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_last_modified();

-- Enable Row Level Security (RLS) - Optional, but recommended for Supabase
-- You may want to configure RLS policies based on your security requirements
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE weeks ENABLE ROW LEVEL SECURITY;
ALTER TABLE submissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Basic RLS policies (adjust based on your needs)
-- Allow all operations for service role (used by your backend)
-- These policies allow the service role key to access everything
-- For production, you may want more restrictive policies

-- Categories: Public read, admin write
CREATE POLICY "Categories are viewable by everyone" ON categories
    FOR SELECT USING (true);

CREATE POLICY "Categories are insertable by service role" ON categories
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Categories are updatable by service role" ON categories
    FOR UPDATE USING (true);

CREATE POLICY "Categories are deletable by service role" ON categories
    FOR DELETE USING (true);

-- Weeks: Public read, admin write
CREATE POLICY "Weeks are viewable by everyone" ON weeks
    FOR SELECT USING (true);

CREATE POLICY "Weeks are insertable by service role" ON weeks
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Weeks are updatable by service role" ON weeks
    FOR UPDATE USING (true);

CREATE POLICY "Weeks are deletable by service role" ON weeks
    FOR DELETE USING (true);

-- Submissions: Public insert, admin read/write
CREATE POLICY "Submissions are viewable by service role" ON submissions
    FOR SELECT USING (true);

CREATE POLICY "Submissions are insertable by everyone" ON submissions
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Submissions are updatable by service role" ON submissions
    FOR UPDATE USING (true);

CREATE POLICY "Submissions are deletable by service role" ON submissions
    FOR DELETE USING (true);

-- Users: Only service role can access
CREATE POLICY "Users are viewable by service role" ON users
    FOR SELECT USING (true);

CREATE POLICY "Users are insertable by service role" ON users
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Users are updatable by service role" ON users
    FOR UPDATE USING (true);

CREATE POLICY "Users are deletable by service role" ON users
    FOR DELETE USING (true);

