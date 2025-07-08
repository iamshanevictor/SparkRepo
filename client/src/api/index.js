const API_BASE_URL = 'http://localhost:5000/api';

export const api = {
  async getCategories() {
    const response = await fetch(`${API_BASE_URL}/categories`);
    if (!response.ok) {
      throw new Error('Failed to fetch categories');
    }
    return response.json();
  },

  async getWeeks(categoryId) {
    const response = await fetch(`${API_BASE_URL}/categories/${categoryId}/weeks`);
    if (!response.ok) {
      throw new Error('Failed to fetch weeks');
    }
    return response.json();
  },

  async getWeek(categoryId, weekNumber) {
    const response = await fetch(`${API_BASE_URL}/categories/${categoryId}/weeks/${weekNumber}`);
    if (!response.ok) {
      throw new Error('Failed to fetch week data');
    }
    return response.json();
  }
};
