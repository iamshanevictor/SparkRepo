# Firebase Setup Guide for SparkRepo

This guide will help you set up Firebase for your SparkRepo application.

> Important: Never commit your service account key to the repository. Keep `serviceAccountKey.json` local and ignored by Git, or use the `FIREBASE_SERVICE_ACCOUNT_KEY` environment variable.

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or "Create a project"
3. Enter project name: `sparkrepo` (or your preferred name)
4. **Disable Google Analytics** (optional, not needed for this project)
5. Click "Create project"

## Step 2: Enable Firestore Database

1. In your Firebase project, click "Firestore Database" in the left sidebar
2. Click "Create database"
3. Select "Start in production mode" (we'll set rules later)
4. Choose a Cloud Firestore location (select closest to your users):
   - For North America: `us-central1`
   - For Europe: `europe-west1`
   - For Asia: `asia-southeast1`
5. Click "Enable"

## Step 3: Set Firestore Security Rules

1. In Firestore Database, click on "Rules" tab
2. Replace the default rules with:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Allow public read for categories and weeks
    match /categories/{category} {
      allow read: if true;
      allow write: if false;  // Only admin via backend
    }
    
    match /weeks/{week} {
      allow read: if true;
      allow write: if false;  // Only admin via backend
    }
    
    // Allow public write for submissions (students can submit)
    match /submissions/{submission} {
      allow read: if true;
      allow create: if true;  // Students can create submissions
      allow update, delete: if false;  // Only admin via backend
    }
    
    // Users collection - no public access
    match /users/{user} {
      allow read, write: if false;  // Only backend access
    }
  }
}
```

3. Click "Publish"

## Step 4: Generate Service Account Key

1. Click the gear icon (⚙️) next to "Project Overview"
2. Select "Project settings"
3. Go to the "Service accounts" tab
4. Click "Generate new private key"
5. Click "Generate key" - a JSON file will download
6. **IMPORTANT:** Keep this file secure! Don't commit it to Git

## Step 5: Configure Local Development

### Option A: Using JSON File (Development)

1. Rename the downloaded JSON file to `serviceAccountKey.json`
2. Move it to the `server/` directory
3. Add to `.gitignore` (already done):
   ```
   serviceAccountKey.json
   ```

4. Create `.env` file in `server/` directory:
   ```bash
   # Firebase
   FIREBASE_SERVICE_ACCOUNT_PATH=serviceAccountKey.json
   
   # Flask
   FLASK_ENV=development
   FLASK_SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-here
   JWT_ACCESS_TOKEN_EXPIRES=86400
   
   # Admin User
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=admin123
   
   # CORS
   CORS_ORIGINS=http://localhost:5173
   
   # Port
   PORT=5000
   ```

### Option B: Using Environment Variable (Production)

1. Convert JSON file to single line:
   ```bash
   # On Windows PowerShell:
   $json = Get-Content serviceAccountKey.json -Raw | ConvertFrom-Json | ConvertTo-Json -Compress
   Write-Host $json
   
   # On Mac/Linux:
   cat serviceAccountKey.json | jq -c
   ```

2. Add to your `.env`:
   ```bash
   FIREBASE_SERVICE_ACCOUNT_KEY='{"type":"service_account","project_id":"..."}'
   ```

## Step 6: Install Dependencies

```bash
cd server
pip install -r requirements.txt
```

## Step 7: Test Firebase Connection

Run the Flask application:

```bash
cd server
python app.py
```

You should see:
```
INFO - Firebase initialized successfully
INFO - Default admin user created: admin
INFO - SparkRepo application initialized successfully
```

Test the API:
```bash
# Check health endpoint
curl http://localhost:5000/health

# Should return:
# {"status": "healthy", "database": "connected"}
```

## Step 8: Initialize Data (Optional)

### Create Sample Category

```bash
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copy the access_token from response, then:

curl -X POST http://localhost:5000/admin/categories \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"name":"Scratch Projects","description":"Learn coding with Scratch"}'
```

### Create Sample Week

```bash
# Use category_id from previous response

curl -X POST http://localhost:5000/admin/categories/CATEGORY_ID/weeks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "week_number": 1,
    "title": "Week 1: Introduction to Scratch",
    "display_name": "Introduction to Scratch",
    "description": "Learn the basics of Scratch programming",
    "is_active": true
  }'
```

## Step 9: Deploy to Render.com

### Set Environment Variables in Render

1. Go to your Render dashboard
2. Select your web service
3. Go to "Environment" tab
4. Add these variables:

```
FLASK_ENV=production
FLASK_SECRET_KEY=<generate-random-string>
JWT_SECRET_KEY=<generate-random-string>
JWT_ACCESS_TOKEN_EXPIRES=86400
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<secure-password>
CORS_ORIGINS=https://your-frontend-url.com
FIREBASE_SERVICE_ACCOUNT_KEY=<paste-single-line-json-here>
```

### Generate Secure Keys

```bash
# On Windows PowerShell:
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 32 | % {[char]$_})

# On Mac/Linux:
openssl rand -hex 32
```

## Firestore Collections Structure

Your Firebase will have these collections:

### categories
```json
{
  "id": "auto-generated",
  "name": "Scratch Projects",
  "description": "Learn coding with Scratch",
  "created_at": "2025-01-15T10:00:00Z"
}
```

### users
```json
{
  "id": "auto-generated",
  "username": "admin",
  "password_hash": "hashed-password",
  "email": "admin@sparkrepo.com",
  "is_admin": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

### weeks
```json
{
  "id": "auto-generated",
  "category_id": "ref-to-category",
  "week_number": 1,
  "title": "Week 1: Introduction",
  "display_name": "Introduction",
  "description": "Learn the basics",
  "assignment_url": "https://...",
  "due_date": "2025-06-15T23:59:59Z",
  "is_active": true,
  "created_at": "2025-01-15T10:00:00Z"
}
```

### submissions
```json
{
  "id": "auto-generated",
  "week_id": "ref-to-week",
  "student_name": "John Doe",
  "project_url": "https://scratch.mit.edu/projects/123",
  "status": "pending",
  "admin_comment": null,
  "submitted_at": "2025-01-15T14:30:00Z",
  "modified_by": null
}
```

## Troubleshooting

### Error: "Firebase credentials not found"

- Check that `FIREBASE_SERVICE_ACCOUNT_KEY` or `FIREBASE_SERVICE_ACCOUNT_PATH` is set
- Verify JSON is valid (use a JSON validator)
- Make sure file path is correct (relative to `server/` directory)

### Error: "Permission denied" when accessing Firestore

- Check Firestore security rules
- Verify service account has proper permissions in Firebase Console

### Error: "Failed to initialize Firebase"

- Check that project_id in service account matches your Firebase project
- Verify service account key hasn't been deleted in Firebase Console
- Check network connectivity to Firebase

### Cannot create admin user

- Check logs for specific error
- Verify `ADMIN_USERNAME` and `ADMIN_PASSWORD` are set in environment
- Try manually creating user via Firebase Console

## Next Steps

1. ✅ Firebase is now set up and connected
2. Test all API endpoints (categories, weeks, submissions)
3. Update frontend `VITE_API_URL` to point to your backend
4. Deploy to Render.com
5. Configure production security rules in Firestore

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/get-started)
- [Firebase Admin SDK for Python](https://firebase.google.com/docs/admin/setup)
- [Render.com Documentation](https://render.com/docs)
