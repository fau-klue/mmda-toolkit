<template>
  <div>
    <v-checkbox v-model="simple_postags" label="manually choose POS-tags"></v-checkbox>
    <v-checkbox v-if="simple_postags" v-model="advanced_postags" label="advanced POS-tags"></v-checkbox>
    <!-- if-advanced , ... we also might want to include a search option here -->
      <v-container v-if="simple_postags">
        <v-layout row class="xs12" wrap fill-height justify-space-between>
          <v-flex v-for="tag in advanced_postags?posTags_advanced:posTags_simple" :key="tag.name">
            <v-checkbox v-model="tag.selected" :label="tag.name"></v-checkbox>
          </v-flex>
        </v-layout>
      </v-container>
  </div>
</template>
<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'AnalysisPosTagsSelection',
  data: () => ({
    simple_postags:false,
    advanced_postags:false,
    posTags_simple:[
    ],
    posTags_advanced:[
    ]
  }),
  computed: {
    ...mapGetters({
    })
  },
  methods: {
    ...mapActions({
    }),
  },
  created () {
    var Simple = ['NOUN','ADJ','ADV','VERB','INTJ','PROPN',"ADP","PUNCT","AUX","SYM","CCONJ","X","DET","NUM","PART","PRON","SCONJ"]
    for(var i of Simple) this.posTags_simple.push({name:i,selected:Math.random()<0.5})
    for(var i=0;i<5;i++) for(var j of Simple) this.posTags_advanced.push({name:j+i,selected:Math.random()<0.5})
  }
}

</script>
