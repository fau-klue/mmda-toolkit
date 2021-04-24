<template>
<v-layout row>
  <v-flex xs12 sm12>

    <v-card-title v-if="showHeader">
      Concordance (window: {{ windowSize }})
      <v-btn v-if="!loading" icon ripple>
        <v-icon class="grey--text text--lighten-1" title="download concordances (.csv)" @click="downloadConcordancesCSV">file_copy</v-icon>
      </v-btn>
    </v-card-title>

    <v-card class="kwic-view-card">
      <v-card-text>

        <v-alert v-if="error&&!loading" value="true" color="error" icon="priority_high" :title="error" outline @click="error=null">{{ error }}</v-alert>
        <v-alert v-else-if="!concordances&&!loading" value="true" color="info" icon="priority_high" outline>No concordance requested</v-alert>

        <div v-else-if="loading" class="text-md-center">
          <p>Loading Concordance...</p>
          <p>{{ loading }}</p>
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </div>

        <v-data-table v-else :items="tableContent" :headers="headers" :disable-initial-sort="true"
                      :hide-actions="tableContent.length<=5" class="kwic-view-table kwic-view-compact"
                      @update:pagination="$nextTick(()=>$nextTick(()=>setupTableSize()))">

          <template slot="items" slot-scope="props">

            <td class="text-xs-center">
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
              <!-- invisible x at the beginning, preventing special characters like @#,.- etc to be moved to the end of the sentence by ellipsis/rtl -->
              <template v-for="(el,idx) in props.item.head">
                <span :key="'s_'+idx">&#160;</span>
                <span :key="'h_'+idx" 
                      @click="selectItem(el)"
                      :class="'concordance '+el.role + (!isCollocate(el.lemma) ? ' nocollocate':'') "
                      :style="el.style + ';direction:ltr'"
                      :title="el.lemma">{{el.text}}</span>
              </template>
              <!-- invisible x at the end, preventing special characters like @#,.- etc to be moved to the front of the sentence by ellipsis/rtl -->
              <span style="color:#0000;">x</span> 
            </td>

            <td class="text-xs-center keyword" 
                @click="toggleKwicMode" 
                :class="'concordance '+props.item.keyword.role"
                :title="props.item.keyword.lemma"><span class="kwic-keyword">{{ props.item.keyword.text }}</span>
            </td>

            <td class="text-xs-left kwic-context">
              <template v-for="(el,idx) in props.item.tail">
                <span :key="'s2_'+idx">&#160;</span>
                <span :key="'t_'+idx"
                      @click="selectItem(el)"
                      :class="'concordance '+el.role + (!isCollocate(el.lemma) ? ' nocollocate':'') "
                      :style="el.style"
                      :title="el.lemma">{{el.text}}</span>
              </template>
            </td>

            <td v-if="useSentiment" class="text-xs-center kwic-sentiment"
                :value="props.item.sentiment"
                :style="'color:'+sentimentColor[ props.item.sentiment ]">
              {{ sentimentEmotion[ props.item.sentiment ] }}
            </td>

            <!-- <td class="text-xs-center"> -->
            <!--   {{ props.item.meta }} -->
            <!-- </td> -->

          </template>

        </v-data-table>
      </v-card-text>
    </v-card>
  </v-flex>
</v-layout>

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
import {domSet, random_color, hex_color_from_array, downloadText} from '@/wordcloud/util_misc.js'

