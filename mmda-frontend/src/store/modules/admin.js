import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all users
  users: null,
  // List of all collocation analyses
  collocation: null,
  // List of all discoursemes
  discoursemes: null,
  // List of all constellations
  constellations: null
}

const getters = {
  users (state) {
    return state.users
  },
  collocation (state) {
    return state.collocation
  },
  discoursemes (state) {
    return state.discoursemes
  },
  constellations (state) {
    return state.constellations
  }
}

const actions = {
  getAllUsers ({commit}) {
    // Get list of all users
    return new Promise((resolve, reject) => {
      api.get(`/admin/user/`).then(function (response) {
        commit('setUsers', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  createNewUser ({dispatch}, data) {
    // Create a new User
    return new Promise((resolve, reject) => {
      api.post(`/admin/user/`, data).then(function () {
        dispatch('getAllUsers')
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUser ({dispatch}, username) {
    // Delete a single user
    return new Promise((resolve, reject) => {

      api.delete(`/admin/user/${username}/`).then(function () {
        dispatch('getAllUsers')
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteObject ({dispatch}, data) {
    // Delete a single element
    return new Promise((resolve, reject) => {
      api.delete(`/admin/${data.object}/${data.object_id}/`).then(function () {
        dispatch('getAllCollocation')
        dispatch('getAllDiscoursemes')
        dispatch('getAllConstellations')
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getAllCollocation ({commit}) {
    // Get list of all collocation analyses
    return new Promise((resolve, reject) => {
      api.get(`/admin/collocation/`).then(function (response) {
        commit('setCollocation', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getAllDiscoursemes ({commit}) {
    // Get list of all discoursemes
    return new Promise((resolve, reject) => {
      api.get(`/admin/discourseme/`).then(function (response) {
        commit('setDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getAllConstellations ({commit}) {
    // Get list of all constellations
    return new Promise((resolve, reject) => {
      api.get(`/admin/constellation/`).then(function (response) {
        commit('setConstellations', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setUsers (state, users) {
    state.users = users
  },
  setCollocation (state, collocation) {
    state.collocation = collocation
  },
  setDiscoursemes (state, discoursemes) {
    state.discoursemes = discoursemes
  },
  setConstellations (state, constellations) {
    state.constellations = constellations
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
