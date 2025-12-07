"""
DEPRECATED: This file is no longer used.

SparkRepo uses Supabase as the primary database service (REST API-based),
not SQLAlchemy ORM models. Database operations are handled via db_service.py
and the Supabase client directly.

To see current data models, check the Supabase schema or refer to db_service.py
for the data structure formatting methods (_format_*).

This file is kept for reference only.
"""

# DATABASE SCHEMA REFERENCE (maintained in Supabase):
#
# Tables:
# - categories: id (PK), name (UNIQUE), description, created_at
# - users: id (PK), username (UNIQUE), password_hash, email (UNIQUE), is_admin, created_at, last_login
# - weeks: id (PK), category_id (FK), week_number, title, display_name, description, assignment_url, due_date, is_active, created_at, last_modified
# - submissions: id (PK), student_name, week_id (FK), project_type, project_url, comment, admin_comment, status, submitted_at, last_modified, modified_by (FK)
#
# Relationships:
# - categories.id -> weeks.category_id (CASCADE DELETE)
# - weeks.id -> submissions.week_id (CASCADE DELETE)
# - users.id -> submissions.modified_by


