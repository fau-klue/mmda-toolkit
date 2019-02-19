import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


const state = {
  windowSize: 3,
  rightSidebar: false,
  associationMeasure: null,
}

const getters = {
  windowSize (state) {
    return state.windowSize
  },
  rightSidebar (state) {
    return state.rightSidebar
  },
  associationMeasure (state) {
    return state.associationMeasure
  }
}

const actions = {
  setWindowSize ({commit}, size) {
    commit('setWindowSize', size)
  },
  setRightSidebar ({commit}, val){
    commit('setRightSidebar', val)
  },
  setAssociationMeasure ({commit}, val){
    commit("setAssociationMeasure", val)
  }
}

const mutations = {
  setWindowSize (state, size) {
    state.windowSize = size
  },
  setRightSidebar (state, val){
    state.rightSidebar = val
  },
  setAssociationMeasure (state, val){
    state.associationMeasure = val
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
