import { ref } from 'vue'
import { api } from '../api'

// Simple cache for categories (they don't change often)
let categoriesCache = null
let cacheTimestamp = 0
const CACHE_TTL = 60000 // 1 minute

/**
 * Reusable composable for loading categories with caching
 */
export function useCategories() {
  const categories = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function loadCategories(forceRefresh = false) {
    const now = Date.now()
    
    // Return cached data if valid
    if (!forceRefresh && categoriesCache && (now - cacheTimestamp) < CACHE_TTL) {
      categories.value = categoriesCache
      return
    }

    loading.value = true
    error.value = null

    try {
      const data = await api.getCategories()
      
      // Sort: Scratch first, Canva second, others after
      const priority = (name) => {
        const lower = name.toLowerCase()
        if (lower.includes('scratch')) return 0
        if (lower.includes('canva')) return 1
        return 2
      }
      
      const sorted = [...data].sort((a, b) => {
        const pa = priority(a.name)
        const pb = priority(b.name)
        if (pa !== pb) return pa - pb
        return a.name.localeCompare(b.name)
      })
      
      categories.value = sorted
      categoriesCache = sorted
      cacheTimestamp = now
    } catch (e) {
      error.value = e.message || 'Failed to load categories'
      console.error('Error loading categories:', e)
    } finally {
      loading.value = false
    }
  }

  return {
    categories,
    loading,
    error,
    loadCategories
  }
}