export default {
  name: 'ConcordancesKeywordInContextList',
  components: {
  },
  props: ['showHeader', 'concordances', 'loading', 'onclickitem'],
  data: () => ({
    item: null,
    implementedSOC_conc: false, //TODO:
    id: null,
    error: null,
    keywordRole: 'node',
    useSentiment: false,
    concordancesRequested: false,
    loadingConcordances: false,
    sentimentColor: ['green','yellow','red'],
    sentimentEmotion: ['😃','😐','😠'],
  }),
  watch:{
    concordances(){
      this.concordancesRequested = true;
      this.error=null;
      // the required data (see setupIt) is available only after two ticks
      this.update();
    },
    loading(){
      if(this.loading) this.concordancesRequested = true;
      // console.log("load "+this.loading);
    },
    windowSize(){
      this.getConcordances({
        username :this.user.username,
        analysis_id: this.id,
        window_size: this.windowSize,
      })
      this.update()
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
      // var p_att = 'p_query';//this.corpus.p_att;
      
      // console.log(p_att);
      // console.debug(this.concordances)
      if(!this.concordances) return C;
      for(var ci of Object.keys(this.concordances)){
        var c = this.concordances[ci]
        var r = { 
          head: [],
          match_pos: ci,
          keyword: {text:'',role:'',lemma:''},
          tail: [],
          // meta: [],
          sentiment: 0,
          // these are for sorting context -purposes
          reverse_head_text: '',
          head_text: '',
          tail_text: ''
        };
        Object.assign(r, c);
        var beforeKeyword = true;

        // TODO:: assign correct sentiment
        r.sentiment = Math.floor( Math.random() * this.sentimentEmotion.length);
        // r.meta = 's'

        for(var i=0; i<c.word.length; ++i){  
          // console.log(c);
          var el = {
            text:   c.word[i],
            role:   c.role[i]? c.role[i].join(" "): "None",
            lemma:  c[this.analysis.p_query][i]
          };

          // if(!el.role) el.role = " ";
          // console.log("hello "+c.role);
          // if(!el.role) {console.log("hello "+el.role+"    "+c.role+"    "+i); console.log(c);}
          for(var role of c.role[i]){
              var nr = Number.parseInt(role);
              if(!role){
                //console.log("Role: '"+role + "' for '"+c.word[i]+"'");
                //continue;
                // nr = -1;
                continue;
              }
              if(nr!==nr) continue;
              var col = random_color(nr);
              el.style = 'text-decoration: ' + hex_color_from_array(col) + " underline double;";
              col[3] = 0.1;
              el.style += 'background-color: ' + hex_color_from_array(col) + ";";
              //console.log(el.style);
          }

          if(beforeKeyword && el.role.includes(this.keywordRole)){
            beforeKeyword=false;
            r . keyword = el;
            continue;
          }
          else if(beforeKeyword){
            r . head.push(el);
            r . head_text += ' '+el.text;
          }
          else{
              if(el.role.includes(this.keywordRole)){
                  r . keyword.text += ' '+el.text;
                  r . keyword.lemma += ' '+el.lemma
              }
              else{
                  r . tail.push(el);
                  r . tail_text += ' '+el.text;
              }
          }
        }

        r.reverse_head_text = r.head_text.split("").reverse().join("");
        C.push(r);
        // console.log(r)
	// console.log(c)
	// return C

      }
      //console.log(this.csvFileText);
      return C;
    },
    csvFileText(){
      var colSeparator="\t";
      var rowSeparator="\n";
      var whitespace=" ";
      var text = "ID\t... context\tkeyword\tcontext ...\n";
      if(!this.corpus) return "";
      if(!this.concordances) return "";
      var firstRow = true;
        for(var ci of Object.keys(this.concordances)){
            var c = this.concordances[ci]
        var beforeKeyword = true;
        var firstWord = true;
        if(!firstRow) text+=rowSeparator;
        text += ci+colSeparator;
        for(var i=0; i<c.word.length; ++i){  
          if(beforeKeyword && c.role[i] && c.role[i].includes(this.keywordRole)){
            beforeKeyword=false;
            text += colSeparator+c.word[i]+colSeparator;
            firstWord = true;
          }else{
            text += ((!firstWord)?whitespace:"")+ c.word[i];
            firstWord = false;
          }
        }
        firstRow = false;
      }
      return text;
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
    downloadConcordancesCSV(){
      downloadText("concordances.csv",this.csvFileText.replace(/"/g,"&quot;"));
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
      // if( item.role.includes('collocate') || item.role.includes('topic') ) this.toggleKwicMode(); 
      //else if( item.role == 'out_of_window') return;
      if(this.onclickitem) this.onclickitem(item.lemma);
      else this.clickOnLemma(item.lemma);
    },
    toggleKwicMode (){
      return; //see selectItem
      //this.keywordRole = this.keywordRole=='collocate'?'topic':'collocate';
      //this.update();
    },
    clickOnLemma (item) {
      this.error = null;
      this.concordancesRequested = true;
      this.getConcordances({
        username :this.user.username,
        analysis_id: this.id,
        window_size: this.windowSize,
        items: item? [item]: []
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
      this.clickOnLemma();
    }
    // console.log("we are here");
  }
}

</script>
