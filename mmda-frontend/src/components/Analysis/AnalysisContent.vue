<template>
<div>
  <v-card flat>
    <v-card-text>
      <v-container>
        <v-layout justify-space-between row>
          <v-flex v-if="analysis" xs12 sm12>

            <v-alert v-if="updated" value="true" dismissible  color="success" icon="info" outline>Updated Analysis </v-alert>
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              <v-text-field v-model="analysis.name" :value="analysis.name" label="Analysis Name" :rules="[rules.required, rules.alphanum, rules.counter]"></v-text-field>
              <v-text-field :value="analysis.corpus" label="Corpus" box readonly></v-text-field>
              <v-text-field :value="analysis.topic_discourseme.items" label="Topic Items" box readonly></v-text-field>


              <v-btn color="info" class="text-lg-right" :to="/analysis/ + analysis.id + /wordcloud/">Open WordCloud</v-btn>
              <v-btn color="success" class="text-lg-right" @click="updateAnalysis">Update Name</v-btn>
              <v-btn color="info" outline class="text-lg-right" @click="reloadCoordinates">Regenerate Coordinates</v-btn>
              <v-btn color="error" outline class="text-lg-right" @click="deleteAnalysis">Delete</v-btn>

              <AnalysisItemTable/>

              <h1 class="my-3 title">Concordances:</h1>

              <ConcordancesKeywordInContextList v-bind:concordances="concordances"/>
              <AnalysisDiscoursemeList/>

            </v-form>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'
import AnalysisDiscoursemeList from '@/components/Analysis/AnalysisDiscoursemeList.vue'
import AnalysisItemTable from '@/components/Analysis/AnalysisItemTable.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'

import rules from '@/utils/validation'

export default {
  name: 'AnalysisContent',
  components: {
    AnalysisDiscoursemeList,
    AnalysisItemTable,
    ConcordancesKeywordInContextList,
    //AnalysisCoordinates
  },
  data: () => ({
    id: null,
    error: null,
    nodata: false,
    updated: false,
    rules: rules
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      concordances:'corpus/concordances'
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
        name: this.analysis.name
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
