<template>
<div>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout justify-space-between row>
              <v-flex xs5 sm5>
                <h1 class="title">Discursive Position Collocate Extraction</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
                </p>
                <h1 class="subheading">Corpora</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>
                <h1 class="subheading">Analysis</h1>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Loading Concordances...</p>
                </div>

                <v-form v-else>
                  <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Please enter missing data</v-alert>
                  <v-alert v-if="error" value="true" color="error" icon="priority_high" outline>Error during Concordance extraction</v-alert>

                  <v-select
                    v-model="selectedCorpora"
                    :items="corpora"
                    label="Corpora"
                    item-value="name_api"
                    item-text="name"
                    multiple
                    chips
                    persistent-hint
                    ></v-select>

                  <v-autocomplete v-model="selectedAnalysis" clearable :items="userAnalysis" item-text="name" label="Analysis"></v-autocomplete>

                  <v-btn color="success" class="text-lg-right" @click="loadConcordances">Submit</v-btn>
                  <v-btn color="info" outline class="text-lg-right" @click="clear">Clear</v-btn>
                </v-form>
              </v-flex>
            </v-layout>
          </v-container>
        </v-card-text>
      </v-card>
    </v-flex>
  </v-layout>
</div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'DiscursivePositionCorporaSelection',
  data: () => ({
    id: null,
    error: null,
    loading: false,
    nodata: false,
    selectedCorpora: [],
    selectedAnalysis: null
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      corpora: 'corpus/corpora',
      userAnalysis: 'analysis/userAnalysis',
    })
  },
  methods: {
    ...mapActions({
      getCorpora: 'corpus/getCorpora',
      getUserAnalysis: 'analysis/getUserAnalysis',
      getUserSingleAnalysis: 'analysis/getUserSingleAnalysis',
      getDiscursivePositionConcordances: 'discursive/getDiscursivePositionConcordances'
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.selectedAnalysis = null,
      this.selectedCorpora = []
    },
    clearSearch () {
      this.search = ''
    },
    loadAnalysisList () {
      this.getUserAnalysis(this.user.username).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadAnalysis (id) {
      const data = {
        username: this.user.username,
        analysis_id: id
      }
      this.getUserSingleAnalysis(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })
    },
    loadCorpora () {
      this.getCorpora().then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    loadConcordances () {
      this.nodata = false

      if (!this.selectedAnalysis || this.selectedCorpora.length === 0) {
        this.nodata = true
        return
      }

      this.loading = true

      this.loadAnalysis()

      console.log(this.analysis)

      const data = {
        username: this.user.username,
        position_id: this.id,
        items: ['foo'],
        corpora: this.selectedCorpora
      }

      this.getDiscursivePositionConcordances(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      }).then(() => {
        this.loading = false
      })

    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadAnalysisList()
    this.loadCorpora()
  }
}

</script>
