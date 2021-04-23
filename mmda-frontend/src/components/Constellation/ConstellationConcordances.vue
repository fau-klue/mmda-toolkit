<template>
<div>
  <ConstellationSelection/>

  <v-card flat v-if="concordances.length!==0">
    <v-card-text>
      <v-container>
        <v-layout>

          <v-flex xs12 sm12>
            <v-tabs color="cyan darken-2" dark slider-color="yellow">
              <v-tab v-for="(concordance, corpus) in concordances" :key="corpus" ripple>
                {{ corpus }}
              </v-tab>
              <v-tab-item v-for="(concordance, corpus) in concordances" :key="corpus">
                <v-card flat>
                  <v-card-text>
                    <ConcordancesKeywordInContextList 
                    v-if="concordance.length!==0" 
                    v-bind:concordances="concordance" v-bind:shown="true"/>
                    <v-alert v-else value="true" color="info" outline>No concordances found</v-alert>
                  </v-card-text>
                </v-card>
              </v-tab-item>
            </v-tabs>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>
  </div>
</template>

<script>
import ConstellationSelection from '@/components/Constellation/ConstellationCorporaSelection.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'

import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ConstellationConcordances',
  components: {
    ConstellationSelection,
    ConcordancesKeywordInContextList
  },
  data: () => ({
    search: '',
    minWindow: 1,
    selectWindow: 3,
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      concordances: 'constellation/concordances',
    })
  },
    methods: {
    ...mapActions({
      getConstellationConcordances: 'constellation/getConstellationConcordances'
    }),
  }
}

</script>