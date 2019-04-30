import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)


const state = {
  windowSize: 3,
  rightSidebar: false,
  associationMeasure: null,
  showMinimap: true,
  secondOrderCollocationDiscoursemeIDs: [],
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
  },
  showMinimap (state) {
    return state.showMinimap
  },
  secondOrderCollocationDiscoursemeIDs(state){
    return state.secondOrderCollocationDiscoursemeIDs;
  }
}

const actions = {
  setWindowSize ({commit}, size) {
    commit('setWindowSize', size)
  },
  setRightSidebar ({commit}, val) {
    commit('setRightSidebar', val)
  },
  setAssociationMeasure ({commit}, val) {
    commit("setAssociationMeasure", val)
  },
  setShowMinimap ({commit}, val) {
    commit("setShowMinimap", val)
  },
  setSecondOrderCollocationDiscoursemeIDs({commit}, val){
    commit("setSecondOrderCollocationDiscoursemeIDs",val)
  }
}

const mutations = {
  setWindowSize (state, size) {
    state.windowSize = size
  },
  setRightSidebar (state, val) {
    state.rightSidebar = val
  },
  setAssociationMeasure (state, val) {
    state.associationMeasure = val
  },
  setShowMinimap (state, val) {
    state.showMinimap = val
  },
  setSecondOrderCollocationDiscoursemeIDs (state, val){
    state.secondOrderCollocationDiscoursemeIDs = val;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
