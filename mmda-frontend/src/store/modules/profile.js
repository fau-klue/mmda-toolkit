import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)


const state = {
  userProfile: null
}

const getters = {
  userProfile (state) {
    return state.userProfile
  }
}

const actions = {
  getUserProfile ({commit}, username) {
    return new Promise((resolve, reject) => {

      if (!username) {
        reject('No user provided')
        return
      }

      api.get(`/user/${username}/`).then(function (response) {
        commit('setProfile', response.data)
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  updateUserPassword ({commit}, data) { // eslint-disable-line no-unused-vars
    return new Promise((resolve, reject) => {

      if (!data.username) {
        reject('No user provided')
        return
      }

      api.put(`/user/${data.username}/password/`, data).then(function () {
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  }
}

const mutations = {
  setProfile (state, profile) {
    state.userProfile = profile
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
