<template>
<!--
  <v-bottom-sheet
    value=true
    hide-overlay
    app
    clipped
    persistent
    ref="bottomsheet"
    > -->
    <v-card class="kwic-view-card">
      <v-card-text>

        <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline>An Error occured</v-alert>
        <v-alert v-else-if="!concordancesRequested" value="true" color="info" icon="priority_high" outline>No Concordances requested</v-alert>

        <div v-else-if="loadingConcordances" class="text-md-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <p v-if="loadingConcordances">Loading Concordances...</p>
        </div>

        <v-data-table v-else
          :items="tableContent"
          :headers="headers"
          :disable-initial-sort="false"
          :hide-actions="tableContent.length<=5"
          class="kwic-view-table"
          @update:pagination="$nextTick(()=>$nextTick(()=>setupTableSize()))"
          >
          <!--:headers="headers"
            <template slot="headers" slot-scope="props">
              <template v-for="h in headers">
                <th :class="'column text-xs-'+h.align+' '+h.class?h.class:''" :value="h.value" :key="h.title">
                  {{h.title}}
                </th>
              </template>
             <!- <th class="text-xs-right kwic-context">... context</th>
              <th class="text-xs-center">keyword</th>
              <th class="text-xs-left kwic-context">context ...</th>
              <th v-if="useSentiment" class="text-xs-center">sentiment</th>->
            </template> --> 

            <template slot="items" slot-scope="props">
            <td class="text-xs-center"
                :title="props.item.head_text+' '+props.item.keyword.lemma+' '+props.item.tail_text"
              >
              <v-menu open-on-hover top offset-y>
              
              <span slot="activator" class="kwic-id">{{ props.item.s_pos }}</span>
              
              <v-list>
        <v-list-tile>
          <v-list-tile-content>
            {{props.item.head_text+' '+props.item.keyword.lemma+' '+props.item.tail_text}}
          </v-list-tile-content>
        </v-list-tile>
      </v-list>
    </v-menu>

              <!-- <span class="kwic-id">{{ props.item.s_pos }}</span>-->
            </td>
            <td class="text-xs-right kwic-context kwic-left">
              <!--<span class="reverse-ellipsis">
                <span class="reverse-ellipsis-span">-->
                <!-- spans at the beginning required for direction=rtl to not place the a possible first @-char at the end of the sentence -->
                  <span style="color:#0000;">x</span> 
                  <!-- invisible x at the beginning,
                  preventing special characters like @#,.- etc to be moved to the end of the sentence by ellipsis/rtl -->
                  <template v-for="(el,idx) in props.item.head">
                    <span :key="'s_'+idx">&#160;</span>
                    <span :key="'h_'+idx" 
                    @click="selectItem(el)"
                    :class="'concordance '+el.role"
                    :title="el.lemma">{{el.text}}</span>
                  </template>
                  <!-- invisible x at the end,
                  preventing special characters like @#,.- etc to be moved to the front of the sentence by ellipsis/rtl -->
                  <span style="color:#0000;">x</span> 
                <!--</span>
              </span>-->
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
                  :class="'concordance '+el.role"
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

<!--  </v-bottom-sheet>
  </div> -->

</template>

<style>
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
.kwic-view-table .concordance.none{
  color:#aaa;
}
.kwic-view-table .concordance.token{
  cursor:pointer;
}
.kwic-view-table .concordance.collocate, 
.kwic-view-table .concordance.topic{
  font-weight:bold;
  cursor:pointer;
}

.kwic-view-card{
  overflow: auto;
}

.reverse-ellipsis {
  text-overflow: clip;
  position: relative;
  background-color: white;
}

.reverse-ellipsis:before {
  content: '\02026';
  position: absolute;
  z-index: 1;
  left: -3em;
  background-color: inherit;
  padding-left: 3em;
  margin-left: 0.5em;
}

.reverse-ellipsis .reverse-ellipsis-span {
  min-width: 100%;
  position: relative;
  display: inline-block;
  float: right;
  overflow: visible;
  background-color: inherit;
  text-indent: 0.5em;
}

