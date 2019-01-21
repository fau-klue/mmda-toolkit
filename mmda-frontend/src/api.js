import axios from 'axios'

// Default API Instance to use for requests.
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000/api/',
})

// Add the JWT Token to each request so you dont have to
api.interceptors.request.use(
  config => {
    config.headers.common = {'Authorization': 'Bearer ' + localStorage.getItem('jwt')}
    return config
  },
  error => Promise.reject(error)
)

export default api
