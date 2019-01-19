import Vue from 'vue'
import Vuex from 'vuex'
import api from '@/api'

Vue.use(Vuex)


const state = {
  // List of all users
  users: null
}

const getters = {
  users (state) {
    return state.users
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
    return new Promise((resolve, reject) => {

      api.post(`/admin/user/`, data).then(function () {
        dispatch('getAllUsers')
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
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
