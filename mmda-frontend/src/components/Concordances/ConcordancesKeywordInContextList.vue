<template>
    <v-card class="kwic-view-card">
      <v-card-text>
        <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline>{{error}}</v-alert>
        <v-alert v-else-if="!concordancesRequested" value="true" color="info" icon="priority_high" outline>No concordance requested</v-alert>

        <div v-else-if="loading" class="text-md-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <p v-if="loading">Loading Concordance...</p>
          <p v-if="loading && typeof loading==='object' && !(implementedSOC_conc && loading.soc_items)">{{"["+loading.topic_items+"] ["+loading.collocate_items+"]"}}</p>
          <p v-if="loading && typeof loading==='object' && (implementedSOC_conc && loading.soc_items)">{{"["+loading.topic_items+"] ["+loading.collocate_items+"] ["+loading.soc_items+"]"}}</p>
        </div>

        <v-data-table v-else
          :items="tableContent"
          :headers="headers"
          :disable-initial-sort="false"
          :hide-actions="tableContent.length<=5"
          compact
          class="kwic-view-table kwic-view-compact"
          @update:pagination="$nextTick(()=>$nextTick(()=>setupTableSize()))"
          >
            <template slot="items" slot-scope="props">
            <td class="text-xs-center"
              >
              <v-menu open-on-hover top offset-y>
                <span slot="activator" class="kwic-id">{{ props.item.match_pos }}</span>
                <v-list>
                  <v-list-tile>
                    <v-list-tile-content>
                      {{props.item.head_text+' '+props.item.keyword.text+' '+props.item.tail_text}}
                    </v-list-tile-content>
                  </v-list-tile>
                </v-list>
              </v-menu>
            </td>
            <td class="text-xs-right kwic-context kwic-left">
              <span style="color:#0000;">x</span> 
              <!-- invisible x at the beginning,
              preventing special characters like @#,.- etc to be moved to the end of the sentence by ellipsis/rtl -->
              <template v-for="(el,idx) in props.item.head">
                <span :key="'s_'+idx">&#160;</span>
                <span :key="'h_'+idx" 
                  @click="selectItem(el)"
                  :class="'concordance '+el.role + (!isCollocate(el.lemma) ? ' nocollocate':'') "
                  :title="el.lemma">{{el.text}}</span>
              </template>
              <!-- invisible x at the end,
              preventing special characters like @#,.- etc to be moved to the front of the sentence by ellipsis/rtl -->
              <span style="color:#0000;">x</span> 
            </td>
            <td class="text-xs-center keyword" 
              @click="toggleKwicMode" 
              :class="'concordance '+props.item.keyword.role"
              :title="props.item.keyword.lemma"><span class="kwic-keyword">{{ props.item.keyword.text }}</span></td>
            <td class="text-xs-left kwic-context">
              <template v-for="(el,idx) in props.item.tail">
                <span :key="'s2_'+idx">&#160;</span>
                <span :key="'t_'+idx"
                  @click="selectItem(el)"
                  :class="'concordance '+el.role + (!isCollocate(el.lemma) ? ' nocollocate':'') "
                  :title="el.lemma">{{el.text}}</span>
              </template>
            </td>
            <td v-if="useSentiment" class="text-xs-center kwic-sentiment"
              :value="props.item.sentiment"
              :style="'color:'+sentimentColor[ props.item.sentiment ]">
              {{ sentimentEmotion[ props.item.sentiment ] }}
            </td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
</template>

<style>
.kwic-view-compact td,
.kwic-view-compact th{
  padding: 0 1rem !important;
  height:  0 !important;
}

.kwic-view-table table{
  table-layout: fixed;
  overflow: hidden;
  width:100%;
}
.kwic-view-table td,
.kwic-view-table th{
  overflow: hidden;
  white-space: nowrap;
}
.kwic-view-table .kwic-context{
  table-layout: fixed;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  width:auto;
}
.kwic-view-table .kwic-context.kwic-left{
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
  /* "overflow" value must be different from "visible" */
  direction: rtl;
  text-align: right;
}

.kwic-view-table .kwic-sentiment{
  font-size:200%;
  font-weight:bold;
}

.kwic-view-table span {
  cursor: pointer;
}

.kwic-view-table .concordance.out_of_window,
.kwic-view-table .concordance.nocollocate:not(.topic){
  color:#aaa;
}
.kwic-view-table .concordance{
  cursor:pointer;
}
.kwic-view-table .concordance.collocate, 
.kwic-view-table .concordance.topic{
  font-weight:bold;
}

.kwic-view-table .concordance.out_of_window{
  font-size: 80%;
}

.kwic-view-card{
  overflow: auto;
}

</style>

<script>
import { mapActions, mapGetters } from 'vuex'
import {domSet} from '@/wordcloud/util_misc.js'

