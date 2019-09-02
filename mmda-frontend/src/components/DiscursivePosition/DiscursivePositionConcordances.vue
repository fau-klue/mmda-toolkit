<template>
<div>
  <DiscursivePositionSelection/>

  <v-card flat v-if="concordances.length!==0">
    <v-card-text>
      <v-container>
        <v-layout>

          <v-flex xs12 sm12>
          <h3 class="my-3 body-2">Window Size</h3>
          <v-slider v-model="selectWindow" :max="maxWindow" :min="minWindow" thumb-label="always"
            thumb-size="28"></v-slider>
            <v-tabs color="cyan darken-2" dark slider-color="yellow">
              <v-tab v-for="(concordance, corpus) in concordances" :key="corpus" ripple>
                {{ corpus }}
              </v-tab>
              <v-tab-item v-for="(concordance, corpus) in concordances" :key="corpus">
                <v-card flat>
                  <v-card-text>
                    <ConcordancesKeywordInContextList 
                    v-if="concordance[''+selectWindow] && concordance[''+selectWindow].length!==0" 
                    v-bind:concordances="concordance[''+selectWindow]"/>
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
import DiscursivePositionSelection from '@/components/DiscursivePosition/DiscursivePositionCorporaSelection.vue'
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'

import { mapGetters } from 'vuex'

export default {
  name: 'DiscursivePositionConcordances',
  components: {
    DiscursivePositionSelection,
    ConcordancesKeywordInContextList
  },
  data: () => ({
    search: '',
    minWindow: 1,
    selectWindow: 1,
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      concordances: 'discursive/concordances'
    }),
    maxWindow(){
      var max = 0;
      for(var k of Object.keys(this.concordances)){
        for(var s of Object.keys(this.concordances[k])){
          var ws = Number.parseInt(s);
          max = Math.max(ws, max);
        }
      }
      console.log("Max Window: "+max);
      return max;
    }
  }
}

</script>
