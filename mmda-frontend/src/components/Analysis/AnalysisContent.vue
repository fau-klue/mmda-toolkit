<template>
<div>
  <v-card flat>
    <v-card-text>

      <v-container>
        <v-layout v-if="analysis" justify-space-between row>
          <v-flex xs8 sm8>
            <v-card-title>Analysis</v-card-title>

            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Analysis Updated </v-alert>
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>

            <v-form>
              <v-layout row>
                <v-text-field v-model="analysis.topic_discourseme.id" :value="analysis.topic_discourseme.id" label="ID" box readonly></v-text-field>
                <v-spacer/>
                <v-text-field v-model="analysis.name" :value="analysis.name" label="analysis name"></v-text-field>
                <v-btn color="info" class="text-lg-right" @click="updateAnalysis">Update</v-btn>
              </v-layout>

              <v-text-field v-model="analysis.topic_discourseme.name" :value="analysis.topic_discourseme.name" label="discourseme" box readonly></v-text-field>
              <v-text-field :value="analysis.corpus" label="corpus" box readonly></v-text-field>
              <v-text-field :value="analysis.items" label="items" box readonly></v-text-field>
              <v-layout row>
                <v-text-field v-model="analysis.p_query" :value="analysis.p_query" label="query layer (p-att)" box readonly></v-text-field>
                <v-spacer/>
                <v-text-field v-model="analysis.s_break" :value="analysis.s_break" label="context break (s-att)" box readonly></v-text-field>
              </v-layout>
            </v-form>

            <v-layout row>
              <v-btn color="success" class="text-lg-right" @click="useForNewAnalysis">Duplicate and Modify</v-btn>
              <v-spacer/>
              <v-btn color="error" class="text-lg-right" @click.stop="dialogDelete = true">Delete</v-btn>
              <v-dialog v-model="dialogDelete" max-width="290">
                <v-card>
                  <v-card-title class="headline">Delete Analysis?</v-card-title>
                  <v-card-text>
                    You’re about to permanently delete this analysis. Once deleted, it cannot be undone or recovered.
                  </v-card-text>
                  <v-card-actions>
                    <v-spacer/>
                    <v-btn outline @click="dialogDelete = false">Close</v-btn>
                    <v-btn color="error" @click="deleteAnalysis">Delete</v-btn>
                  </v-card-actions>
                </v-card>
              </v-dialog>
            </v-layout>
          </v-flex>
          <v-spacer/>
          <v-flex xs4 sm4>
            <v-card-title>WordCloud</v-card-title>
            <div class="minimap_button" @click="gotoWordcloud" title="Open Wordcloud">
              <WordcloudMinimap v-bind:height="25"/>
            </div>
            <div class="text-xs-center">
              <v-btn color="info" class="text-lg-right" @click="reloadCoordinates">Regenerate Coordinates</v-btn>
            </div>
          </v-flex>
        </v-layout>
      </v-container>
      
      <v-container>
        <!-- concordance -->
        <v-layout v-if="concordances||concordances_loading||show_concordances" row>
          <v-flex xs12 sm12>
            <v-card-title>
              Concordance
              <v-btn v-if="!concordances_loading" icon ripple>
                <v-icon class="grey--text text--lighten-1" title="download concordances (.csv)" @click="downloadConcordancesCSV">file_copy</v-icon>
              </v-btn>
            </v-card-title>
            <ConcordancesKeywordInContextList ref="kwicView" v-bind:concordances="concordances" v-bind:loading="concordances_loading" v-bind:shown="true"/>
          </v-flex>
        </v-layout>
        <v-layout v-else>
          <v-card-title>Concordance</v-card-title>
          <v-btn color="info" class="text-lg-right" @click="show_concordances=true">Show Concordance</v-btn>
        </v-layout>
      </v-container>

      <v-container>
        <!-- collocates -->
        <v-layout v-if="analysis" row>
          <v-flex xs12 sm12>
            <AnalysisItemTable/>
          </v-flex>
        </v-layout>
      </v-container>

      <v-container>
        <!-- discourseme overview -->
        <v-layout row>
          <v-flex xs12 sm12>
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
    dialogDelete: false,
    rules: rules,
    show_concordances: false
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates:'analysis/collocates',
      concordances:'analysis/concordances',
      concordances_loading:'analysis/concordances_loading',
    })
  },
  watch:{
    collocates(){
      this.resetConcordances();
    }
  },
  methods: {
    ...mapActions({
      getUserSingleAnalysis: 'analysis/getUserSingleAnalysis',
      updateUserAnalysis: 'analysis/updateUserAnalysis',
      deleteUserAnalysis: 'analysis/deleteUserAnalysis',
      reloadAnalysisCoordinates: 'coordinates/reloadAnalysisCoordinates',
      resetConcordances: 'analysis/resetConcordances'
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
    downloadConcordancesCSV(){
      //console.log(this.$refs.kwicView);
      this.$refs.kwicView.downloadConcordancesCSV();
    },
    deleteAnalysis () {
      this.dialogDelete = false

      const data = {
        username: this.user.username,
        analysis_id: this.id
      }
      this.deleteUserAnalysis(data).then(() => {
        this.error = null
        this.$router.push('/analysis')
        this.dialogDelete = false
      }).catch((error) => {
        this.error = error
        this.dialogDelete = false
      })
    },
    useForNewAnalysis () {
      let A = this.analysis;
      var q = "?name="+A.name;
      q+="&corpus="+A.corpus;
      q+="&window="+A.context;
      for(var i of A.items) q+="&item="+i;
      this.$router.push('/analysis/new'+q);
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
        // p_query: this.analysis.p_query,
        // s_break: this.analysis.s_break,
        // window_size: this.analysis.context
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
    this.resetConcordances()
    this.loadAnalysis()
  }
}

</script>
