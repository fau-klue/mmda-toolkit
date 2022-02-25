<template>
<div>
  <v-card flat>
    <v-card-text>
      
      <v-container v-if="collocation">
        <v-layout justify-space-between row>
          
          <v-flex xs8 sm8>
            
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Collocation Analysis Updated </v-alert>
            
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>
            
            <v-form>
              <v-layout row>
                <v-flex xs3 sm2>
                  <v-text-field v-model="collocation.id" :value="collocation.id" label="ID" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm5>
                  <v-text-field v-model="collocation.topic_discourseme.name" :value="collocation.topic_discourseme.name" label="discourseme" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm5>
                  <v-text-field :value="collocation.corpus" label="corpus" box readonly></v-text-field>
                </v-flex>
              </v-layout>
              <v-text-field :value="collocation.items" label="items" box readonly></v-text-field>
              <v-layout row>
                <v-flex xs3 sm4>
                  <v-text-field v-model="collocation.p_query" :value="collocation.p_query" label="query layer (p-att)" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm4>
                  <v-text-field v-model="collocation.p_collocation" :value="collocation.p_collocation" label="collocation layer (p-att)" box readonly></v-text-field>
                </v-flex>
                <v-flex xs3 sm4>
                  <v-text-field v-model="collocation.s_break" :value="collocation.s_break" label="context break (s-att)" box readonly></v-text-field>
                </v-flex>
              </v-layout>
            </v-form>
            
            <v-layout row>
              <v-btn color="error" class="text-lg-right" @click.stop="dialogDelete = true">Delete</v-btn>
              <v-spacer/>
              <v-btn color="info" class="text-lg-right" @click="reloadCoordinates">Regenerate Semantic Map</v-btn>
              <v-btn color="success" class="text-lg-right" @click="useForNewCollocation">Duplicate and Modify</v-btn>
            </v-layout>

            <v-layout row>
              <v-slider :value="windowSize" :max="collocation.context" ticks="always" :min="min" thumb-label="always" label="context window" thumb-size="28" @change="setWindowSize"/>
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
                  <v-btn color="error" @click="deleteCollocation">Delete</v-btn>
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

      <v-container v-if="breakdown">
        <v-tabs color="blue" dark >

          <v-tab :key="1">Frequency Breakdown</v-tab>
          <v-tab :key="2">Collocate Table</v-tab>
          <v-tab :key="3">Concordance Lines</v-tab>
          <v-tab :key="4">Discoursemes</v-tab>
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
            <ItemTable/>
          </v-tab-item>
          <v-tab-item :key="3">
            <ConcordancesKeywordInContextList ref="kwicView" v-bind:concordances="concordances" v-bind:loading="concordances_loading" showHeader="true"/>
          </v-tab-item>
          <v-tab-item :key="4">
            <CollocationDiscoursemeList/>
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
import CollocationDiscoursemeList from '@/components/Collocation/CollocationDiscoursemeList.vue'
import ItemTable from '@/components/ItemTable/ItemTable.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'
import WordcloudMinimap from '@/components/Wordcloud/WordcloudMinimap.vue'

import rules from '@/utils/validation'

export default {
  name: 'CollocationContent',
  components: {
    CollocationDiscoursemeList,
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
      collocation: 'collocation/collocation',
      coordinates: 'coordinates/coordinates',
      collocates:'collocation/collocates',
      concordances:'collocation/concordances',
      concordances_loading:'collocation/concordances_loading',
      windowSize: 'wordcloud/windowSize',
      breakdown: 'collocation/breakdown',
      meta: 'collocation/meta',
    })
  },
  methods: {
    ...mapActions({
      setWindowSize: 'wordcloud/setWindowSize',
      getUserSingleCollocation: 'collocation/getUserSingleCollocation',
      updateUserCollocation: 'collocation/updateUserCollocation',
      deleteUserCollocation: 'collocation/deleteUserCollocation',
      reloadCollocationCoordinates: 'coordinates/reloadCollocationCoordinates',
      resetConcordances: 'collocation/resetConcordances',
      resetBreakdown: 'collocation/resetBreakdown',
      getCollocationBreakdown: 'collocation/getCollocationBreakdown',
      getCollocationMeta: 'collocation/getCollocationMeta'
    }),
    loadCollocation () {
      const data = {
        username: this.user.username,
        collocation_id: this.id
      }
      this.getUserSingleCollocation(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    gotoWordcloud(){
      this.$router.push("/collocation/"+this.collocation.id+"/wordcloud/");
    },
    downloadConcordancesCSV(){
      //console.log(this.$refs.kwicView);
      this.$refs.kwicView.downloadConcordancesCSV();
    },
    deleteCollocation () {
      this.dialogDelete = false

      const data = {
        username: this.user.username,
        collocation_id: this.id
      }
      this.deleteUserCollocation(data).then(() => {
        this.error = null
        this.$router.push('/collocation')
        this.dialogDelete = false
      }).catch((error) => {
        this.error = error
        this.dialogDelete = false
      })
    },
    useForNewCollocation () {
      let A = this.collocation;
      var q = "?name="+A.name;
      q+="&corpus="+A.corpus;
      q+="&window="+A.context;
      for(var i of A.items) q+="&item="+i;
      this.$router.push('/collocation/new'+q);
    },
    updateCollocation () {
      this.nodata = false
      this.updated = false

      if (!this.collocation.name) {
        this.nodata = true
        return
      }

      const data = {
        collocation_id: this.id,
        username: this.user.username,
        name: this.collocation.name
      }

      this.updateUserCollocation(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    },
    reloadCoordinates () {
      const data = {
        username: this.user.username,
        collocation_id: this.id
      }
      this.reloadCollocationCoordinates(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadCollocation()
    this.resetBreakdown()
    this.getCollocationBreakdown({
      username: this.user.username,
      collocation_id: this.id
    })
    this.resetConcordances()
    this.getCollocationMeta({
      username: this.user.username,
      collocation_id: this.id
    })
  }
}

</script>
