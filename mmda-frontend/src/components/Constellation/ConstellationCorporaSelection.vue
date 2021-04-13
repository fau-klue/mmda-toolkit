<template>
<div>
  <v-layout wrap row>
    <v-flex xs12>
      <v-card flat>
        <v-card-text>
          <v-container>
            <v-layout justify-space-between row>
              <v-flex xs5 sm5>
                <h1 class="title">{{ $t("constellation.extraction.helpTitle") }}</h1>
                <p>
                  {{ $t("constellation.extraction.helpText") }}
                </p>
                <h1 class="subheading">{{ $t("constellation.extraction.corpora") }}</h1>
                <p>
                  {{ $t("constellation.extraction.helpCorpora") }}
                </p>
                <h1 class="subheading">{{ $t("constellation.extraction.analysis") }}</h1>
                <p>
                  {{ $t("constellation.extraction.helpAnalysis") }}
                </p>

              </v-flex>
              <v-flex xs6 sm6>
                <div v-if="loading" class="text-md-center">
                  <v-progress-circular indeterminate color="primary"></v-progress-circular>
                  <p>Loading Concordance...</p>
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

                  <v-autocomplete v-model="selectedAnalysisId" clearable :items="userAnalysis" item-value="id" item-text="name" label="Analysis"></v-autocomplete>
		  <v-slider v-model="selectWindow" :max="maxWindow" :min="minWindow" thumb-label="always"
            thumb-size="28"></v-slider>
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
  name: 'ConstellationCorporaSelection',
  data: () => ({
    id: null,
    error: null,
    loading: false,
    nodata: false,
    selectedCorpora: [],
      selectedAnalysisId: null,
      selectWindow: 3,
      maxWindow: 10,
      minWindow: 1
  }),
    watch: {
	selectedAnalysisId(){
	    // console.log(this.selectedAnalysisId)
	    // console.log(this.selectWindow)
	    this.loadAnalysis(this.selectedAnalysisId).then(()=>{
		this.selectWindow = this.analysis.max_window_size
	    })
	},
	selectWindow(){
	    console.log(this.selectWindow)
	},
	analysis(){
	    // console.log(this.selectedAnalysisId)
	    // console.log(this.selectWindow)
	    // this.selectWindow = this.analysis.max_window_size
	    this.maxWindow = this.analysis.max_window_size
	}
    },
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
      getConstellationConcordances: 'constellation/getConstellationConcordances'
    }),
    clear () {
      this.error = null
      this.nodata = false
      this.selectedAnalysisId = null,
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
      // Return Promise
      return this.getUserSingleAnalysis(data)
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

      if (!this.selectedAnalysisId || this.selectedCorpora.length === 0) {
        this.nodata = true
        return
      }

      this.loading = true
      // this.loadAnalysis(this.selectedAnalysisId).then(() => {
      //   this.error = null
      // }).catch((error) => {
      //   this.error = error
      // }).then(() => {

        const data = {
          username: this.user.username,
          constellation_id: this.id,
          window_size: this.selectWindow,
          analysis: this.analysis.id,
          corpora: this.selectedCorpora
        }

        this.getConstellationConcordances(data).then(() => {
          this.error = null
        }).catch((error) => {
          this.error = error
        }).then(() => {
          this.loading = false
        })
      // })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadAnalysisList()
    this.loadCorpora()
  }
}

</script>
