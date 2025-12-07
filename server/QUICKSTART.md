# 🚀 SparkRepo Server - Quick Start Guide

## ✅ Pre-requisites Checklist

- [x] Python 3.8+ installed
- [x] Dependencies installed: `pip install -r requirements.txt`
- [x] Supabase project created
- [x] Environment variables configured in `.env`

## 🏃 Get Started in 3 Steps

### Step 1: Configure Environment
```bash
# Copy the example configuration
cp .env.example .env

# Edit .env with your Supabase credentials:
# SUPABASE_URL=https://your-project.supabase.co
# SUPABASE_KEY=your-public-anon-key
# SUPABASE_SERVICE_KEY=your-service-role-key
```

### Step 2: Install Dependencies
```bash
# Install all required packages
pip install -r requirements.txt
```

### Step 3: Start the Server
```bash
# Option 1: Using Python directly
python app.py

# Option 2: Using PowerShell script
.\run_backend.ps1
```

## ✅ Verify It's Working

### Health Check
```bash
# Should return: {"status":"healthy",...}
curl http://localhost:5000/health
```

### API Endpoints Test
```bash
# Get all categories
curl http://localhost:5000/api/categories

# Login (default admin)
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 📋 Server Features

- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Admin Management** - Role-based access control
- ✅ **Categories** - Manage course/project categories
- ✅ **Weekly Assignments** - Create and manage weekly tasks
- ✅ **Submissions** - Students submit project links
- ✅ **Logging** - Complete activity logging
- ✅ **Validation** - Comprehensive input validation
- ✅ **Error Handling** - Clear error messages

## 🔧 Common Issues & Solutions

### Issue: "SyntaxError: unexpected character..."
**Solution**: All syntax errors have been fixed. Re-install from latest code.

### Issue: "SUPABASE_URL not set"
**Solution**: Make sure `.env` file exists and has all required variables.
```bash
cp .env.example .env
# Then edit .env with your credentials
```

### Issue: "Connection refused"
**Solution**: Make sure your Supabase instance is accessible and credentials are correct.

### Issue: "Port 5000 already in use"
**Solution**: Change the port in `app.py` or kill the process using port 5000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

## 📁 Project Structure

```
server/
├── app.py                 # Flask application factory
├── api.py                 # Public API routes
├── auth.py                # Authentication routes
├── admin.py               # Admin routes
├── config.py              # Configuration classes
├── db_service.py          # Database service layer
├── supabase_client.py     # Supabase client
├── models.py              # Database schema reference
├── utils/
│   ├── logger.py          # Logging configuration
│   ├── exceptions.py      # Custom exceptions
│   ├── validators.py      # Input validators
│   └── errors.py          # Error response helpers
├── requirements.txt       # Python dependencies
├── .env.example           # Example environment config
├── init_db.py             # Database initialization helper
└── run_backend.ps1        # PowerShell startup script
```

## 🔐 Security Tips

1. **Change Admin Password**: Update `ADMIN_PASSWORD` in `.env`
2. **Secure JWT Secret**: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
3. **Use HTTPS**: In production, always use HTTPS URLs in `CORS_ORIGINS`
4. **Validate Input**: All user inputs are validated and sanitized
5. **Review Logs**: Check logs regularly for suspicious activity

## 📚 Documentation

- `REFACTORING_SUMMARY.md` - What was fixed and improved
- `FIXES_AND_REFACTORING.md` - Technical details of all changes
- `COMPLETION_CHECKLIST.md` - Verification checklist

## 🆘 Getting Help

### Check Logs
The server logs to both console and `sparkrepo.log` file. Check these for:
- Connection issues
- Authentication failures
- Validation errors
- Server errors

### API Documentation
All endpoints have docstrings. Reference:
- `/api/` - API discovery endpoint
- `/health` - Health check
- `api.py` - Public API routes
- `auth.py` - Authentication routes
- `admin.py` - Admin routes

### Test Endpoints
```bash
# Health check
curl http://localhost:5000/health

# API discovery
curl http://localhost:5000/api/

# List all categories
curl http://localhost:5000/api/categories

# Login
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 🎯 Next Steps

1. **Test the Backend**: Start server and run API tests
2. **Connect Frontend**: Configure frontend to use backend URL
3. **Create Admin User**: Use admin login to manage categories
4. **Add Categories**: Create project categories (Scratch, Canva, etc.)
5. **Create Weeks**: Add weekly assignments
6. **Deploy**: Follow deployment guide for production

---

**Status**: ✅ Server is production-ready!

**Last Updated**: December 7, 2025  
**Version**: 2.0 (Refactored)
