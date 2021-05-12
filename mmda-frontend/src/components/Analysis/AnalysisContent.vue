<template>
<div>
  <v-card flat>
    <v-card-text>
      
      <v-container v-if="analysis">
        <v-layout justify-space-between row>
          
          <v-flex xs8 sm8>
            <!-- <v-card-title>Analysis</v-card-title> -->
            
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Analysis Updated </v-alert>
            
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>
            
            <v-form>
              <v-layout row>
                <v-flex xs3 sm2>
                  <v-text-field v-model="analysis.id" :value="analysis.id" label="ID" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm5>
                  <v-text-field v-model="analysis.topic_discourseme.name" :value="analysis.topic_discourseme.name" label="discourseme" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm5>
                  <v-text-field :value="analysis.corpus" label="corpus" box readonly></v-text-field>
                </v-flex>
                <!-- <v-text-field v-model="analysis.name" :value="analysis.name" label="analysis name" box background-color="white"></v-text-field> -->
              </v-layout>
              <v-text-field :value="analysis.items" label="items" box readonly></v-text-field>
              <v-layout row>
                <v-flex xs3 sm4>
                  <v-text-field v-model="analysis.p_query" :value="analysis.p_query" label="query layer (p-att)" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm4>
                  <v-text-field v-model="analysis.p_analysis" :value="analysis.p_analysis" label="analysis layer (p-att)" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm4>
                  <v-text-field v-model="analysis.s_break" :value="analysis.s_break" label="context break (s-att)" box readonly></v-text-field>
                </v-flex>
              </v-layout>
            </v-form>
            
            <v-layout row>
              <v-btn color="info" class="text-lg-right" @click="reloadCoordinates">Regenerate Semantic Map</v-btn>
              <v-spacer/>
              <v-btn color="success" class="text-lg-right" @click="useForNewAnalysis">Duplicate and Modify</v-btn>
              <v-btn color="error" class="text-lg-right" @click.stop="dialogDelete = true">Delete</v-btn>
            </v-layout>

            <v-layout row>
              <v-slider :value="windowSize" :max="analysis.context" ticks="always" :min="min" thumb-label="always" label="context window" thumb-size="28" @change="setWindowSize"/>
            </v-layout>
            
            <v-dialog v-model="dialogDelete" max-width="290">
              <v-card>
                <v-card-title class="headline">Delete Analysis?</v-card-title>
                <v-card-text>
                  You're about to permanently delete this analysis. Once deleted, it cannot be undone or recovered.
                </v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn outline @click="dialogDelete = false">Close</v-btn>
                  <v-btn color="error" @click="deleteAnalysis">Delete</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-flex>
          
          <v-spacer/>
          
          <v-flex xs4 sm4>
            <!-- <v-card-title>WordCloud</v-card-title> -->
            <div class="minimap_button" @click="gotoWordcloud" title="Open Semantic Map">
              <WordcloudMinimap v-bind:height="20"/>
            </div>
          </v-flex>
          
        </v-layout>
        
      </v-container>

      <v-container v-if="analysis">
        <v-tabs color="blue" dark >

          <v-tab :key="1">Frequency Breakdown</v-tab>
          <v-tab :key="2">Associated Discoursemes</v-tab>
          <v-tab :key="3">Concordance Lines</v-tab>
          <v-tab :key="4">Collocate Table</v-tab>
          <v-tab :key="5">Meta Distribution</v-tab>

          <v-tab-item :key="1">
            <template>
              <v-data-table :headers="breakdownHeaders" :items="breakdown" :pagination.sync="pagination" class="elevation-1">
                <template v-slot:items="props">
                  <td>{{ props.item.item }}</td>
                  <td>{{ props.item.freq }}</td>
                </template>
              </v-data-table>
            </template>
          </v-tab-item>
          <v-tab-item :key="2">
            <AnalysisDiscoursemeList/>
          </v-tab-item>
          <v-tab-item :key="3">
            <ConcordancesKeywordInContextList ref="kwicView" v-bind:concordances="concordances" v-bind:loading="concordances_loading" showHeader="true"/>
          </v-tab-item>
          <v-tab-item :key="4">
            <ItemTable/>
          </v-tab-item>
          <v-tab-item :key="5">
            <center>
              <template v-for="m in meta">
                <v-card v-bind:key="m">
                  <br/>
                  <div v-html="m"> </div>
                  <br/>
                </v-card>
              </template>
            </center>
          </v-tab-item>
        </v-tabs>
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
import ItemTable from '@/components/ItemTable/ItemTable.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'
import WordcloudMinimap from '@/components/Wordcloud/WordcloudMinimap.vue'

import rules from '@/utils/validation'

export default {
  name: 'AnalysisContent',
  components: {
    AnalysisDiscoursemeList,
    ItemTable,
    ConcordancesKeywordInContextList,
    WordcloudMinimap
  },
  data: () => ({
    id: null,
    error: null,
    nodata: false,
    updated: false,
    dialogDelete: false,
    rules: rules,
    min: 1,
    breakdownHeaders: [
      {text: "item", align: "left", value: "item"},
      {text: "frequency", value: "freq"}
    ],
    pagination: {
      sortBy: 'freq',
      descending: true,
      rowsPerPage: 10
    }
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates:'analysis/collocates',
      concordances:'analysis/concordances',
      concordances_loading:'analysis/concordances_loading',
      windowSize: 'wordcloud/windowSize',
      breakdown: 'analysis/breakdown',
      meta: 'analysis/meta',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      getUserSingleAnalysis: 'analysis/getUserSingleAnalysis',
      updateUserAnalysis: 'analysis/updateUserAnalysis',
      deleteUserAnalysis: 'analysis/deleteUserAnalysis',
      reloadAnalysisCoordinates: 'coordinates/reloadAnalysisCoordinates',
      resetConcordances: 'analysis/resetConcordances',
      getAnalysisBreakdown: 'analysis/getAnalysisBreakdown',
      getAnalysisMeta: 'analysis/getAnalysisMeta'
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
    this.resetConcordances()
    this.getAnalysisBreakdown({
      username: this.user.username,
      analysis_id: this.id
    }),
    this.getAnalysisMeta({
      username: this.user.username,
      analysis_id: this.id
    })
  }
}

</script>
