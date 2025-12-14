# Supabase Migration Setup Guide

This guide will walk you through setting up Supabase for your SparkRepo application after the migration from PostgreSQL/SQLAlchemy.

## Prerequisites

- A Supabase account (sign up at https://supabase.com)
- Your Supabase project created

## Step 1: Create a Supabase Project

1. Go to https://supabase.com and sign in (or create an account)
2. Click "New Project"
3. Fill in:
   - **Name**: Your project name (e.g., "sparkrepo")
   - **Database Password**: Choose a strong password (save this!)
   - **Region**: Choose the region closest to your users
   - **Pricing Plan**: Start with Free tier
4. Click "Create new project"
5. Wait for the project to be provisioned (takes 1-2 minutes)

## Step 2: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. You'll need these values:
   - **Project URL**: Found under "Project URL" (e.g., `https://xxxxx.supabase.co`)
   - **anon/public key**: Found under "Project API keys" → "anon public"
   - **service_role key**: Found under "Project API keys" → "service_role" (⚠️ Keep this secret!)

## Step 3: Set Up the Database Schema

1. In your Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Open the file `server/migrations/001_initial_schema.sql` from this repository
4. Copy the entire contents of that file
5. Paste it into the SQL Editor
6. Click "Run" (or press Ctrl+Enter)
7. You should see "Success. No rows returned" - this means the tables were created successfully

## Step 4: Configure Environment Variables

### For Local Development

1. Create or update `server/.env` file with:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key

# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Admin User (created on first run)
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# CORS
CORS_ORIGINS=http://localhost:5173
```

**Important**: 
- Replace `your-project-id`, `your-anon-public-key`, and `your-service-role-key` with your actual Supabase credentials
- Generate secure random strings for `SECRET_KEY` and `JWT_SECRET_KEY` (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)

### For Production (Render.com)

1. In your Render dashboard, go to your backend service
2. Go to **Environment** tab
3. Add these environment variables:

```
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-public-key
SUPABASE_SERVICE_KEY=your-service-role-key
FLASK_APP=app.py
FLASK_ENV=production
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_PASSWORD=your-secure-admin-password
CORS_ORIGINS=https://your-frontend-url.onrender.com
```

## Step 5: Install Dependencies

Make sure you have the updated dependencies installed:

```bash
cd server
pip install -r requirements.txt
```

The key dependencies are:
- `supabase==2.3.1` - Supabase Python client
- `Flask-JWT-Extended==4.6.0` - JWT authentication
- `python-dotenv==1.0.0` - Environment variable management

## Step 6: Seed the Database (Optional)

To populate your database with sample data:

```bash
cd server
python seed.py
```

This will create:
- An admin user (username: `admin`, password: `admin`)
- Sample categories (Beginner Scratch, Intermediate Canva)
- Sample weeks and submissions

**Note**: Change the admin password after first login!

## Step 7: Test Your Setup

1. Start your backend server:
   ```bash
   cd server
   python app.py
   ```

2. Test the health endpoint:
   ```bash
   curl http://localhost:5000/health
   ```

3. Test the API:
   ```bash
   curl http://localhost:5000/api/categories
   ```

4. Test admin login:
   ```bash
   curl -X POST http://localhost:5000/auth/login \
     -H "Content-Type: application/json" \
     -d '{"username": "admin", "password": "admin"}'
   ```

## Step 8: Verify Database Tables

In your Supabase dashboard:

1. Go to **Table Editor**
2. You should see these tables:
   - `categories`
   - `users`
   - `weeks`
   - `submissions`

3. Check that data exists (if you ran the seed script):
   - Go to each table and verify records exist

## Troubleshooting

### Error: "Missing Supabase URL or key"
- Make sure your `.env` file has `SUPABASE_URL` and `SUPABASE_KEY` set
- Check that the values are correct (no extra spaces)

### Error: "relation does not exist"
- Make sure you ran the SQL migration script (`001_initial_schema.sql`)
- Check the SQL Editor for any errors

### Error: "permission denied"
- Make sure you're using the `service_role` key for admin operations
- Check Row Level Security (RLS) policies in Supabase

### Authentication not working
- Verify `JWT_SECRET_KEY` is set in environment variables
- Check that the admin user was created (run `python scripts/seed_admin.py`)

## Security Notes

1. **Never commit your `.env` file** - it's already in `.gitignore`
2. **Keep your `SUPABASE_SERVICE_KEY` secret** - it bypasses RLS
3. **Use environment variables** for all secrets in production
4. **Change default admin password** after first login
5. **Review RLS policies** in Supabase for production security

## Next Steps

1. ✅ Database schema created
2. ✅ Environment variables configured
3. ✅ Dependencies installed
4. ✅ Database seeded (optional)
5. ✅ Application tested
6. 🔄 Deploy to production
7. 🔄 Update frontend API URL if needed
8. 🔄 Set up database backups in Supabase

## Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://github.com/supabase/supabase-py)
- [Flask-JWT-Extended Documentation](https://flask-jwt-extended.readthedocs.io/)

## Migration Checklist

- [x] Created Supabase project
- [ ] Got Supabase credentials (URL, anon key, service role key)
- [ ] Ran SQL migration script
- [ ] Configured environment variables
- [ ] Installed dependencies
- [ ] Tested local setup
- [ ] Seeded database (optional)
- [ ] Updated production environment variables
- [ ] Tested production deployment

