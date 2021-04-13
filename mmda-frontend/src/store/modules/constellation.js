import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all constellations
  userConstellations: null,
  // One single constellation
  constellation: null,
  // Constellation Concordances
  concordances: [],
  // Constellation Discoursemes
  discoursemes: []
}

const getters = {
  userConstellations (state) {
    return state.userConstellations
  },
  constellation (state) {
    return state.constellation
  },
  concordances (state) {
    return state.concordances
  },
  discoursemes (state) {
    return state.discoursemes
  }
}

const actions = {
  getUserSingleConstellation ({commit}, data) {
    // Get a single Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${data.username}/constellation/${data.constellation_id}/`).then(function (response) {
        commit('setConstellationSingle', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserConstellations ({commit}, username) {
    // Get all of users Constellations
    return new Promise((resolve, reject) => {

      if (!username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${username}/constellation/`).then(function (response) {
        commit('setConstellations', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getConstellationDiscoursemes ({commit}, data) {
    // Get Constellation discoursemes
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${data.username}/constellation/${data.constellation_id}/discourseme/`).then(function (response) {
        commit('setConstellationDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserConstellation ({commit}, data) { // eslint-disable-line no-unused-vars
    // Add a new Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.post(`/user/${data.username}/constellation/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserConstellation ({commit}, data) { // eslint-disable-line no-unused-vars
    // Update details of a Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.put(`/user/${data.username}/constellation/${data.constellation_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserConstellation ({commit}, data) {
    // Delete a Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.delete(`/user/${data.username}/constellation/${data.constellation_id}/`).then(function () {
        commit('setConstellationSingle', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addDiscoursemeToConstellation ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Add a discourseme to a Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.put(`/user/${data.username}/constellation/${data.constellation_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getConstellationDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  removeDiscoursemeFromConstellation ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Remove a discourseme from a Constellation
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.delete(`/user/${data.username}/constellation/${data.constellation_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getConstellationDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getConstellationConcordances ({commit}, data) {
    // Get Constellations discoursemes
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.constellation_id) return reject('No Constellation provided')
      if (!data.corpora) return reject('No Corpora provided')
      if (!data.analysis) return reject('No Analysis provided')
      if (!data.window_size) return reject('No window size provided')

      let params = new URLSearchParams()
      // Concat corpus parameter. api/?corpus=foo&corpus=bar
      data.corpora.forEach((corpus)=>{ params.append("corpus", corpus) })
      // Add &analysis=123
	params.append("analysis", data.analysis)
	params.append("window_size", data.window_size)

      const request = {
        params: params
      }
      api.get(`/user/${data.username}/constellation/${data.constellation_id}/concordance/`, request).then(function (response) {
        commit('setConstellationConcordances', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setConstellations (state, constellations) {
    // List of Constellations
    state.userConstellations = constellations
  },
  setConstellationDiscoursemes (state, discoursemes) {
    // List of Discoursemes
    state.discoursemes = discoursemes
  },
  setConstellationConcordances (state, concordances) {
    // List of Concordances: [{corpusName: concordances}]
    state.concordances = concordances
  },
  setConstellationSingle (state, constellation) {
    // One Constellation
    state.constellation = constellation
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
