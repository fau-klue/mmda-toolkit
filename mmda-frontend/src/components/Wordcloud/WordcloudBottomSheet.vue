<template>
  <v-bottom-sheet class="wordcloud-bottom-sheet" hide-overlay v-model="sheet">
    <v-card class="wordcloud-bottom-card">
      <ConcordancesKeywordInContextList v-bind:concordances="concordances"/>
    </v-card>
  </v-bottom-sheet>
</template>

<style>
.wordcloud-bottom-card{
  max-height: 50%;   /*does not work like that, because parents have no height.   -> therefore max-height is set on mounted*/
  overflow: auto; 
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
  },
  mounted(){
    var E = document.getElementsByClassName("wordcloud-bottom-card");
    for(var e of E){
      e.style.maxHeight  = Math.floor(innerHeight*0.5)+"px";
    }
  }
};
</script>

