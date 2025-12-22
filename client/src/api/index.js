const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'
const FULL_API_URL = API_BASE_URL.endsWith('/api') ? API_BASE_URL : `${API_BASE_URL}/api`
console.log("Frontend API Base URL:", FULL_API_URL)

// Request deduplication - prevent duplicate simultaneous requests
const pendingRequests = new Map()

function authHeaders() {
  const token = localStorage.getItem('access_token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function request(path, options = {}) {
  const requestUrl = `${FULL_API_URL}${path}`
  const requestKey = `${options.method || 'GET'}:${requestUrl}`
  
  // Check if same request is already in progress
  if (pendingRequests.has(requestKey)) {
    console.log("Reusing pending request:", requestKey)
    return pendingRequests.get(requestKey)
  }

  console.log("Fetch Request URL:", requestUrl)
  
  const requestPromise = fetch(requestUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
      ...authHeaders(),
    },
  }).then(async (res) => {
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
  }).finally(() => {
    // Remove from pending after completion
    pendingRequests.delete(requestKey)
  })

  // Store pending request
  pendingRequests.set(requestKey, requestPromise)
  
  return requestPromise
}

export const api = {
  getCategories() {
    return request('/categories').then((data) => data.categories || [])
  },

  getWeeks(categoryId) {
    return request(`/categories/${categoryId}/weeks`).then((data) => data.weeks || [])
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
    }).then((data) => data?.submission || data)
  },

  getWeekSubmissions(weekId) {
    return request(`/weeks/${weekId}/submissions`).then((data) => data.submissions || [])
  },

  // Note: This endpoint doesn't exist yet on backend
  // Returns null if user hasn't submitted yet
  getSubmission(categoryId, weekNumber) {
    return request(`/categories/${categoryId}/weeks/${weekNumber}/submission`).catch(() => null)
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
    return request('/admin/weeks').then((data) => data.weeks || [])
  },
  updateWeek(weekId, payload) {
    return request(`/admin/weeks/${weekId}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },
  deleteWeek(weekId) {
    return request(`/admin/weeks/${weekId}`, {
      method: 'DELETE',
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
    return request(`/admin/submissions${suffix}`).then((data) => data.submissions || [])
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
