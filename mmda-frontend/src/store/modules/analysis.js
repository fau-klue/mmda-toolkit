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
  collocates: null,

  concordances: null,
  concordances_loading : null,
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
  },
  concordances (state) {
    return state.concordances
  },
  concordances_loading (state) {
    return state.concordances_loading
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
  getAnalysisDiscoursemeCollocates ({commit}, data) {
    // Get collocates analysis
    return new Promise((resolve, reject) => {

      if (!data.username)    return reject('No user provided')
      if (!data.analysis_id) return reject('No analysis provided')
      if (!data.window_size) return reject('No window size provided')
      if (!data.discourseme_items&&!data.discourseme_id&&!data.discourseme_ids) return reject('No discourseme_[items, id or ids]')

      let params = new URLSearchParams()
      // Append api/?window_size=12
      params.append("window_size", data.window_size)
     
      if(data.discourseme_items) for(var it of data.discourseme_items) params.append("collocate", it);
      if(data.discourseme_id) params.append("discourseme",data.discourseme_id);
      if(data.discourseme_ids) for(var ids of data.discourseme_ids) params.append("discourseme", ids);

      const request = {
        params: params
      }
      //console.log(data);
      api.get(`/user/${data.username}/analysis/${data.analysis_id}/collocate/`, request).then(function (response) {
        commit('setCollocates', response.data);
        //console.log(response.data.t_score);
        resolve()
      }).catch(function (error) {
        reject(error)
      })
    })
  },
  getConcordances ({commit}, data ) {
    // Get Concordances
    return new Promise((resolve, reject) => {

      //if (!data.corpus) return reject('No corpus provided')
      if (!data.username) return reject('No username provided')
      if (data.analysis_id===undefined) return reject('No analysis_id provided')
      //if (!data.topic_items) return reject('No topic items provided')

      let params = new URLSearchParams()
      // Concat item parameter. api/?item=foo&item=bar
      //data.topic_items.forEach((item)=>{ params.append("item", item) })

      if(data.collocate_items){
        // Concat item parameter. api/?collocate=foo&collocate=bar
        //data.collocate_items.forEach((item)=>{ params.append("collocate", item) })
        data.collocate_items.forEach((item)=>{ params.append("item", item) })
      }

      //Second order concordances
      //if(data.discourseme_items) for(var it of data.discourseme_items) params.append("collocate", it);
      if(data.discourseme_id) params.append("discourseme",data.discourseme_id);
      if(data.discourseme_ids) for(var it of data.discourseme_ids) params.append("discourseme", it);

      if(data.window_size){
         // Append api/?window_size=12
         //console.log("Ws "+data.window_size);
         params.append("window_size", data.window_size)
      }

      const request = {
        params: params
      }
      //console.log("req called");
      commit('setConcordancesLoading', data);
      api.get(`/user/${data.username}/analysis/${data.analysis_id}/concordance/`, request).then(function (response) {
        // only accept the loading, if data is the latest call
        // otherwise another request has happened and this one is invalid
        //  TODO:: cancel prevous requests upon a new one (i.e. notify the server to drop the activity)
        if(data == state.concordances_loading){
          //console.log("req fullfilled");
          commit('setConcordances', response.data)
          commit('setConcordancesLoading',null)
        //}else{
        //  console.log("req dropped");
        }
        resolve()
      }).catch(function (error) {
        commit('setConcordances',null)
        commit('setConcordancesLoading',null)
        reject(error)
      })
    })
  },
  cancelConcordanceRequest({commit}){
    //console.log("req canceled");
    commit('setConcordancesLoading',null);
  },
  resetConcordances({commit}){
    commit('setConcordances',null);
  }
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
  },
  setConcordances (state, concordances) {
    state.concordances = concordances
  },
  setConcordancesLoading(state,concordances_loading){
    state.concordances_loading = concordances_loading;
  }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
