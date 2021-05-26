<template>
  <v-bottom-sheet class="wordcloud-bottom-sheet" v-model="sheet">
    <v-card class="wordcloud-bottom-card">

      <!-- TODO:: let this button hover over the content below, to not waste space-->
      <!-- <v-btn @click="shown=!shown" v-if="shown" icon title="close concordance view">X</v-btn> -->
      <ConcordancesKeywordInContextList ref="kwic" v-bind:shown="shown"
      v-bind:concordances="concordances"
      v-bind:loading="loading"
      v-bind:onclickitem="onclickitem"/>
      <!-- <ConcordancesContextWordTree v-bind:concordances="concordances" v-bind:loading="loading"/> -->
      <v-layout>
        <v-spacer />
        <v-btn v-if="shown && !loading" icon ripple>
          <v-icon class="grey--text text--lighten-1" title="download concordances (.csv)" @click="downloadConcordancesCSV">file_copy</v-icon>
        </v-btn>
      </v-layout>
      <div v-if="!shown" class="text-md-center">
        <v-progress-circular v-if="loading" indeterminate color="primary"></v-progress-circular>
        <div v-else> <v-btn @click="shown=!shown" icon><v-icon>keyboard_arrow_up</v-icon></v-btn> Concordances</div>
      </div>

    </v-card>
  </v-bottom-sheet>
</template>

<style>
.wordcloud-bottom-card{
  /* max-height: 100%;   /\*does not work like that, because parents have no height.   -> therefore max-height is set on mounted*\/ */
  overflow: auto; 
}
</style>

<script>
import { mapGetters, mapActions } from "vuex";
import ConcordancesKeywordInContextList from '@/components/Concordances/ConcordancesKeywordInContextList.vue'
//import ConcordancesContextWordTree from '@/components/Concordances/ConcordancesContextWordTree.vue'

import { domSet } from '@/wordcloud/util_misc.js';

export default {
  name: "WordcloudBottomSheet",
  props:['onclickitem', 'onchangevisibility', 'sheetVisible'],
  components: {
    ConcordancesKeywordInContextList,
//    ConcordancesContextWordTree
  },
  data: () => ({
    shown:true,
    error:null,
    sheet:true
  }),
  computed: {
    ...mapGetters({
      concordances: 'analysis/concordances',
      loading: 'analysis/concordances_loading'
    })
  },
  watch:{
    concordances(){
      this.sheet = true;
    },
    sheet(){
      // console.log("in BottomSheet: " + this.sheet)
      if (this.onchangevisibility){
        this.onchangevisibility(this.sheet)
      }
      // if (!this.sheet){
      //   setTimeout(()=>{this.sheet=true},200);
      // }
    },
    sheetVisible(){
      if (this.sheet!=this.sheetVisible){
        this.sheet=this.sheetVisible
      }
    },
    error(){
      this.$refs.kwic.error = this.error;
    },
    loading(){
      // show the sheet after timeout, because:
      // - loading happens on user input
      // - after the input the sheet is automatically set false
      if(this.loading) setTimeout(()=>{this.sheet=true},200);
    },
  },
  methods: {
    ...mapActions({
    }),
    downloadConcordancesCSV(){
      this.$refs.kwic.downloadConcordancesCSV();
    }
  },
  mounted(){
    var E = document.getElementsByClassName("wordcloud-bottom-card");
    for(var e of E){
      e.style.maxHeight  = Math.floor(innerHeight*.8)+"px";
      domSet(e,'maxHeight',Math.floor(innerHeight*.8)+'px');
    }
  }
};
</script>

