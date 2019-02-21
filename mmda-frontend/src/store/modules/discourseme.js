import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)

const state = {
  // All of users dicoursemes
  userDiscoursemes: null,
  // One discourseme
  discourseme: null
}

const getters = {
  userDiscoursemes (state) {
    return state.userDiscoursemes
  },
  discourseme (state) {
    return state.discourseme
  }
}

const actions = {
  getUserDiscourseme ({commit}, data) {
    // Get one discourseme
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.get(`/user/${data.username}/discourseme/${data.discourseme_id}/`).then(function (response) {
        commit('setDiscourseme', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getUserDiscoursemes ({commit}, username) {
    // Get all of users discoursemes
    return new Promise((resolve, reject) => {

      if (!username)    return reject('No user provided')

      api.get(`/user/${username}/discourseme/`).then(function (response) {
        commit('setDiscoursemes', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  addUserDiscourseme ({commit}, data) { // eslint-disable-line no-unused-vars
    // Create a new discourseme
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.post(`/user/${data.username}/discourseme/`, data).then(function (response) {
        resolve(response.data.msg) //return id
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  deleteUserDiscourseme ({commit}, data) {
    // Delete a dicourseme
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.delete(`/user/${data.username}/discourseme/${data.discourseme_id}/`).then(function () {
        commit('setDiscourseme', null)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserDiscourseme ({commit}, data) { // eslint-disable-line no-unused-vars
    // Update discourseme details
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.discourseme_id) return reject('No discourseme provided')

      api.put(`/user/${data.username}/discourseme/${data.discourseme_id}/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setDiscoursemes (state, discoursemes) {
    state.userDiscoursemes = discoursemes
  },
  setDiscourseme (state, discourseme) {
    state.discourseme = discourseme
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