.reverse-ellipsis .reverse-ellipsis-span:before {
  content: '';
  position: absolute;
  display: inline-block;
  width: 1em;
  height: 1em;
  background-color: inherit;
  z-index: 200;
  left: -0.5em;
}

</style>

<script>
import { mapActions, mapGetters } from 'vuex'
//import AnalysisDiscoursemeList from '@/components/Analysis/AnalysisDiscoursemeList.vue'
//import AnalysisCoordinates from '@/components/Analysis/AnalysisCoordinates.vue'
//import AnalysisItemTable from '@/components/Analysis/AnalysisItemTable.vue'


export default {
  name: 'ConcordancesKeywordInContextList',
  components: {
  },
  data: () => ({
    id: null,
    error: null,
    keywordRole: 'topic',
    useSentiment:false,
    concordancesRequested: false,
    loadingConcordances: false,
    sentimentColor:['green','yellow','red'],
    sentimentEmotion:['😃','😐','😠'],
    /*headers:[
      {text:'s_pos',value:'s_pos'},
      {text:'...',value:'preSentence',align:'right'},
      {text:'keyword',value:'keyword',align:'center'},
      {text:'...',value:'postSentence',align:'left'},
    ]*/
  }),
  watch:{
    concordances(){
      this.concordancesRequested = true;
      //the required data (see setupIt) is available only after two ticks
      this.$nextTick(()=>this.$nextTick(()=>this.setupTableSize()));
    }
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      concordances: 'corpus/concordances'
    }),
   
   
    headers () {
      return [
        { class:'kwic-id-head',text:'ID',value:'s_pos',align:'center'},
        { class:'kwic-context text-xs-right', align:"right", text:'... context', value:'reverse_head_text'},
        { class:'kwic-keyword-head',align:'center', text:'keyword', value:'keyword.text'},
        { class:'kwic-context text-xs-left',align:'left', text:'context ...', value:'tail_text'},
        ...this.useSentiment?[{text:"sentiment",value:'sentiment'}]:[]
      ];
    },
    tableContent () {
      var C = [];
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
          var el = {
            text:   c.word[i],
            role:   c.role[i],
            lemma:  c.tt_lemma[i]
          };

          if(beforeKeyword && el.role==this.keywordRole){
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
          //c.lemmas
        }

        r.reverse_head_text = r.head_text.split("").reverse().join("");

//TODO:: one conceptionally doesnt have to do this, when table positions are correct
       /* if(r.head.length>2){ 
          r.head = r.head.slice(r.head.length-2,r.head.length); 
          r.head.splice(0,{text:'...',role:'none'});
        }
        if(r.tail.length>2){ 
          r.tail = r.tail.slice(0,2); 
          r.tail.push({text:'...',role:'none'});
        }*/

        C.push(r);
      }
      return C;
    }
  },
  /*watch:{
    concordances () {
      console.log(this.tableContent);
    },
  },*/
  
  methods: {
    ...mapActions({
      getConcordances: 'corpus/getConcordances',
    }),
    hideView () {
      // e.g. setConcordances(null);
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
        id.style.width = w+2*pad+"px";      

        E = document.getElementsByClassName("kwic-keyword");
        w = Array.from(E).reduce((sum,e)=>Math.max(e.offsetWidth,sum),0);
        var kw = document.getElementsByClassName("kwic-keyword-head")[0];
        if(kw===undefined) return;
        kw.style.width = w+2*pad+"px";
      }
    },
    selectItem (item) {
      if( item.role == 'collocate' || item.role == 'topic' ) this.toggleKwicMode(); 
      else this.clickOnLemma(item.lemma); 
    },
    toggleKwicMode (){
      this.keywordRole = this.keywordRole=='collocate'?'topic':'collocate';
      //TODO:: update
    },
    clickOnLemma (name) {
      this.loadingConcordances = true;
      this.concordancesRequested = true;
      this.getConcordances({
        corpus:           this.analysis.corpus,
        topic_items:      this.analysis.topic_discourseme.items,
        collocate_items:  [name],
        window_size:      this.windowSize
      }).catch((error)=>{
        this.error = error
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
  },
  created () {
    this.id = this.$route.params.id
  }
}

</script>
