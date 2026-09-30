import axios from 'axios'

const api = axios.create({ baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8001/api', timeout: 30000 })

export async function analyzeImage(file) {
  const formData = new FormData()
  formData.append('image', file)
  const { data } = await api.post('/analyze', formData)
  return data
}

export async function compareProduct(productName) {
  const { data } = await api.post('/compare', { product_name: productName, keywords: [productName] })
  return data
}
