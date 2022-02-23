import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // Coordinates of a collocation analysis
  coordinates: null,
}

const getters = {
  coordinates (state) {
    return state.coordinates
  }
}

const actions = {
  getCollocationCoordinates ({commit}, data ) {
    // Get the coordinates of a collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.get(`/user/${data.username}/collocation/${data.collocation_id}/coordinates/`).then(function (response) {
        commit('setCoordinates', response.data)
        resolve( response.data )
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getKeywordCoordinates ({commit}, data ) {
    // Get the coordinates of an collocation
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword provided')

      api.get(`/user/${data.username}/keyword/${data.keyword_id}/coordinates/`).then(function (response) {
        commit('setCoordinates', response.data)
        resolve( response.data )
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  reloadCollocationCoordinates ({dispatch}, data) {
    // Reload the coordinates of a collocation analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.collocation_id) return reject('No collocation provided')

      api.put(`/user/${data.username}/collocation/${data.collocation_id}/coordinates/reload/`).then(function () {
        dispatch('getCollocationCoordinates', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  reloadKeywordCoordinates ({dispatch}, data) {
    // Reload the coordinates of a keyword analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.keyword_id)  return reject('No keyword provided')

      api.put(`/user/${data.username}/keyword/${data.keyword_id}/coordinates/reload/`).then(function () {
        dispatch('getKeywordCoordinates', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  setUserCoordinatesKeyword (unused, data) {
      // Reload the coordinates of a keyword analysis
      return new Promise((resolve, reject) => {

        if (!data.username)    return reject('No user provided')
        if (!data.keyword_id)  return reject('No keyword provided')

        api.put(`/user/${data.username}/keyword/${data.keyword_id}/coordinates/`, data.user_coordinates).then(function () {
          resolve()
        }).catch(function (error) {
          reject(error)
        })
      })
  },
  setUserCoordinates (unused, data) {
      // Reload the coordinates of a collocation analysis
      return new Promise((resolve, reject) => {

        if (!data.username)    return reject('No user provided')
        if (!data.collocation_id) return reject('No collocation provided')

        api.put(`/user/${data.username}/collocation/${data.collocation_id}/coordinates/`, data.user_coordinates).then(function () {
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
