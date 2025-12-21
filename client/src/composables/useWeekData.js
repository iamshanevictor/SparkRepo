import { ref, watch } from 'vue'
import { api } from '../api'

// Simple cache to prevent duplicate API calls
const cache = new Map()
const CACHE_TTL = 30000 // 30 seconds

function getCacheKey(type, ...args) {
  return `${type}:${args.join(':')}`
}

function setCache(key, data) {
  cache.set(key, { data, timestamp: Date.now() })
}

function getCache(key) {
  const cached = cache.get(key)
  if (!cached) return null
  if (Date.now() - cached.timestamp > CACHE_TTL) {
    cache.delete(key)
    return null
  }
  return cached.data
}

export function clearCache() {
  cache.clear()
}

/**
 * Reusable composable for loading week data with caching
 */
export function useWeekData(categoryId, weekNumber) {
  const weekData = ref(null)
  const existingSubmission = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function loadWeekData() {
    if (!categoryId.value || !weekNumber.value) return
    
    loading.value = true
    error.value = null

    try {
      // Try cache first
      const cacheKey = getCacheKey('week', categoryId.value, weekNumber.value)
      const cached = getCache(cacheKey)
      
      if (cached) {
        weekData.value = cached.weekData
        existingSubmission.value = cached.submission
        loading.value = false
        return
      }

      // Load fresh data
      const [data, submission] = await Promise.allSettled([
        api.getWeek(categoryId.value, weekNumber.value),
        api.getSubmission(categoryId.value, weekNumber.value)
      ])

      weekData.value = data.status === 'fulfilled' ? data.value : null
      existingSubmission.value = submission.status === 'fulfilled' ? submission.value : null

      // Cache the result
      setCache(cacheKey, {
        weekData: weekData.value,
        submission: existingSubmission.value
      })

      if (data.status === 'rejected') {
        error.value = data.reason?.message || 'Failed to load week'
      }
    } catch (e) {
      error.value = e.message || 'Failed to load week data'
      console.error('Error loading week data:', e)
    } finally {
      loading.value = false
    }
  }

  function refresh() {
    const cacheKey = getCacheKey('week', categoryId.value, weekNumber.value)
    cache.delete(cacheKey)
    return loadWeekData()
  }

  // Watch for changes
  watch([categoryId, weekNumber], loadWeekData, { immediate: true })

  return {
    weekData,
    existingSubmission,
    loading,
    error,
    loadWeekData,
    refresh
  }
}

/**
 * Reusable composable for loading weeks list with caching
 */
export function useWeeksList(categoryId) {
  const weeks = ref([])
  const loading = ref(false)
  const error = ref(null)

  async function loadWeeks() {
    if (!categoryId.value) return
    
    loading.value = true
    error.value = null

    try {
      const cacheKey = getCacheKey('weeks', categoryId.value)
      const cached = getCache(cacheKey)

      if (cached) {
        weeks.value = cached
        loading.value = false
        return
      }

      const data = await api.getWeeks(categoryId.value)
      weeks.value = data.sort((a, b) => a.week_number - b.week_number)
      
      setCache(cacheKey, weeks.value)
    } catch (e) {
      error.value = e.message || 'Failed to load weeks'
      console.error('Error loading weeks:', e)
    } finally {
      loading.value = false
    }
  }

  watch(categoryId, loadWeeks, { immediate: true })

  return {
    weeks,
    loading,
    error,
    loadWeeks
  }
}
