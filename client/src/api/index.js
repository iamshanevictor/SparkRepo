const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://cxraide-backend.onrender.com/api'
console.log("Frontend API Base URL:", API_BASE_URL)

function authHeaders() {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  const requestUrl = `${API_BASE_URL}${path}`
  console.log("Fetch Request URL:", requestUrl)
  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
      ...authHeaders(),
    },
  })
  if (!res.ok) {
    // Try to extract error message
    let message = `Request failed: ${res.status}`
    try {
      const data = await res.json()
      if (data?.error) message = data.error
    } catch {}
    throw new Error(message)
  }
  // No content
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  getCategories() {
    return request('/categories')
  },

  getWeeks(categoryId) {
    return request(`/categories/${categoryId}/weeks`)
  },

  getWeek(categoryId, weekNumber, includeSubmissions = false) {
    const q = includeSubmissions ? '?include_submissions=true' : ''
    return request(`/categories/${categoryId}/weeks/${weekNumber}${q}`)
  },

  // Submissions
  submitProject(categoryId, weekNumber, payload) {
    return request(`/categories/${categoryId}/weeks/${weekNumber}/submissions`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  // Auth
  login(username, password) {
    return request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password }),
    })
  },

  me() {
    return request('/auth/me')
  },

  // Admin
  getAdminWeeks() {
    return request('/admin/weeks')
  },
  updateWeek(weekId, payload) {
    return request(`/admin/weeks/${weekId}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },
  createWeek(categoryId, payload) {
    return request(`/admin/categories/${categoryId}/weeks`, {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },
  getAdminSubmissions(params = {}) {
    const query = new URLSearchParams(params).toString()
    const suffix = query ? `?${query}` : ''
    return request(`/admin/submissions${suffix}`)
  },
  updateSubmission(submissionId, payload) {
    return request(`/admin/submissions/${submissionId}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },
  deleteSubmission(submissionId) {
    return request(`/admin/submissions/${submissionId}`, {
      method: 'DELETE',
    })
  },
}
