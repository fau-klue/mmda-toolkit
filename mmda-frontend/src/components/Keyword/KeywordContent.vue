<template>
<div>
  <v-card flat>
    <v-card-text>
      
      <v-container v-if="keyword">
        <v-layout justify-space-between row>
          
          <v-flex xs8 sm8>
            
            <v-alert v-if="updated" value="true" dismissible color="success" icon="info" outline>Keyword Analysis Updated </v-alert>
            <v-alert v-if="nodata" value="true" color="warning" icon="priority_high" outline>Missing Data</v-alert>
            
            <v-form>
              <v-layout row>
                <v-text-field v-model="keyword.corpus" :value="keyword.corpus" label="corpus" box readonly></v-text-field>
                <v-spacer/>
                <v-text-field v-model="keyword.corpus_reference" value="keyword.corpus_reference" label="reference corpus" box readonly></v-text-field>
              </v-layout>
              <v-layout>
                <v-text-field v-model="keyword.p" :value="keyword.p" label="query layer (p-att)" box readonly></v-text-field>
                <v-spacer/>
                <v-text-field v-model="keyword.p_reference" :value="keyword.p_reference" label="query layer (p-att)" box readonly></v-text-field>
              </v-layout>
              <v-layout row>
                <v-btn color="info" class="text-lg-right" @click="reloadCoordinates">Regenerate Semantic Map</v-btn>
                <v-spacer/>
                <v-btn color="error" class="text-lg-right" @click.stop="dialogDelete = true">Delete</v-btn>
              </v-layout>
            </v-form>
            <v-dialog v-model="dialogDelete" max-width="290">
              <v-card>
                <v-card-title class="headline">Delete Analysis?</v-card-title>
                <v-card-text>
                  You're about to permanently delete this analysis. Once deleted, it cannot be undone or recovered.
                </v-card-text>
                <v-card-actions>
                  <v-spacer/>
                  <v-btn outline @click="dialogDelete = false">Close</v-btn>
                  <v-btn color="error" @click="deleteKeyword">Delete</v-btn>
                </v-card-actions>
              </v-card>
            </v-dialog>
          </v-flex>
          
          <v-spacer/>
          
          <v-flex xs4 sm4>
            <div class="minimap_button" @click="gotoWordcloud" title="Open Semantic Map">
              <WordcloudKeywordMinimap v-bind:height="20"/>
            </div>
          </v-flex>
          
        </v-layout>
        
      </v-container>

      <v-container>
        <v-tabs color="blue" dark>
          <v-tab :key="1">Keyword Table</v-tab>
          <v-tab :key="2">Concordance Lines</v-tab>
          <v-tab :key="3">Discoursemes</v-tab>

          <v-tab-item :key="1">
            <ItemTableKeyword/>
          </v-tab-item>
          <v-tab-item :key="2">
            <ConcordancesKeywordKWICList ref="kwicView" v-bind:concordances="concordances" v-bind:loading="concordances_loading" showHeader="true"/>
          </v-tab-item>
          <v-tab-item :key="3">
            <KeywordDiscoursemeList/>
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
import KeywordDiscoursemeList from '@/components/Keyword/KeywordDiscoursemeList.vue'
import ItemTableKeyword from '@/components/ItemTable/ItemTableKeyword.vue'
import ConcordancesKeywordKWICList from '@/components/ConcordancesKeyword/ConcordancesKeywordKWIC.vue'
import WordcloudKeywordMinimap from '@/components/WordcloudKeyword/WordcloudKeywordMinimap.vue'

import rules from '@/utils/validation'

export default {
  name: 'KeywordContent',
  components: {
    KeywordDiscoursemeList,
    ItemTableKeyword,
    ConcordancesKeywordKWICList,
    WordcloudKeywordMinimap
  },
  data: () => ({
    id: null,
    error: null,
    nodata: false,
    updated: false,
    dialogDelete: false,
    rules: rules,
    min: 1
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      keyword: 'keyword/keyword',
      coordinates: 'coordinates/coordinates',
      keywords:'keyword/keywords',
      concordances:'keyword/concordances',
      concordances_loading:'keyword/concordances_loading'
    })
  },
  methods: {
    ...mapActions({
      getUserSingleKeyword: 'keyword/getUserSingleKeyword',
      updateUserKeyword: 'keyword/updateUserKeyword',
      deleteUserKeyword: 'keyword/deleteUserKeyword',
      reloadKeywordCoordinates: 'coordinates/reloadKeywordCoordinates',
      resetConcordances: 'keyword/resetConcordances'
    }),
    loadKeyword () {
      const data = {
        username: this.user.username,
        keyword_id: this.id
      }
      this.getUserSingleKeyword(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    },
    gotoWordcloud(){
      this.$router.push("/keyword/"+this.keyword.id+"/wordcloud/");
    },
    downloadConcordancesCSV(){
      this.$refs.kwicView.downloadConcordancesCSV();
    },
    deleteKeyword () {
      this.dialogDelete = false

      const data = {
        username: this.user.username,
        keyword_id: this.id
      }
      this.deleteUserKeyword(data).then(() => {
        this.error = null
        this.$router.push('/keyword')
        this.dialogDelete = false
      }).catch((error) => {
        this.error = error
        this.dialogDelete = false
      })
    },
    updateKeyword () {
      this.nodata = false
      this.updated = false

      if (!this.keyword.name) {
        this.nodata = true
        return
      }

      const data = {
        keyword_id: this.id,
        username: this.user.username,
        name: this.keyword.name
      }

      this.updateUserKeyword(data).then(() => {
        this.error = null
        this.updated = true
      }).catch((error) => {
        this.error = error
      })
    },
    reloadCoordinates () {
      const data = {
        username: this.user.username,
        keyword_id: this.id
      }
      this.reloadKeywordCoordinates(data).then(() => {
        this.error = null
      }).catch((error) => {
        this.error = error
      })
    }
  },
  created () {
    this.id = this.$route.params.id
    this.loadKeyword()
    this.resetConcordances()
  }
}

</script>
