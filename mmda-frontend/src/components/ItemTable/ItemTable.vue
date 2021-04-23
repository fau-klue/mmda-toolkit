<template>
<v-layout v-if="analysis" row>
  <v-flex xs12 sm12>
    
    <v-card-title>
      Collocates (window: {{ windowSize }})
      <v-btn icon ripple>
        <v-icon class="grey--text text--lighten-1" title="download collocation list (.csv)" @click="downloadCollocationCSV">file_copy</v-icon>
      </v-btn>
      <v-spacer/>
      <v-text-field v-model="search" append-icon="mdi-magnify" label="Search" single-line hide-details ></v-text-field>
    </v-card-title>
    
    <v-alert v-if="error" value="true" color="error" icon="priority_high" :title="error" outline @click="error=null">{{ error }}</v-alert>
    
    <div v-else-if="loadingCoordinates || loadingCollocates" class="text-md-center">
      <v-progress-circular indeterminate color="primary"></v-progress-circular>
      <p v-if="loadingCoordinates">Loading Coordinates...</p>
      <p v-if="loadingCollocates">Loading Collocates...</p>
    </div>
    
    <!-- TODO: sorting, number of items -->
    <v-data-table v-else :headers="headers" :items="transposedCoordinates" :items-per-page="10" :search="search" :sort-by="'log ratio'" class="elevation-1">
      
      <template slot="items" slot-scope="props">
        <td v-for="el in headers" :key="props.item.name+el.text" class="text-xs-center">
          <div v-if="el.value==='name'">
            <v-layout row>
              <v-btn @click="gotoConcordanceViewOf(props.item)" icon ripple :title="'show concordances of '+props.item.name">
                <v-icon class="grey--text text--lighten-1">info</v-icon>
              </v-btn>
              <div class="analysis-table-name">{{props.item.name}}</div>
            </v-layout>
          </div>
          <div v-else-if="props.item[el.value+'#Norm']===undefined"> {{props.item[el.value]}} </div>
          <div v-else>
            <div class="analysis-table-sphere" :style="
                                                       'width:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'height:'+props.item[el.value+'#Norm']*2+'rem;'
                                                       +'border-radius:'+props.item[el.value+'#Norm']+'rem;'">
              <div class="analysis-table-number">{{props.item[el.value]}}</div>
            </div>
          </div>
        </td>
      </template>
      
    </v-data-table>
  </v-flex>
</v-layout>
</template>

<style>
  .analysis-table-name{
    margin: auto 0;
  }
  .analysis-table-sphere{
    margin:auto;
    background-color:lightgrey;
    position:relative;
  }
  .analysis-table-number{
    margin:auto;
    position:absolute;
    left:50%;
    top:50%;
    transform:translate(-50%,-50%);
    text-shadow:0 0 .5rem white;
  }
</style>

<script>
import { mapActions, mapGetters } from 'vuex'
import { downloadText } from '@/wordcloud/util_misc.js'

