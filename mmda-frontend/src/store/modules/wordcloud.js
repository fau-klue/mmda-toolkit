import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


const state = {
  windowSize: 3
}

const getters = {
  windowSize (state) {
    return state.windowSize
  }
}

const actions = {
  setWindowSize ({commit}, size) {
    commit('setWindowSize', size)
  }
}

const mutations = {
  setWindowSize (state, size) {
    state.windowSize = size
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
