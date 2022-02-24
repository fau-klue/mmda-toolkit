<template>
    <v-card class="wordtree-view-card">
      <v-card-text>
        <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline>An Error occured</v-alert>
        <v-alert v-else-if="!concordancesRequested" value="true" color="info" icon="priority_high" outline>No concordance requested</v-alert>

        <div v-else-if="loading" class="text-md-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <p v-if="loading">Loading Concordance...</p>
          <p v-if="loading && typeof loading==='object'">{{"["+loading.topic_items+"] ["+loading.collocate_items+"]"}}</p>
        </div>

        <div v-else>
          <p>
            {{output}}
          </p>
        </div>
      </v-card-text>
    </v-card>
</template>

<style>
.wordtree-view-card{
  overflow: auto;
}

</style>

<script>
import { mapActions, mapGetters } from 'vuex'

export default {
  name: 'ConcordancesContextWordTree',
  components: {
  },
  props:['concordances','loading'],
  data: () => ({
    id: null,
    error: null,
    keywordRole: 'topic',
    useSentiment:false,
    concordancesRequested: false,
  }),
  watch:{
    concordances(){
      this.concordancesRequested = true;
      //the required data (see setupIt) is available only after two ticks
      this.update();
    },
    loading(){
      if(this.loading) this.concordancesRequested = true;
      //console.log("load "+this.loading);
    }

  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      collocation: 'collocation/collocation',
      corpus: 'corpus/corpus',
    }),
    output(){
      var result = "";

      if(!this.corpus) return '';
      var p_att = this.corpus.p_att;

      var pre_context = new Map();
      var keyword = new Map();
      var post_context = new Map();

      for(var c of this.concordances){
        var pre = null;
        var context = pre_context;
        for(var i=0; i<c.word.length; ++i){  
          var el = {
            text:   c.word[i],
            role:   c.role[i],
            lemma:  c[p_att][i],
            next:   null,
          };
          el.prev = pre;
          if(pre){
            pre.next = el;
          }
          if(context==pre_context && el.role==this.keywordRole){
            context = post_context;
            if(keyword.has(el.lemma)){
              el.similar = keyword.get(el.lemma);
              el.similar.push(el);
            }else{
              keyword.set(el.lemma, el.similar=[el]);
            }
          }else{
            if(context.has(el.lemma)){
              el.similar = context.get(el.lemma);
              el.similar.push(el);
            }else{
              context.set(el.lemma, el.similar=[el]);
            }
          }
          pre = el;
        }
      }

/*
      var roots = [];

      for(var [key,arr] of keyword.entries()){

        var root = { };
        root.nexts = new Map();
        nex(root, arr, root.nexts);
        roots.push(root);

        function nex(node, arr, nxMap){
          for(var el of arr){
            if(!el.next) continue;
            if(nxMap.has(el.next.lemma)){
              nxMap.get(el.next.lemma).push(el.next);
            }else{
              nxMap.set(el.next.lemma,[el.next]);
            }
          }
          for(var [key,value] of nxMap){
            var node2 = {};
            node2.nexts = new Map();
            node2 = nex(node2, value, node.nexts);
          
          }
          return node;
        }

        for(var [key,value] of nxMap.entries()){
          
        }

        
        var prMap = new Map();
        for(var v of value){
          if(!v.prev) continue;
          if(prMap.has(v.prev.lemma)){
            prMap.get(v.prev.lemma).push(v.prev);
          }else{
            prMap.set(v.prev.lemma,[v.prev]);
          }
        }


    }*/



      return result;
    }
  },
  
  methods: {
    ...mapActions({
      getConcordances: 'collocation/getConcordances',
      getCorpus: 'corpus/getCorpus'
    }),
    update(){
      //the required data (see setupIt) is available only after two ticks
      //this.$nextTick(()=>this.$nextTick(()=>this.setupTableSize()));
    },
    clickOnLemma (name) {
      if(!this.collocation) return;
      this.concordancesRequested = true;
      this.getConcordances({
        username :this.user.username,
        collocation_id: this.id,
        //        corpus:           this.collocation.corpus,
        topic_items:      this.collocation.items,
        soc_items: undefined, //TODO
        collocate_items:  [name],
        window_size:      this.windowSize
      }).catch((error)=>{
        this.error = error
      }).then(()=>{
      });
    }
  },
  created () {
    this.id = this.$route.params.id;
    if(!this.collocation) return this.$router.push("/collocation"); //fallback
    this.getCorpus(this.collocation.corpus).catch((error)=>{
      this.error = error;
    });
  }
}

</script>
