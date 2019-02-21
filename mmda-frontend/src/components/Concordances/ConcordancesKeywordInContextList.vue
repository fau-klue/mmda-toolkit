<template>
  <!-- <v-data-table
    v-if="concordances"
    :headers="headers"
    :items="tableContent"
    class="elevation-1"
    >
    <template slot="items" slot-scope="props">
      <td>{{ props.item.s_pos }}</td>
      <td class="text-xs-right" style="width:0;">{{ props.item.preSentence }}</td>
      <td class="text-xs-center">{{ props.item.keyword }}</td>
      <td class="text-xs-left" style="width:0;">{{ props.item.postSentence }}</td>
    </template>
  </v-data-table>
  <h1 v-else class="title">Click on any item to show concordances.</h1>
-->
<!--
<div>
    <v-card v-if=" !concordances || !concordances.length ">
      <v-card-text>
        <v-layout row>
          <v-flex justify-center>
            <v-avatar><v-icon class="red--text darken-1">warning</v-icon></v-avatar>No concordances found</v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
    <v-card v-else>
      <v-card-text>
        <v-layout row flex avatar>
          <v-flex xs9 class="text-xs-center">
            <v-subheader inset>
              Keyword in context view
            </v-subheader>
          </v-flex>
        </v-layout>
        <v-divider></v-divider>
        <v-data-table
          :items="tableContent"
          class="kwic-view-table"
          hide-headers
          disable-initial-sort
          :hide-actions="tableContent.length<=5"
          >
            <template slot="items" slot-scope="props">
            <td class="text-xs-center">{{props.item.s_pos}}</td>
            <td class="text-xs-right kwic-context">
              <template v-for="(el,idx) in props.item.head">
                <span :key="'s_'+idx">&nbsp;</span>
                <span :key="'h_'+idx" :class="el.role">{{el.text}}</span>
              </template>
            </td>
            <td :class="'text-xs-center '+props.item.keyword.role">{{ props.item.keyword.text }}</td>
            <td class="text-xs-left kwic-context">
              <template v-for="(el,idx) in props.item.tail">
                <span :key="'s2_'+idx">&nbsp;</span>
                <span :key="'t_'+idx" :class="el.role">{{el.text}}</span>
              </template>
            </td>
            <td>{{props.item.sentiment}}</td>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>
-->
<!--
  <v-bottom-sheet
    value=true
    hide-overlay
    app
    clipped
    persistent
    ref="bottomsheet"
    > -->

    <v-card v-if="!concordances || !concordances.length">
      <v-card-text>
        <v-layout row>
          <v-flex justify-center>
            <v-avatar><v-icon class="red--text darken-1">warning</v-icon></v-avatar>
            No concordances found
          </v-flex>
        </v-layout>
      </v-card-text>
    </v-card>
    <v-card v-else class="kwic-view-card">
      <v-card-text>
        <!--<v-btn
          v-if="showConcordances"
          absolute icon ripple slot="activator"
          right
          @click="showConcordances=false"
          >
          <v-icon color="grey lighten-1">close</v-icon>
        </v-btn> -->

        <v-data-table
          :items="tableContent"
          :hide-headers="false"
          :disable-initial-sort="false"
          :hide-actions="tableContent.length<=5"
          class="kwic-view-table"
          >
            <template slot="headers">
              <template v-for="h in [{
                title:'ID',align:'c'
              }]">
                <th class="text-xs-center column sortable" :key="h.title">
                  {{h.title}}
                </th>
              </template>
              <th class="text-xs-right kwic-context">... context</th>
              <th class="text-xs-center">keyword</th>
              <th class="text-xs-left kwic-context">context ...</th>
              <th v-if="useSentiment" class="text-xs-center">sentiment</th>
            </template>

            <template slot="items" slot-scope="props">
            <td class="text-xs-center">{{props.item.s_pos}}</td>
            <td class="text-xs-right kwic-context">
              <template v-for="(el,idx) in props.item.head">
                <span :key="'s_'+idx">&#160;</span>
                <span :key="'h_'+idx" 
                @click="selectItem(el)"
                :class="'concordance '+el.role"
                :title="el.lemma">{{el.text}}</span>
              </template>
            </td>
            <td class="text-xs-center" 
              @click="toggleKwicMode" 
              :class="'concordance '+props.item.keyword.role"
              :title="props.item.keyword.lemma">{{ props.item.keyword.text }}</td>
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
.kwic-view-table .kwic-context{
  width:50%;
}
.kwic-view-table .kwic-sentiment{
  font-size:200%;
  font-weight:bold;
}
.kwic-view-table .concordance.none{
  color:#aaa;
}
.kwic-view-table .concordance.collocate, 
.kwic-view-table .concordance.topic{
  font-weight:bold;
  cursor:pointer;
  padding: 0;
}

.kwic-view-card{
  overflow: auto;
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
    sentimentColor:['green','yellow','red'],
    sentimentEmotion:['😃','😐','😠'],
    /*headers:[
      {text:'s_pos',value:'s_pos'},
      {text:'...',value:'preSentence',align:'right'},
      {text:'keyword',value:'keyword',align:'center'},
      {text:'...',value:'postSentence',align:'left'},
    ]*/
  }),
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      concordances: 'corpus/concordances'
    }),
    tableContent () {
      var C = [];
      if(!this.concordances) return C;
      for(var c of this.concordances){
        var r = { 
          head:[],
          keyword:{text:'',role:'',lemma:''},
          tail:[],
          seltiment:''
          };
        Object.assign(r, c);
        var beforeKeyword = true;

        r.sentiment = Math.random()<0.333?0:Math.random()<0.5?1:2;

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
          }else{
            r . tail.push(el);
          }
          //c.lemmas
        }

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
    selectItem (item) {
      if( item.role == 'collocate' || item.role == 'topic' ) this.toggleKwicMode(); 
      else this.clickOnLemma(item.lemma); 
    },
    toggleKwicMode (){
      this.keywordRole = this.keywordRole=='collocate'?'topic':'collocate';
      //TODO:: update
    },
    clickOnLemma (name) {
      this.getConcordances({
        corpus:           this.analysis.corpus,
        topic_items:      this.analysis.topic_discourseme.items,
        collocate_items:  [name],
        window_size:      this.windowSize
      }).catch((error)=>{
        this.error = error
      });
    },
  },
  created () {
    this.id = this.$route.params.id
  }
}

</script>
