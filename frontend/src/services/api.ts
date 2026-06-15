import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 品牌管理API
export const getBrands = async () => {
  const response = await api.get('/brands/')
  return response.data
}

export const createBrand = async (data: any) => {
  const response = await api.post('/brands/', data)
  return response.data
}

export const updateBrand = async (id: number, data: any) => {
  const response = await api.put(`/brands/${id}`, data)
  return response.data
}

export const deleteBrand = async (id: number) => {
  const response = await api.delete(`/brands/${id}`)
  return response.data
}

// 新闻搜索API
export const searchNews = async (keyword: string, days: number = 7, limit: number = 20) => {
  const response = await api.get('/news/search', {
    params: { keyword, days, limit }
  })
  return response.data
}

export const getBrandNews = async (brandId: number, days: number = 7) => {
  const response = await api.get(`/news/brand/${brandId}`, {
    params: { days }
  })
  return response.data
}

export const getLatestNews = async (limit: number = 20) => {
  const response = await api.get('/news/latest', {
    params: { limit }
  })
  return response.data
}

export const getNegativeNews = async (days: number = 7) => {
  const response = await api.get('/news/negative', {
    params: { days }
  })
  return response.data
}

// 展板数据API
export const getDashboardStats = async () => {
  const response = await api.get('/dashboard/stats')
  return response.data
}

export const getTop20News = async (date?: string) => {
  const response = await api.get('/dashboard/top20', {
    params: { date }
  })
  return response.data
}

export const getSentimentTrends = async (days: number = 7) => {
  const response = await api.get('/dashboard/trends', {
    params: { days }
  })
  return response.data
}

export const getBrandDistribution = async (days: number = 7) => {
  const response = await api.get('/dashboard/brand-distribution', {
    params: { days }
  })
  return response.data
}
