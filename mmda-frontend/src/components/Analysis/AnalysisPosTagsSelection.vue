<template>
  <div>
    <v-checkbox v-model="simple_postags" label="select POS-tags"></v-checkbox>
    <v-checkbox v-if="simple_postags" v-model="advanced_postags" label="advanced POS-tag options"></v-checkbox>
      <v-container v-if="simple_postags">
        <v-layout row fluid class="xs12" wrap fill-height>
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
    for(var i=0;i<10;i++) this.posTags_simple.push({name:'SPT'+i,selected:Math.random()<0.5})
    for(var i=0;i<100;i++) this.posTags_advanced.push({name:'APT'+i,selected:Math.random()<0.5})
  }
}

</script>
