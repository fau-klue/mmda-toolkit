import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

// Use a custom api without interceptor. Otherwise we cant change the token to the refresh token
const api = axios.create({
  baseURL: process.env.VUE_APP_API_BASE_URL || 'http://localhost:5000/api/',
})

/**
 * Adds 14 min to a date, which is one less than the default (15min) of Flask JWT Extended
 * https://flask-jwt-extended.readthedocs.io/en/latest/options.html#configuration-options
 * @param date  Date to start with
 */
function calculateExpirationDate(date) {
  const minutes = 14
  return new Date(date.getTime() + minutes*60000)
}

/**
 * Check if token ist expired
 */
function isExpired() {
  const now = new Date()
  const expiration = localStorage.getItem('jwt_expiration')
  if (expiration === null) {
    return true
  }
  return now.getTime() >= Date.parse(expiration)
}

const state = {
  user: null,
  authenticated: false,
}

const getters = {
  user (state) {
    return state.user
  },
  isAdmin (state) {
    if (state.user === null || state.user.roles === undefined) {
      return false
    }
    return state.user.roles.includes('admin')
  },
  isAuthenticated (state) {
    return state.user !== null
  },
}

const actions = {
  clearJWT ({commit}) {
    // Removes all user data from the local storage
    return new Promise((resolve) => {
      commit('setAuthenticated', false)
      commit('setUser', null)
      localStorage.removeItem('jwt')
      localStorage.removeItem('jwt_refresh')
      localStorage.removeItem('jwt_expiration')
      resolve()
    })
  },
  fetchJWT ({commit}, credentials ) {
    // Get a fresh JWT from the backend
    localStorage.removeItem('jwt')
    return new Promise((resolve, reject) => {
      api.post('/login/', credentials).then(function (response) {
        // Stores the return values and the expiration date in the browser's local storags
        localStorage.jwt = response.data.access_token
        localStorage.jwt_refresh = response.data.refresh_token
        localStorage.jwt_expiration = calculateExpirationDate(new Date())
        commit('setUser', response.data.current_identity)
        commit('setAuthenticated', true)
        resolve()
      }).catch(function (error) {
        commit('setUser', null)
        commit('setAuthenticated', false)
        reject(error)
      })
    })
  },
  refreshJWT () {
    // Use the refresh token to get a new JWT token
    const config = {'headers': {'Authorization': 'Bearer ' + localStorage.getItem('jwt_refresh')}}

    return new Promise((resolve, reject) => {
      api.post('/refresh/', null, config).then(function (response) {
        // Store the new JWT and expiration date in the local storage
        localStorage.jwt = response.data.access_token
        localStorage.jwt_expiration = calculateExpirationDate(new Date())
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })

  },
  testJWT ({commit, dispatch, getters} ) {
    // Rest if the JWT is still valid
    return new Promise((resolve, reject) => {

      // If we're already authenticated, we're good
      if (getters.isAuthenticated) {
        resolve()
        return
      }

      const token = localStorage.getItem('jwt')
      const refreshToken = localStorage.getItem('jwt_refresh')

      // Do we have a token at all?
      if (!token || !refreshToken) {
        reject('No tokens')
        return
      }

      // Ok, we have one, but is is expired? If so, try to refresh.
      if (refreshToken && isExpired()){
        dispatch('refreshJWT').catch(function (error) {
          reject(error)
          return
        })
      }

      // Get the old or new token
      const config = {'headers': {'Authorization': 'Bearer ' + localStorage.getItem('jwt')}}

      // Test if the token is good and set the user
      api.get('/test-login/', config).then(function (response) {
        commit('setUser', response.data.current_identity)
        commit('setAuthenticated', true)
        resolve()
      }).catch(function (error) {
        commit('setUser', null)
        commit('setAuthenticated', false)
        reject(error)
      })
    })
  }
}

const mutations = {
  setUser (state, user) {
    state.user = user
  },
  setAuthenticated (state, status) {
    state.authenticated = status
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
