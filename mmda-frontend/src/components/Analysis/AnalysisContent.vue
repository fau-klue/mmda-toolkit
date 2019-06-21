<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout v-if="analysis" justify-space-between row>
          <v-flex xs8 sm8>

            <v-alert v-if="updated" value="true" dismissible  color="success" icon="info" outline>Updated Analysis </v-alert>
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              <v-text-field v-model="analysis.name" :value="analysis.name" label="Analysis Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
              <v-text-field :value="analysis.corpus" label="Corpus" box readonly></v-text-field>
              <v-text-field :value="analysis.topic_discourseme.items" label="Topic Items" box readonly></v-text-field>
              <v-text-field v-model="analysis.p_query" :value="analysis.p_query" label="P-Query Attribute"></v-text-field>
              <v-text-field v-model="analysis.s_break" :value="analysis.s_break" label="S-Break Attribute"></v-text-field>

              <!-- <v-btn color="info" class="text-lg-right" :to="/analysis/ + analysis.id + /wordcloud/">Open WordCloud</v-btn> -->
              <v-btn color="success" class="text-lg-right" @click="updateAnalysis">Update Name</v-btn>
              <v-btn color="info" outline class="text-lg-right" @click="reloadCoordinates">Regenerate Coordinates</v-btn>
              <v-btn color="error" outline class="text-lg-right" @click="deleteAnalysis">Delete</v-btn>
              <v-btn color="error" outline class="text-lg-right" @click="editAnalysis">Edit</v-btn>

            </v-form>
          </v-flex>

          <v-flex xs4 sm4>
            <div class="minimap_button" @click="gotoWordcloud" title="Open Wordcloud">
              <WordcloudMinimap v-bind:label="'Open Wordcloud'"
                                v-bind:height="25"
                  />
                </div>
          </v-flex>

        </v-layout>

        <v-layout v-if="analysis" row>
          <v-flex xs12 sm12>
              <AnalysisItemTable/>
              </v-flex>
        </v-layout>

        <v-layout v-if="concordances" row>
          <v-flex xs12 sm12>
            <h1 class="my-3 title">Concordances:</h1>
              <ConcordancesKeywordInContextList v-bind:concordances="concordances" v-bind:loading="concordances_loading"/>
          </v-flex>
        </v-layout>

        <v-layout row>
          <v-flex xs12 sm12>
            <h1 class="title">Discoursemes:</h1>
            <AnalysisDiscoursemeList/>
          </v-flex>
        </v-layout>

      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<style>
.minimap_button{
  cursor: pointer;
}
.minimap_button:hover{
  background-color: lightgray;
  transition:all 0.1s linear;
}
</style>

<script>
import { mapActions, mapGetters } from 'vuex'
import AnalysisDiscoursemeList from '@/components/Analysis/AnalysisDiscoursemeList.vue'
import AnalysisItemTable from '@/components/Analysis/AnalysisItemTable.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'
import WordcloudMinimap from '@/components/Wordcloud/WordcloudMinimap.vue'

import rules from '@/utils/validation'

export default {
  name: 'AnalysisContent',
  components: {
    AnalysisDiscoursemeList,
    AnalysisItemTable,
    ConcordancesKeywordInContextList,
    WordcloudMinimap,
    //AnalysisCoordinates
  },
  data: () => ({
    id: null,
    error: null,
    nodata: false,
    updated: false,
    rules: rules,
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      concordances:'analysis/concordances',
      concordances_loading:'analysis/concordances_loading',
    })
  },
  methods: {
    ...mapActions({
      getUserSingleAnalysis: 'analysis/getUserSingleAnalysis',
      updateUserAnalysis: 'analysis/updateUserAnalysis',
      deleteUserAnalysis: 'analysis/deleteUserAnalysis',
      reloadAnalysisCoordinates: 'coordinates/reloadAnalysisCoordinates',
    }),
    loadAnalysis () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      this.getUserSingleAnalysis(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    gotoWordcloud(){
      this.$router.push("/analysis/"+this.analysis.id+"/wordcloud/");
    },
    deleteAnalysis () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      this.deleteUserAnalysis(data).then(() => {
        this.error = null
        this.$router.push('/analysis')
      }).catch((error) => {
        this.error = error
      })
    },
    editAnalysis () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      let A = this.analysis;
      this.deleteUserAnalysis(data).then(() => {
        this.error = null
        var q = "?name="+A.name;
        q+="&corpus="+A.corpus;
        q+="&window="+A.window_size;
        for(var i of A.topic_discourseme.items) q+="&item="+i;
        this.$router.push('/analysis/new'+q);
      }).catch((error) => {
        this.error = error
      })
    },
    updateAnalysis () {
      this.nodata = false
      this.updated = false

      if (!this.analysis.name) {
        this.nodata = true
        return
      }

      const data = {
        analysis_id: this.id,
        username: this.user.username,
        name: this.analysis.name,
        p_query: this.analysis.p_query,
        s_break: this.analysis.s_break
      }

      this.updateUserAnalysis(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    },
    reloadCoordinates () {
      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      this.reloadAnalysisCoordinates(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadAnalysis()
  }
}

</script>
