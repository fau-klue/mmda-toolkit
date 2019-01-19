import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)


const state = {
  // List of all users
  users: null,
  // List of all analysis
  analysis: null,
  // List of all discoursemes
  discoursemes: null,
  // List of all positions
  positions: null
}

const getters = {
  users (state) {
    return state.users
  },
  analysis (state) {
    return state.analysis
  },
  discoursemes (state) {
    return state.discoursemes
  },
  positions (state) {
    return state.positions
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
  getAllAnalysis ({commit}) {
    // Get list of all analysis
    return new Promise((resolve, reject) => {
      api.get(`/admin/analysis/`).then(function (response) {
        commit('setAnalysis', response.data)
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
  getAllPositions ({commit}) {
    // Get list of all positions
    return new Promise((resolve, reject) => {
      api.get(`/admin/discursiveposition/`).then(function (response) {
        commit('setPositions', response.data)
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
  setAnalysis (state, analysis) {
    state.analysis = analysis
  },
  setDiscoursemes (state, discoursemes) {
    state.discoursemes = discoursemes
  },
  setPositions (state, positions) {
    state.positions = positions
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
