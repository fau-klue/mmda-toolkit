import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // Coordinates of an analysis
  coordinates: null,
}

const getters = {
  coordinates (state) {
    return state.coordinates
  }
}

const actions = {
  getAnalysisCoordinates ({commit}, data ) {
    // Get the coordinates of an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.get(`/user/${data.username}/analysis/${data.analysis_id}/coordinates/`).then(function (response) {
        commit('setCoordinates', response.data)
        resolve( response.data )
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  reloadAnalysisCoordinates ({dispatch}, data) {
    // Reload the coordinates of an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.put(`/user/${data.username}/analysis/${data.analysis_id}/coordinates/reload/`).then(function () {
        dispatch('getAnalysisCoordinates', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  setUserCoordinates ({dispatch}, data) {
      // Reload the coordinates of an analysis
      return new Promise((resolve, reject) => {

        if (!data.username)    return reject('No user provided')
        if (!data.analysis_id) return reject('No analysis provided')

        api.put(`/user/${data.username}/analysis/${data.analysis_id}/coordinates/`, data.user_coordinates).then(function () {
          dispatch('getAnalysisCoordinates', data)
          resolve()
        }).catch(function (error) {
          reject(error)
        })
      })
    }
}

const mutations = {
  setCoordinates (state, coordinates) {
    state.coordinates = coordinates
  },
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