export default {
  name: 'ConcordancesKeywordInContextList',
  components: {
  },
  props:['concordances','loading','onclickitem'],
  data: () => ({
    implementedSOC_conc: false, //TODO:
    id: null,
    error: null,
    keywordRole: 'topic',
    useSentiment:false,
    concordancesRequested: false,
    //loadingConcordances: false,
    sentimentColor:['green','yellow','red'],
    sentimentEmotion:['😃','😐','😠'],
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
      analysis: 'analysis/analysis',
      corpus: 'corpus/corpus',
      collocates: 'analysis/collocates',
      windowSize: "wordcloud/windowSize",
      AM: "wordcloud/associationMeasure",
    }),
    headers () {
      return [
        { class:'kwic-id-head',text:'ID',value:'match_pos',align:'center'},
        { class:'kwic-context text-xs-right', align:"right", text:'... context', value:'reverse_head_text'},
        { class:'kwic-keyword-head',align:'center', text:'keyword', value:'keyword.text'},
        { class:'kwic-context text-xs-left',align:'left', text:'context ...', value:'tail_text'},
        ...this.useSentiment?[{text:"sentiment",value:'sentiment'}]:[]
      ];
    },
    tableContent () {
      var C = [];
      if(!this.corpus) return C;
      //var p_att = 'p_query';//this.corpus.p_att;
      
      //console.log(p_att);

      if(!this.concordances) return C;
      for(var c of this.concordances){
        var r = { 
          head:[],
          keyword:{text:'',role:'',lemma:''},
          tail:[],
          sentiment:0,
          //these are for sorting context -purposes
          reverse_head_text:'',
          head_text:'',
          tail_text:''
          };
        Object.assign(r, c);
        var beforeKeyword = true;

        //TODO:: assign correct sentiment
        r.sentiment = Math.floor( Math.random() * this.sentimentEmotion.length);

        for(var i=0; i<c.word.length; ++i){  
          //console.log(c);
          var el = {
            text:   c.word[i],
            role:   c.role[i].join(" "),
            lemma:  c.p_query[i]
          };

          if(!el.role) el.role = " ";


          if(beforeKeyword && el.role.includes(this.keywordRole)){
            beforeKeyword=false;
            r . keyword = el;
            continue;
          }
          if(beforeKeyword){
            r . head.push(el);
            r. head_text += ' '+el.text;
          }else{
            r . tail.push(el);
            r. tail_text += ' '+el.text;
          }
        }

        r.reverse_head_text = r.head_text.split("").reverse().join("");
        C.push(r);
      }
      return C;
    }
  },
  
  methods: {
    ...mapActions({
      getConcordances: 'analysis/getConcordances',
      getCorpus: 'corpus/getCorpus'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    update(){
      //the required data (see setupIt) is available only after two ticks
      this.$nextTick(()=>this.$nextTick(()=>this.setupTableSize()));
    },
    setupTableSize(){
      //This function takes care that:
      // - the id and keyword column of the table match their content
      // while:
      // - the context columns are equally sized, and ellipse their content
      /// TODO:: can wee do it better? 
      // much work has been done to reach this state. 
      // it doesnt seem much easier, given we want to stay with the vue data-table
      var E = document.getElementsByClassName("kwic-id");
      var id = document.getElementsByClassName("kwic-id-head")[0];
      var pad;
      if(id!=undefined){
        pad = window.getComputedStyle(id, null).getPropertyValue('padding-left');
        pad = Number.parseInt(pad.substring(0,pad.length-2));
        var w = Array.from(E).reduce((sum,e)=>Math.max(e.offsetWidth,sum),0);
        //id.style.width = w+2*pad+"px";      
        domSet(id,'width',w+2*pad+'px');


        E = document.getElementsByClassName("kwic-keyword");
        w = Array.from(E).reduce((sum,e)=>Math.max(e.offsetWidth,sum),0);
        var kw = document.getElementsByClassName("kwic-keyword-head")[0];
        if(kw===undefined) return;
        //kw.style.width = w+2*pad+"px";
        domSet(kw,'width',w+2*pad+'px');
      }
    },
    isCollocate(lemma){
      if(!this.collocates || !this.AM || !this.windowSize) return true;
      return this.collocates[this.AM][lemma] !== undefined;
    },
    selectItem (item) {
      //TODO::: there exists no collocate-role anymore so changing the mode is not necessary anymore (even though it might still be beneficial)
      //if( item.role.includes('collocate') || item.role.includes('topic') ) this.toggleKwicMode(); 
      //else if( item.role == 'out_of_window') return;
      if(this.onclickitem) this.onclickitem(item.lemma);
      else this.clickOnLemma(item.lemma);
    },
    toggleKwicMode (){
      return; //see selectItem
      //this.keywordRole = this.keywordRole=='collocate'?'topic':'collocate';
      //this.update();
    },
    clickOnLemma (name) {
      this.error = null;
      this.concordancesRequested = true;
      this.getConcordances({
        username :this.user.username,
        analysis_id: this.id,
        //corpus:           this.analysis.corpus,
        topic_items:      this.analysis.topic_discourseme.items,
        soc_items: undefined, //TODO
        collocate_items:  [name],
        window_size:      this.windowSize
      }).catch((error)=>{
        this.error = this.error_message_for(error,"analysis.concordances.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
      });
    }
  },
  created () {
    this.id = this.$route.params.id;
    if(!this.analysis) return this.$router.push('/analysis'); //fallback


    this.getCorpus(this.analysis.corpus).catch((error)=>{
      this.error = "Analysis or Corpus not Found: "+error.message;//this.error_message_for(error,"corpus.");
    });

    if(!this.loading){
      this.concordancesRequested = true;
      this.update();
    }
  }
}

</script>
