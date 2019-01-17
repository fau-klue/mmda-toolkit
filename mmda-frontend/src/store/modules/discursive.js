import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all positions
  userDiscursivePositions: null,
  // One single position
  discursivePosition: null,
  // DiscursivePosition Discoursemes
  discoursemes: []
}

const getters = {
  userDiscursivePositions (state) {
    return state.userDiscursivePositions
  },
  discursivePosition (state) {
    return state.discursivePosition
  },
  discoursemes (state) {
    return state.discoursemes
  }
}

const actions = {
  getUserSingleDiscursivePosition ({commit}, data) {
    // Get a single Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${data.username}/discursiveposition/${data.position_id}/`).then(function (response) {
        commit('setDiscursivePositionSingle', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserDiscursivePositions ({commit}, username) {
    // Get all of users Discursive Positions
    return new Promise((resolve, reject) => {

      if (!username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${username}/discursiveposition/`).then(function (response) {
        commit('setDiscursivePositions', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getDiscursivePositionDiscoursemes ({commit}, data) {
    // Get Discursive Positions discoursemes
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${data.username}/discursiveposition/${data.position_id}/discourseme/`).then(function (response) {
        commit('setDiscursivePositionDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserDiscursivePosition ({commit}, data) { // eslint-disable-line no-unused-vars
    // Add a new Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.post(`/user/${data.username}/discursiveposition/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserDiscursivePosition ({commit}, data) { // eslint-disable-line no-unused-vars
    // Update details of a Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.put(`/user/${data.username}/discursiveposition/${data.position_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserDiscursivePosition ({commit}, data) {
    // Delete a Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.delete(`/user/${data.username}/discursiveposition/${data.position_id}/`).then(function () {
        commit('setDiscursivePositionSingle', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addDiscoursemeToDiscursivePosition ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Add a discourseme to a Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.put(`/user/${data.username}/discursiveposition/${data.position_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getDiscursivePositionDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  removeDiscoursemeFromDiscursivePosition ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Remove a discourseme from a Discursive Position
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.delete(`/user/${data.username}/discursiveposition/${data.position_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getDiscursivePositionDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setDiscursivePositions (state, discursivePositions) {
    // List of discursivePosition
    state.userDiscursivePositions = discursivePositions
  },
  setDiscursivePositionDiscoursemes (state, discoursemes) {
    // List of discursivePosition
    state.discoursemes = discoursemes
  },
  setDiscursivePositionSingle (state, discursivePosition) {
    // One discursivePosition
    state.discursivePosition = discursivePosition
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