export default {
  name: 'ItemTable',
  data: () => ({
    search: '',
    error: null,
    loading: false,
    loadingConcordances:false,
    loadingCollocates:false,
    loadingCoordinates:false,
    min: 1
  }),
  watch:{
    windowSize(){
      this.getCollocates();
    },
    analysis(){
      this.init();
    }
  },
  computed: {
    ...mapGetters({
      user: 'login/user',
      analysis: 'analysis/analysis',
      coordinates: 'coordinates/coordinates',
      collocates: 'analysis/collocates',
      windowSize: 'wordcloud/windowSize',
    }),
    minmaxAM () {
      var R = {};
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          if(!R[am]){
            R[am] = {min:Number.POSITIVE_INFINITY,max:Number.NEGATIVE_INFINITY};
          }
          for(var w of Object.keys(this.collocates[am])){
            var val = Number.parseFloat(this.collocates[am][w]);
            if(val!=val) continue;
            val = this.map_value(val);
            R[am].min = Math.min(R[am].min,val);
            R[am].max = Math.max(R[am].max,val);
          }
        }
      }
      return R;
    },
    transposedCoordinatesFullPrecision () {
      // TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R = {}, val;
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          R[c] = {name:c};
          for(var x of Object.keys(this.coordinates[c])){
            val = this.coordinates[c][x];
            R[c][x] = val;
          }
        }
      }
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          for(var w of Object.keys(this.collocates[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.collocates[am][w];
            val = Number.parseFloat(val);
            R[w][am] = val;
            R[w][am.replace(/\./g,'_')] = val;
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(this.map_value(val), this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);
    },
    transposedCoordinates () {
      // TODO: does this know, that it needs both this.coordinates and this.collocates?
      // and does it update, if any of them changes?
      var R={},val;
      if(this.coordinates){
        for(var c of Object.keys(this.coordinates)){
          R[c] = {name:c};
          for(var x of Object.keys(this.coordinates[c])){
            val = this.coordinates[c][x];
            R[c][x] = typeof val ==="number" ? val.toPrecision(3): val;
          }
        }
      }
      if(this.collocates){
        for(var am of Object.keys(this.collocates)){
          for(var w of Object.keys(this.collocates[am])){
            if(!R[w]) R[w] = { name: w };
            val = this.collocates[am][w];
            val = Number.parseFloat(val);
            R[w][am] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')] = val.toPrecision(2);
            R[w][am.replace(/\./g,'_')+'#Norm'] = this.map_range(this.map_value(val),this.minmaxAM[am]);
          }
        }
      }
      return Object.values(R);
    },
    csvText(){
      var H = this.headers;
      var colSeparator="\t";
      var rowSeparator="\n";
      var text = "";
      var X = this.transposedCoordinatesFullPrecision;

      var firstColumn = true;
      var h ;
      for(h of H){
        if(!firstColumn) text += colSeparator;
        text += h.text;
        firstColumn = false;
      }

      for(var x of X){
        text+=rowSeparator;
        firstColumn = true;
        for(h of H){
          if(!firstColumn) text += colSeparator;
          var val = x[h.value];
          if(val!==undefined && val!==null) text += val;
          firstColumn = false;
        }
      }
      return text;
    },
    headers () {
      var Coll = 
        this.collocates 
      ? Object.keys(this.collocates).map(k=>{
          return {
            text:k, 
            valueWithDot:k, 
            value:k.replace(/\./g,'_'), 
            align:'center'
          }
        }) 
      : [];
      return [
        {text:'item',value:'name',align:'center'},
        ...Coll,
        { text: 'x (auto)', value: 'x', align:"center" },
        { text: 'y (auto)', value: 'y', align:'center' },
        { text: 'x (user)', value: 'x_user', align:'center' },
        { text: 'y (user)', value: 'y_user', align:'center' }
      ];
    }
  },
  methods: {
    ...mapActions({
      getAnalysisCoordinates: 'coordinates/getAnalysisCoordinates',
      getAnalysisCollocates:  'analysis/getAnalysisCollocates',
      getConcordances:        'analysis/getConcordances',
      resetConcordances:      'analysis/resetConcordances'
    }),
    error_message_for(error, prefix, codes){
      if( error.response ){
        let value = codes[ error.response.status ];
        if( value ) return this.$t( prefix+value );
      }
      return error.message;
    },
    downloadCollocationCSV(){
      downloadText("collocation.csv",this.csvText.replace(/"/g,'&quot;'));
    },
    map_value(value){
      return Math.log(1 + Math.max(0,value));
    },
    map_range (value, minmax){
      return (value-minmax.min)/(minmax.max-minmax.min);
    },
    gotoConcordanceViewOf ( item ) {
      if(!this.analysis) return;
      this.loadingConcordances = true;
      this.getConcordances({
        username : this.user.username,
        analysis_id: this.id,
        //corpus:         this.analysis.corpus, 
        topic_items:    this.analysis.items,
        soc_items: undefined,
        collocate_items: [item.name], 
        window_size:    this.windowSize
      }).catch((e)=>{
        this.error = this.error_message_for(e,"analysis.concordances.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingConcordances = false;
      });
    },
    getCollocates(){
      this.loadingCollocates = true;
      this.getAnalysisCollocates({
        username:     this.user.username, 
        analysis_id:  this.id, 
        window_size:  this.windowSize
      }).catch((error)=>{
        this.error = this.error_message_for(error,"analysis.collocates.",{400:"invalid_input",404:"not_found"});
      }).then(()=>{
        this.loadingCollocates = false;
      })
    },
    init(){
      this.loadingCoordinates = true;
      if(this.analysis&&this.analysis.id==this.id){
        this.selectWindow = this.windowSize;
        this.getAnalysisCoordinates({
          username:     this.user.username, 
          analysis_id:  this.id
        }).catch((error)=>{
          this.error = this.error_message_for(error,"analysis.coordinates_request.",{404:"not_found"});
        }).then(()=>{
          this.loadingCoordinates = false;
        });
        this.getCollocates();
      }
    }
  },
  created () {
    this.id = this.$route.params.id
    this.init();
  }
}

</script>
