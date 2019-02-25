<template>
  <v-bottom-sheet class="wordcloud-bottom-sheet" hide-overlay v-model="sheet">
    <v-card class="card">
      <ConcordancesKeywordInContextList v-bind:concordances="concordances"/>
    </v-card>
  </v-bottom-sheet>
</template>

<style>
.wordcloud-bottom-sheet .card{
  max-height: 50%;
  overflow: scroll; /*does not work like that*/
}
</style>

<script>
import { mapGetters, mapActions } from "vuex";
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'

export default {
  name: "WordcloudBottomSheet",
  components: {
    ConcordancesKeywordInContextList,
  },
  data: () => ({
    sheet:true,
  }),
  computed: {
    ...mapGetters({
      concordances: 'corpus/concordances'
    })
  },
  watch:{
    concordances(){
      this.sheet=true;
    }
  },
  methods: {
    ...mapActions({
    }),
  }
};
</script>

