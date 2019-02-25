import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // List of all analysis
  userAnalysis: null,
  // One single analysis
  analysis: null,
  // List of discoursemes
  discoursemes: [],
  // Collocates of analysis
  collocates: null
}

const getters = {
  userAnalysis (state) {
    return state.userAnalysis
  },
  analysis (state) {
    return state.analysis
  },
  discoursemes (state) {
    return state.discoursemes
  },
  collocates (state) {
    return state.collocates
  }
}

const actions = {
  getUserSingleAnalysis ({commit}, data) {
    // Get one analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.get(`/user/${data.username}/analysis/${data.analysis_id}/`).then(function (response) {
        commit('setAnalysisSingle', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserAnalysis ({commit}, username) {
    // Get all analysis of a user
    return new Promise((resolve, reject) => {

      if (!username) return  reject('No user provided')

      api.get(`/user/${username}/analysis/`).then(function (response) {
        commit('setAnalysis', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getAnalysisDiscoursemes ({commit}, data) {
    // Get list of discoursmes of the analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.get(`/user/${data.username}/analysis/${data.analysis_id}/discourseme/`).then(function (response) {
        commit('setAnalysisDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserAnalysis ({commit}, data) { // eslint-disable-line no-unused-vars
    // Get all users analysis
    return new Promise((resolve, reject) => {

      if (!data.username) return reject('No user provided')

      api.post(`/user/${data.username}/analysis/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserAnalysis ({commit}, data) { // eslint-disable-line no-unused-vars
      // Update analysis details
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.put(`/user/${data.username}/analysis/${data.analysis_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserAnalysis ({commit}, data) {
    // Delete an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')

      api.delete(`/user/${data.username}/analysis/${data.analysis_id}/`).then(function () {
        commit('setAnalysisSingle', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addDiscoursemeToAnalysis ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Add a discourseme to an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.put(`/user/${data.username}/analysis/${data.analysis_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getAnalysisDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  removeDiscoursemeFromAnalysis ({commit, dispatch}, data) { // eslint-disable-line no-unused-vars
    // Remove a discourseme from an analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.delete(`/user/${data.username}/analysis/${data.analysis_id}/discourseme/${data.discourseme_id}/`).then(function () {
        dispatch('getAnalysisDiscoursemes', data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getAnalysisCollocates ({commit}, data) {
    // Get collocates analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')
      if (!data.window_size) return reject('No window size provided')

      let params = new URLSearchParams()
      // Append api/?window_size=12
      params.append("window_size", data.window_size)

      const request = {
        params: params
      }
      api.get(`/user/${data.username}/analysis/${data.analysis_id}/collocate/`, request).then(function (response) {
        commit('setCollocates', response.data);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
}

const mutations = {
  setAnalysis (state, analysis) {
    // List of analysis
    state.userAnalysis = analysis
  },
  setAnalysisDiscoursemes (state, discoursemes) {
    // List of discoursemes
    state.discoursemes = discoursemes
  },
  setAnalysisSingle (state, analysis) {
    // One analysis
    state.analysis = analysis
  },
  setCollocates (state, collocates) {
    // One analysis
    state.collocates = collocates
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
