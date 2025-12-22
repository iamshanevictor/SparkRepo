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
  const weekSubmissions = ref([])
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
        weekSubmissions.value = cached.weekSubmissions || []
        loading.value = false
        return
      }

      // Load fresh data
      const [weekResult] = await Promise.allSettled([
        api.getWeek(categoryId.value, weekNumber.value)
      ])

      weekData.value = weekResult.status === 'fulfilled' ? weekResult.value : null
      existingSubmission.value = null // No per-student submission lookup (no accounts)

      // Load submissions for the week (used for the "Submitted" panel name list)
      if (weekData.value?.id) {
        try {
          weekSubmissions.value = await api.getWeekSubmissions(weekData.value.id)
        } catch {
          weekSubmissions.value = []
        }
      } else {
        weekSubmissions.value = []
      }

      // Cache the result
      setCache(cacheKey, {
        weekData: weekData.value,
        submission: existingSubmission.value,
        weekSubmissions: weekSubmissions.value
      })

      if (weekResult.status === 'rejected') {
        error.value = weekResult.reason?.message || 'Failed to load week'
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
    weekSubmissions,
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
