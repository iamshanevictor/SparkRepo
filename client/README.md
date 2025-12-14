# SparkRepo Frontend (Vue 3 + Vite)

This is the Vue 3 frontend for SparkRepo.

## Environment

Copy the example env and adjust if needed:

```powershell
Copy-Item .env.example .env
```

Key variables:

- `VITE_API_URL` (default `http://localhost:5000/api`)

## Scripts

Dev server (Vite + HMR):

```powershell
./run_frontend.ps1
```

Or using npm directly:

```bash
npm install
npm run dev
```

## Architecture Notes

- Centralized API client: `src/api/index.js` (handles base URL, auth headers, errors)
- Auth composable: `src/composables/useAuth.js`
- Generic upload form: `src/components/UploadForm.vue` (adapts to Scratch/Canva based on `categoryInfo.name`)
- Admin dashboard split components: `src/components/admin/WeeksTable.vue`, `src/components/admin/SubmissionsTable.vue`

## Linting

An ESLint config is included (`.eslintrc.cjs`). Run lint:

```bash
npm run lint
```
