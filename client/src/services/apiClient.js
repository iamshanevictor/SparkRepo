// Centralized API client for the frontend
// Uses Vite env var VITE_API_BASE_URL when provided, otherwise relative paths

const API_BASE = import.meta.env.VITE_API_BASE_URL || ''

function buildUrl(path) {
  if (API_BASE) {
    // Ensure no double slashes
    return `${API_BASE.replace(/\/$/, '')}${path.startsWith('/') ? '' : '/'}${path}`
  }
  return path
}

export async function apiGet(path, options = {}) {
  const res = await fetch(buildUrl(path), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export async function apiPost(path, body = {}, options = {}) {
  const res = await fetch(buildUrl(path), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    body: JSON.stringify(body),
    ...options,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export async function apiPut(path, body = {}, options = {}) {
  const res = await fetch(buildUrl(path), {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    body: JSON.stringify(body),
    ...options,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  return res.json()
}

export async function apiDelete(path, options = {}) {
  const res = await fetch(buildUrl(path), {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
    ...options,
  })
  if (!res.ok) throw new Error(`${res.status} ${res.statusText}`)
  try { return await res.json() } catch { return null }
}

export function withAuthHeaders(token) {
  return token ? { Authorization: `Bearer ${token}` } : {}
}
