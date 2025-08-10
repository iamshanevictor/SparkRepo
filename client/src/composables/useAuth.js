const TOKEN_KEY = 'access_token'
const USER_KEY = 'user'

export function useAuth() {
  const getToken = () => localStorage.getItem(TOKEN_KEY)
  const getUser = () => {
    const raw = localStorage.getItem(USER_KEY)
    try {
      return raw ? JSON.parse(raw) : null
    } catch {
      return null
    }
  }

  const isAuthenticated = () => Boolean(getToken())
  const isAdmin = () => Boolean(getUser()?.is_admin)

  const login = (token, user) => {
    localStorage.setItem(TOKEN_KEY, token)
    localStorage.setItem(USER_KEY, JSON.stringify(user))
  }

  const logout = () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  return { getToken, getUser, isAuthenticated, isAdmin, login, logout }
}
